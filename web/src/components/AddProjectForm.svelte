<form bind:this={form_el} class="add-task">
    <ThemedInputText bind:value={title_value} placeholder={"Title"} />
    <ThemedTextArea bind:value={description_value} required={true} placeholder={"Description"}/>
    <ThemedDropDown bind:value={phase_value} label={"Project Phase"} options={filter_enum(ProjectPhase)}/>
    <div class="btn-wrapper flex-div dir-row-reverse">
        <ThemedButton type={"submit"} --bgcolor="var(--primary)" --color="var(--foreground)" callback={primaryCallback}>Add</ThemedButton>
        <ThemedButton --bgcolor="none" --color="var(--primary)" callback={secondaryCallback}>Cancel</ThemedButton>
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

export let secondaryCallback: VoidFunction;
export let update_data: VoidFunction;

let description_value:string;
let title_value:string;
let phase_value:string;
let form_el: HTMLFormElement;

const primaryCallback = async () => {
    if(!form_el.checkValidity()) return

    let resp = await fetch(`${get(API_ENDPOINT)}/project/add`, {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        credentials : 'include',
        body: JSON.stringify({
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