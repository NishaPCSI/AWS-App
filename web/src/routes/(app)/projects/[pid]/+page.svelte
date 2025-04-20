<div class="project-container">
    <div class="heading flex-div align-center">
        {data.project_data.project.name}
        {#if data.project_data.project.uid == $USER_DATA.uid}
            <FilledButton icon_left="edit" callback={()=>{edit_project = !edit_project}}>Edit</FilledButton>
        {/if}
    </div>

    <div class="sub-heading">
        {ProjectPhase[data.project_data.project.phase]}
    </div>
    <div class="project-description">
        {data.project_data.project.description}
    </div>
</div>

<div class="button-wrapper">
    <FilledButton icon_left="sticky_note_2" icon_right="add_circle" callback={()=>{add_task = !add_task}}>Task</FilledButton>
    {#if data.project_data.project.uid == $USER_DATA.uid}
        <FilledButton icon_left="sticky_note_2" icon_right="add_circle" callback={()=>{add_member = !add_member}}>Add Member</FilledButton>
    {/if}
    {#if data.project_data.project.uid == $USER_DATA.uid}
        <FilledButton icon_left="sticky_note_2" icon_right="do_not_disturb_on" callback={()=>{remove_member = !remove_member}}>Remove Member</FilledButton>
    {/if}
</div>

{#each Object.entries(data.project_data.tasks) as [username,tasks]}
    <div class="heading">
        {username}'s tasks
    </div>
    <div class="card-grid-container">
    {#each tasks as task}
        <CardContainer
            title={task.name} 
            status={TaskStatus[task.status]}
            priority={Priority[task.priority]}
            project={task.project?.name}
            description={task.description}
            deadline={task.deadline}
        />
    {/each}
    </div>
{/each}

{#if edit_project}
{@const project = data.project_data.project}
    <AbsoluteCenterWrapper --backdrop-filter="blur(8px)" >
        <EditProjectForm
            title_value={project.name}
            description_value={project.description}
            phase_value={project.phase.toString()}
            pid={project.pid}
            secondaryCallback={()=> {edit_project = false}}
            update_data={update_data}
        />
    </AbsoluteCenterWrapper>
{/if}
{#if add_task}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <AddTaskForm update_data={update_data} user_projects={_project_map} secondaryCallback={()=>{add_task = false}}/>
</AbsoluteCenterWrapper>
{/if}
{#if add_member}
<AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
    <div class="card-container flex-div dir-column">
        <ThemedInputText bind:value={add_member_input} placeholder={"Enter Email"} />
        <div class="button-wrapper flex-div align-center dir-row-reverse">
            <ThemedButton callback={add_member_to_project}>Add</ThemedButton>
            <ThemedButton callback={()=>{add_member_input='';add_member_list=[];add_member = false;error=''}}>Cancel</ThemedButton>
        </div>
        <div class="error">{error}</div>
    </div>
    {#each add_member_list as member (member.uid)}
        <button on:click={()=>{add_member_input = member.email}} animate:flip class="member-entry">{member.fullname} : {member.email}</button>
    {/each}
</AbsoluteCenterWrapper>
{/if}
{#if remove_member}
    <AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
        <div class="card-container flex-div dir-column">
            <ThemedInputText bind:value={remove_member_input} placeholder={"Enter Email"} />
            <div class="button-wrapper flex-div align-center dir-row-reverse">
                <ThemedButton callback={remove_member_from_project}>Remove</ThemedButton>
                <ThemedButton callback={()=>{remove_member_input='';remove_member = false;rem_error=''}}>Cancel</ThemedButton>
            </div>
            <div class="error">{rem_error}</div>
        </div>
        {#each filtered_member_list as member (member.uid)}
            <button on:click={()=>{remove_member_input = member.email}} animate:flip class="member-entry">{member.fullname} : {member.email}</button>
        {/each}
    </AbsoluteCenterWrapper>
{/if}

<script lang="ts">
import CardContainer from "../../../../components/CardContainer.svelte";
import { TaskStatus, type Task } from "../../../../types/Task";
import { Priority, ProjectPhase, type Project } from "../../../../types/Project";
import FilledButton from "../../../../components/FilledButton.svelte";
import EditProjectForm from "../../../../components/EditProjectForm.svelte";
import AbsoluteCenterWrapper from "../../../../components/AbsoluteCenterWrapper.svelte";
import { API_ENDPOINT, USER_DATA } from "../../../../store/store";
import AddTaskForm from "../../../../components/AddTaskForm.svelte";
import ThemedInputText from "../../../../components/ThemedInputText.svelte";
import ThemedButton from "../../../../components/ThemedButton.svelte";
import type { User } from "../../../../types/User";
import { flip } from "svelte/animate";


let edit_project:boolean = false;
let add_task:boolean = false;
let add_member:boolean = false;
let remove_member:boolean = false;
let add_member_input:string;
let remove_member_input:string = '';
let error:string = '';
let rem_error:string = '';

let add_member_list:User[] = [];
let filtered_member_list:User[] = [];

const update_member_list = async () => {
    if (add_member_input === undefined || add_member_input.trim() === '') return
    let resp = await fetch(`${$API_ENDPOINT}/user/email/${add_member_input}`,{
        credentials: 'include'
    })
    add_member_list =  await resp.json()
}

const add_member_to_project = async () => {
    if(add_member_input === undefined || add_member_input.trim() === '') return

    let resp = await fetch(`${$API_ENDPOINT}/project/adduser/${add_member_input}/${data.project_data.project.pid}`,{
        method:'POST',
        credentials: 'include'
    })
    if (resp.ok){
        add_member = false
        error = ''
    } else {
        error = await resp.text()
    }
    update_data()
}

const remove_member_from_project = async () => {

    if(remove_member_input === undefined || remove_member_input.trim() === '') return

    let resp = await fetch(`${$API_ENDPOINT}/project/removeuser/${remove_member_input}/${data.project_data.project.pid}`,{
        method:'POST',
        credentials: 'include'
    })
    if (resp.ok){
        remove_member = false
        rem_error = ''
    } else {
        rem_error = await resp.text()
    }
    update_data()
}

let myTimeout = setTimeout(update_member_list, 300);
$:add_member_input,(() => {
    clearTimeout(myTimeout)
    myTimeout = setTimeout(update_member_list, 300);
})()

const update_data = async () => {
    let project_data = await fetch(`${$API_ENDPOINT}/project/details/${data.project_data.project.pid}`, {
        credentials : 'include'
    })
    let existing_data = await fetch(`${$API_ENDPOINT}/project/members/${data.project_data.project.pid}`,{
        credentials:'include'
    })
    if(project_data.ok){
        data.existing_members = await existing_data.json(),
        data.project_data = await project_data.json()
    }
}

$:remove_member_input,(() => {
    filtered_member_list = data.existing_members.filter((x)=>{return x.email.includes(remove_member_input.trim())})
})()

export let data:{
    project_data:{
        project:Project;
        tasks:{[key:string]:Task[]}
    };
    existing_members:User[];
};

let _project_map:{[key:string]:string}={}
_project_map[data.project_data.project.pid] = data.project_data.project.name

</script>

<style>
.heading{
    font-weight: 700;
    font-size: 28px;
    text-transform: capitalize;
    margin: 8px 0;
    gap: 16px;
}
.sub-heading{
    font-weight: 700;
    font-size: 20px;
    color: var(--primary);
    margin: 8px 0;
}
.project-description{
    font-size: 18px;
    margin: 8px 0;
}
.card-container{
    background-color: var(--foreground);
    height: fit-content;
    border-radius: 16px;
    padding: 24px;
    gap: 16px;
    margin-bottom: 16px;
}
.button-wrapper{
    gap: 16px;
}
.member-entry{
    padding: 8px 16px;
    border-bottom: 1px var(--background) solid;
    background: #fff;
    border-radius: 16px;
    border: 1px var(--background-tinted) solid;
    font-family: inherit;
    font-size: 18px;
    text-align: left;
    margin-bottom: 8px;
    display: block;
    width: 100%;
}
.error{
    font-weight: 700;
    color: red;
}
</style>