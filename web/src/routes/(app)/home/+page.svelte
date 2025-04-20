<div class="heading">Welcome, {$USER_DATA.fullname}</div>
<div class="task-container">
    <FilledButton icon_left="edit_square" icon_right="add_circle" callback={()=>{add_task = !add_task}}>Task</FilledButton>
    <FilledButton icon_left="assignment" icon_right="add_circle" callback={()=>{add_project = !add_project}}>Project</FilledButton>
    <div class="heading">> Today's Tasks</div>
    <div class="card-grid-container">
        {#each data.task_data.filter(x=>x.status != TaskStatus.Finished) as task (task.tid)}
            <div animate:flip={{duration: 300}}>
                <CardContainer
                    title={task.name} 
                    status={TaskStatus[task.status]}
                    priority={Priority[task.priority]}
                    project={task.project?.name}
                    description={task.description}
                    btn_pri="Done"
                    btn_pri_callback={() => {mark_as_done(task.tid)}}
                    btn_sec="Edit"
                    btn_sec_callback={()=>{edit_task = task}}
                    btn_pri_icon="check" />
            </div>
        {/each}
        {#if data.task_data.filter(x=>x.status != TaskStatus.Finished).length == 0}
            <div class="subheading" transition:fly|local={{y:100}}>All Caught Up !!!</div>
        {/if}
    </div>
</div>
<div class="task-container">
    <div class="heading">> Quick Notes</div>
    <FilledButton icon_left="sticky_note_2" icon_right="add_circle" callback={()=>{add_note = !add_note}}>Notes</FilledButton>
    <div class="card-grid-container">
        {#each data.note_data as note (note.nid)}
            <div animate:flip={{duration: 300}}>
                <CardContainer
                    description={note.content}
                    btn_pri="Delete"
                    btn_pri_callback={() => {delete_note(note.nid)}}
                    btn_sec="Edit"
                    btn_sec_callback={()=>{edit_note = note}}
                    btn_pri_icon="delete"
                />
            </div>
        {/each}
    </div>
    {#if data.note_data.length == 0}
        <div class="subheading" transition:fly|local={{y:100}}>No notes found, you can add some!</div>
    {/if}
</div>
{#if add_task}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <AddTaskForm update_data={update_task_data} user_projects={{...{0:"None"},...data.project_list}} secondaryCallback={()=>{add_task = false}}/>
</AbsoluteCenterWrapper>
{/if}
{#if edit_task !== null}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <EditTaskForm 
        description_value={edit_task.description ?? ''}
        title_value={edit_task.name}
        priority_value={edit_task.priority.toString()}
        phase_value={edit_task.status.toString()}
        link_value={edit_task.pid?.toString() ?? '0' }
        date_value={epoch_to_input(edit_task.deadline)}
        tid_value={edit_task.tid}
        update_data={update_task_data} 
        user_projects={{...{0:"None"},...data.project_list}} 
        secondaryCallback={()=>{edit_task = null}}
    />
</AbsoluteCenterWrapper>
{/if}
{#if add_note}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <AddNoteForm 
        update_data={update_note_data} 
        secondaryCallback={()=>{add_note = false}}
    />
</AbsoluteCenterWrapper>
{/if}
{#if edit_note !== null}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <EditNoteForm
        nid_value={edit_note.nid}
        description_value={edit_note.content}
        update_data={update_note_data} 
        secondaryCallback={()=>{edit_note = null}}
    />
</AbsoluteCenterWrapper>
{/if}
{#if add_project}
    <AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
        <AddProjectForm
            update_data={()=>{}}
            secondaryCallback={()=> {add_project = false}}
        />
    </AbsoluteCenterWrapper>
{/if}

<script lang="ts">
import { API_ENDPOINT, USER_DATA } from "../../../store/store";
import type { Task } from "../../../types/Task";
import CardContainer from "../../../components/CardContainer.svelte";
import { flip } from "svelte/animate";
import { fly } from "svelte/transition";
import AbsoluteCenterWrapper from "../../../components/AbsoluteCenterWrapper.svelte";
import AddTaskForm from "../../../components/AddTaskForm.svelte";
import { Priority } from "../../../types/Project";
import { TaskStatus } from "../../../types/Task";
import EditTaskForm from "../../../components/EditTaskForm.svelte";
import { get_today_iso, epoch_to_input } from "../../../store/utils";
import FilledButton from "../../../components/FilledButton.svelte";
import AddNoteForm from "../../../components/AddNoteForm.svelte";
import EditNoteForm from "../../../components/EditNoteForm.svelte";
import type { Note } from "../../../types/Note"
import AddProjectForm from "../../../components/AddProjectForm.svelte";


let add_task:boolean = false
let add_note:boolean = false
let edit_note:Note|null = null
let edit_task:Task|null = null
let add_project:boolean = false

export let data: {
    task_data : Task[],
    project_list : {[key:string]:string};
    note_data : Note[],
};


const update_task_data = async () => {
    let task_data = await fetch(`${$API_ENDPOINT}/calendar/task/${get_today_iso()}/${get_today_iso()}`, {
        credentials : 'include'
    })
    data.task_data = await task_data.json()   
}

const update_note_data = async () => {
    let note_data = await fetch(`${$API_ENDPOINT}/note/all`, {
        credentials : 'include'
    })
    data.note_data = await note_data.json()   
}
const mark_as_done = async (tid: string) => {
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
        data.task_data.filter((x)=>{return x.tid == tid})[0].status = TaskStatus.Finished
        data.task_data = data.task_data
    }
}

const delete_note = async (note_id : string) => {
    let resp = await fetch(`${$API_ENDPOINT}/note/remove/${note_id}`,{
        method: 'POST',
        credentials:'include',
    })
    if (resp.ok){
        data.note_data = data.note_data.filter((x)=>{return x.nid != note_id})
        data.note_data = data.note_data
    }
}
</script>

<style>
.task-container{
    padding: 16px;
}
.heading{
    font-size: min(9vw,32px);
    font-weight: 700;
    margin: 20px 8px;
}
.subheading{
    font-weight: 700;
    margin: 20px 0;
    margin-left: 28px;
    font-size: 24px; 
}
</style>