<form bind:this={form_el} class="add-task">
    <ThemedInputText bind:value={title_value} placeholder={"Title"} />
    <ThemedTextArea bind:value={description_value} required={true} placeholder={"Description"}/>
    <ThemedDropDown bind:value={phase_value} label={"Project Phase"} options={filter_enum(ProjectPhase)}/>
    <div class="btn-wrapper flex-div dir-row-reverse">
        <ThemedButton type={"submit"} --bgcolor="var(--primary)" --color="var(--foreground)" callback={primaryCallback}>Update</ThemedButton>
        <ThemedButton --bgcolor="none" --color="var(--primary)" callback={secondaryCallback}>Cancel</ThemedButton>
        <IconButton style={"margin-right:auto;"} on_click={delete_project}>delete</IconButton>
    </div>

</form>

<script lang="ts">
import ThemedButton from "./ThemedButton.svelte";
import ThemedTextArea from "./ThemedTextArea.svelte";
import ThemedDropDown from "./ThemedDropDown.svelte";
import { ProjectPhase } from "../types/Project";
import ThemedInputText from "./ThemedInputText.svelte";
import { API_ENDPOINT } from "../store/store";
import { get } from "svelte/store";
import { filter_enum } from "../store/utils";
import { goto } from "$app/navigation";
import IconButton from "./IconButton.svelte";


export let secondaryCallback: VoidFunction;
export let update_data: VoidFunction;

export let description_value:string;
export let title_value:string;
export let phase_value:string;
export let pid:string;
let form_el: HTMLFormElement;

const primaryCallback = async () => {
    if(!form_el.checkValidity()) return

    let resp = await fetch(`${get(API_ENDPOINT)}/project/change`, {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        credentials : 'include',
        body: JSON.stringify({
            pid:pid,
            name:title_value,
            description:description_value,
            phase:Number(phase_value),
        })
    })
    if (resp.ok){
        secondaryCallback()
        update_data()
    }
}

const delete_project = async () => {
    let _resp = await fetch(`${$API_ENDPOINT}/project/remove/${pid}`,{
        method:'POST',
        credentials: 'include'
    })
    if (_resp.ok) goto('/projects')
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