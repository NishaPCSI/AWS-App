<div class="calendar-container">
    <div class="calendar-header">
        <span>
            <button on:click={()=>prev_year()}>&lt;&lt;</button>
            <button on:click={()=>prev()}>&lt;</button>
        </span>
        <div class="month-name">{monthNames[month]} {year} </div>
        <span>
            <button on:click={()=>next()}>&gt;</button>
            <button on:click={()=>next_year()}>&gt;&gt;</button>
        </span>
    </div>

    <Calendar
        {headers}
        {days}
        day_click_callback={goto_id}
    />
</div>

{#each Object.entries(data.task_data).sort() as [date, task] (date)}
    {@const _date = (new Date(Number(date)).toLocaleString("en-US", {day:'numeric',weekday:'short'}))}
    <div class="grid-list">
        <span>
            <div class="date-wrapper" class:today={date === date_today.toString()}>
                {_date}
            </div>
        </span>
        <div class="card-grid-container">
            {#each task as t (t.tid)}
                <CardContainer
                    id={`_${t.deadline}`}
                    title={t.name} 
                    status={TaskStatus[t.status]} 
                    priority={Priority[t.priority]}
                    project={t.project?.name}
                    description={t.description}
                    btn_pri="Done"
                    btn_pri_callback={t.status !== TaskStatus.Finished ? () => {mark_as_done(date,t.tid)} : undefined }
                    btn_sec="Edit"
                    btn_sec_callback={()=> {edit_note = t}}
                    btn_pri_icon="check" />
            {/each}
        </div>
    </div>
{/each}

{#if edit_note !== null}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <EditTaskForm 
        description_value={edit_note.description ?? ''}
        title_value={edit_note.name}
        priority_value={edit_note.priority.toString()}
        phase_value={edit_note.status.toString()}
        link_value={edit_note.pid?.toString() ?? '0' }
        date_value={epoch_to_input(edit_note.deadline)}
        tid_value={edit_note.tid}
        update_data={update_data} 
        user_projects={{...{0:"None"},...data.project_list}} 
        secondaryCallback={()=>{edit_note = null}}
        />
</AbsoluteCenterWrapper>
{/if}


<script lang="ts">
import { TaskStatus, type Task } from "../../../types/Task"
import CardContainer from "../../../components/CardContainer.svelte";
import { API_ENDPOINT } from "../../../store/store";
import { Priority } from "../../../types/Project";
import { chunk_task_data_by_deadline, epoch_to_input, get_today_iso } from "../../../store/utils";
import AbsoluteCenterWrapper from "../../../components/AbsoluteCenterWrapper.svelte";
import EditTaskForm from "../../../components/EditTaskForm.svelte";
import { getMonthCalendar } from "./+page";
import Calendar from "../../../components/Calendar.svelte";
import type { CalendarDay } from "../../../types/CalendarDay";

export const goto_id = (d:CalendarDay) => {
    document.querySelector(`#_${d.date.getTime()}`)?.scrollIntoView({behavior: "smooth"})
}

export let data:{
    activeTab:string,
    project_list:{[key:string]:string},
    task_data:{[key:string]:Task[]}
};

let date_today = get_today_iso()

let edit_note:Task|null = null;

var dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
let monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

let headers:string[] = [];
let now = new Date();
let year = now.getFullYear();		//	this is the month & year displayed
let month = now.getMonth();

var days:CalendarDay[] = [];	//	The days to display in each box

// choose what date/day gets displayed in each date box.
function initContent() {
    headers = dayNames;
    initMonth();
}
initContent()

function initMonth() {
    days = [];
    let monthAbbrev = monthNames[month].slice(0,3);
    let nextMonthAbbrev = monthNames[(month+1)%12].slice(0,3);
    //	find the last Monday of the previous month
    var firstDay = new Date(year, month, 1).getDay();
    //console.log('fd='+firstDay+' '+dayNames[firstDay]);
    var daysInThisMonth = new Date(year, month+1, 0).getDate();
    var daysInLastMonth = new Date(year, month, 0).getDate();
    var prevMonth = month==0 ? 11 : month-1;
    
    //	show the days before the start of this month (disabled) - always less than 7
    for (let i=daysInLastMonth-firstDay;i<daysInLastMonth;i++) {
        let d = new Date(prevMonth==11?year-1:year,prevMonth,i+1);
        days.push({name:''+(i+1),enabled:false,date:d,tasks:[]});
    }
    //	show the days in this month (enabled) - always 28 - 31
    for (let i=0;i<daysInThisMonth;i++) {
        let d = new Date(year,month,i+1);
        if (i==0) days.push({name:monthAbbrev+' '+(i+1),enabled:true,date:d,tasks:data.task_data[d.getTime()] ?? []});
        else days.push({name:''+(i+1),enabled:true,date:d,tasks:data.task_data[d.getTime()] ?? []});
        //console.log('i='+i+'  dt is '+d+' date() is '+d.getDate());
    }
    //	show any days to fill up the last row (disabled) - always less than 7
    for (let i=0;days.length%7;i++) {
        let d = new Date((month==11?year+1:year),(month+1)%12,i+1);
        if (i==0) days.push({name:nextMonthAbbrev+' '+(i+1),enabled:false,date:d,tasks: []});
        else days.push({name:''+(i+1),enabled:false,date:d,tasks:[]});
    }
}

const update_data = async () => {
    let task_data = await getMonthCalendar(year, month, fetch)
    data.task_data = chunk_task_data_by_deadline(await task_data.json())
    initContent()
}

const mark_as_done = async (date:string, tid: string) => {
    let resp = await fetch(`${$API_ENDPOINT}/task/change`,{
        method: 'POST',
        credentials:'include',
        headers:{
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify({
            tid:tid,
            status:TaskStatus.Finished
        })
    })
    if (resp.ok){
        data.task_data[date].filter((x)=>{return x.tid === tid})[0].status = TaskStatus.Finished
        data.task_data = data.task_data
    }
}

const next_year = async () => {
    year++
    await update_data()
    initContent()
}

const prev_year = async () => {
    year--
    await update_data()
    initContent()
}

const next = async () => {
    month++;
    if (month == 12) {
        year++;
        month=0;
    }
    await update_data()
    initContent()
}
const prev = async () => {
    if (month==0) {
        month=11;
        year--;
    } else {
        month--;
    }
    await update_data()
    initContent()
}

</script>

<style>
.calendar-container {
  margin: auto;
  overflow: hidden;
  box-shadow: 0 2px 18px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  background: #fff;
  max-width: 720px;
  padding: 8px;
  margin-bottom: 16px;
}
.calendar-header {
  text-align: center;
  padding: 16px 0;
  display: flex;
  align-items: center;
  font-weight: 700;
  justify-content: center;
}
.month-name{
    display: inline-block;
    width: 250px;
}
.calendar-header button {
  background: var(--primary);
  border-radius: 100px;
  border: none;
  padding: 6px;
  width: 30px;
  color: var(--foreground);
  cursor: pointer;
  outline: 0;
  overflow: hidden;
  font-family: inherit;
}
.grid-list{
    display: grid;
    grid-template-columns: 60px 1fr;
    margin-bottom: 16px;
    gap: 16px;
}
@media only screen and (max-width:600px){
    .grid-list{
        grid-template-columns: none;
    }
}
.date-wrapper{
    font-size: 18px;
    text-align: center;
    padding: 18px 8px;
    border-radius: 16px;
    font-weight: 700;
}
.date-wrapper.today{
    background: var(--primary);
}
.card-grid-container{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
}
</style>