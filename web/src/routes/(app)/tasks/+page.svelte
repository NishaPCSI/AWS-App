{#if Object.keys(data.task_data).length == 0}
    <div in:fade class="heading">Everything Done !!!</div>
{/if}
{#each Object.entries(data.task_data).sort() as [priority, tasks] (priority)}
<div class="heading">{Priority[Number(priority)]}</div>
    <div class="card-grid-container">
    {#each tasks as task (task.tid)}
        <div animate:flip={{duration:200}}>
            <CardContainer
                title={task.name} 
                status={TaskStatus[task.status]}
                priority={Priority[task.priority]}
                project={task.project?.name}
                description={task.description}
                deadline={task.deadline}
                btn_pri="Done"
                btn_pri_callback={() => {mark_as_done(task.tid,task.priority)}}
                btn_sec="Edit"
                btn_sec_callback={()=>{edit_task = task}}
                btn_pri_icon="check"
            />
        </div>
    {/each}
    </div>
{/each}
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
        update_data={update_data} 
        user_projects={{...{0:"None"},...data.project_list}} 
        secondaryCallback={()=>{edit_task = null}}
        />
</AbsoluteCenterWrapper>
{/if}

<script lang="ts">
import CardContainer from "../../../components/CardContainer.svelte";
import { TaskStatus, type Task } from "../../../types/Task";
import { Priority } from "../../../types/Project";
import AbsoluteCenterWrapper from "../../../components/AbsoluteCenterWrapper.svelte";
import EditTaskForm from "../../../components/EditTaskForm.svelte";
import { API_ENDPOINT } from "../../../store/store";
import { epoch_to_input, get_today_iso } from "../../../store/utils";
import { chunk_task_data_by_priority } from "../../../store/utils"
import { fade } from "svelte/transition";
import  { filter_task_data } from "./+page"
import { flip } from "svelte/animate";


let edit_task:Task|null = null;

const update_data = async () => {
    let task_data = await fetch(`${$API_ENDPOINT}/task/all`, {
        credentials : 'include'
    })
    data.task_data = filter_task_data(chunk_task_data_by_priority(await task_data.json()))
}


const mark_as_done = async (tid: string,priority:number) => {
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
        update_data()
    }
}

export let data:{
    activeTab:string,
    project_list: {[key:string]:string}
    task_data:{[key:string]:Task[]}
};
</script>

<style>
.heading{
    font-size: 28px;
    font-weight: 700;
    margin: 20px 0;
}
</style>