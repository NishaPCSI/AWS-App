<div {id} transition:fly|local={{x:-200}} class="cardcontainer flex-div dir-column">
    <div>
        {#if title}
            <div class="title">
                <span>{title}</span>
                {#if priority}
                    <span class="pri-icon">{@html get_priority_svg[priority]}</span>
                {/if}
            </div>
        {/if}
        {#if status}
            <div class="subtitle">{status}</div> 
        {/if}
        {#if priority}
            <div class="subtitle">{priority}</div>
        {/if}
        {#if project}
            <div class="project flex-div align-center">
                {project} 
                <span class="material-symbols-outlined">link</span>
            </div>
        {/if}
        {#if deadline !== null}
            <div> <span class="subtitle"> deadline : </span> {epoch_to_input(deadline)}</div>
        {/if}
    </div>
    {#if description}
        <div>{description}</div>
    {/if}
    <div class="btn-wrapper flex-div dir-row-reverse">
        {#if btn_pri_callback !== undefined}
            <ThemedButton --bgcolor="var(--primary)" --color="var(--background)" --border-radius="100px" callback={btn_pri_callback} icon={btn_pri_icon}>
                {btn_pri}
            </ThemedButton>
        {/if}
        {#if btn_sec_callback !== undefined}
        <ThemedButton --bgcolor="none" --color="var(--primary)" --border-radius="100px" callback={btn_sec_callback}>
            {btn_sec}
        </ThemedButton>
        {/if}
    </div>
</div>

<script lang="ts">
import { fly } from "svelte/transition";
import ThemedButton from "./ThemedButton.svelte";
import { epoch_to_input, get_priority_svg, input_to_epoch } from "../store/utils"
export let title:string|null = null;
export let status:string|null = null;
export let priority:string|null = null;
export let project: string|null = null;
export let description: string|null = null;
export let id:string|null = null;
export let deadline: number|null = null;

export let btn_pri:string|undefined = undefined;
export let btn_pri_icon:string|undefined = undefined;
export let btn_pri_callback: VoidFunction|undefined = undefined;

export let btn_sec:string|undefined = undefined;
export let btn_sec_callback: VoidFunction|undefined = undefined;

</script>

<style>
.cardcontainer{
    background-color: var(--foreground);
    height: fit-content;
    min-height: 288px;
    border-radius: 16px;
    padding: 24px;
    gap: 8px;
}

.title{
    font-weight: 700;
    display: flex;
}
.pri-icon{
    margin-left: auto;
    width: 18px;
}
.subtitle{
    color: var(--primary);
    font-weight: 700;
}
.btn-wrapper{
    margin-top: auto;
    flex-wrap: wrap;
}
.project{
    font-weight: 700;
    color: var(--background-overlay-inverse);
    gap: 4px;
}
</style>