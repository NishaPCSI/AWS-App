<form bind:this={form_el} class="add-task">
    <ThemedInputText bind:value={title_value} placeholder={"Title"} />
    <ThemedDateInput bind:value={date_value} placeholder={"Deadline"} />
    <ThemedTextArea bind:value={description_value} placeholder={"Description"}/>
    <ThemedDropDown bind:value={priority_value} label={"Task Priority"} options={filter_enum(Priority)}/>
    <ThemedDropDown bind:value={phase_value} label={"Phase"} options={filter_enum(TaskStatus)}/>
    <ThemedDropDown bind:value={link_value} label={"Linked Project"} options={user_projects}/>
    <div class="btn-wrapper flex-div dir-row-reverse">
        <ThemedButton type={"submit"} --bgcolor="var(--primary)" --color="var(--foreground)" callback={primaryCallback}>Update</ThemedButton>
        <ThemedButton --bgcolor="none" --color="var(--primary)" callback={secondaryCallback}>Cancel</ThemedButton>
        <IconButton style="margin-right:auto" on_click={delete_task}>delete</IconButton>
    </div>
</form>

<script lang="ts">
import ThemedButton from "./ThemedButton.svelte";
import ThemedTextArea from "./ThemedTextArea.svelte";
import ThemedDropDown from "./ThemedDropDown.svelte";
import { Priority } from "../types/Project";
import ThemedInputText from "./ThemedInputText.svelte";
import ThemedDateInput from "./ThemedDateInput.svelte";
import { API_ENDPOINT } from "../store/store";
import { get } from "svelte/store";
import { TaskStatus } from "../types/Task";
import { filter_enum, input_to_epoch } from "../store/utils";
import IconButton from "./IconButton.svelte";

export let secondaryCallback: VoidFunction;
export let user_projects: {[key:string]:string};
export let update_data: VoidFunction;

export let description_value:string;
export let title_value:string;
export let priority_value:string;
export let phase_value:string;
export let link_value:string;
export let date_value:string;
export let tid_value:string;

let form_el: HTMLFormElement;

const primaryCallback = async () => {
    if(!form_el.checkValidity()) return
    
    let resp = await fetch(`${get(API_ENDPOINT)}/task/change`, {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        credentials : 'include',
        body: JSON.stringify({
            tid:tid_value,
            name:title_value,
            description:description_value,
            deadline: input_to_epoch(date_value),
            priority:Number(priority_value),
            status:Number(phase_value),
            pid:(link_value === "0") ? null : link_value,
            notify:false,
        })
    })
    if (resp.ok){
        secondaryCallback()
        update_data()
    }
}

const delete_task = async () => {
    let resp = await fetch(`${get(API_ENDPOINT)}/task/remove/${tid_value}`, {
        method: 'POST',
        credentials : 'include',
    })
    if (resp.ok){
        secondaryCallback()
        update_data()
    }
}

</script>

<style>
.add-task{
    max-width: 450px;
    border-radius: 16px;
    background-color: #fff;
    padding: 16px;
}
.btn-wrapper{
    margin-top: 16px;
}
</style>