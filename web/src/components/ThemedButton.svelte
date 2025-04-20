<button {style} {type} on:click={callback} on:submit|preventDefault={callback}>
    {#if href !== undefined}
    <a href={href}>
        {#if icon !== undefined}
            <span class="material-symbols-outlined">{icon}</span>
        {/if}
        <slot></slot>
    </a>
    {:else}
        {#if icon !== undefined}
            <span class="material-symbols-outlined">{icon}</span>
        {/if}
        <slot></slot>
    {/if}
</button>

<script lang="ts">
export let callback:VoidFunction = () => {}
export let icon: string|undefined = undefined;
export let href:string|undefined = undefined;
export let type:string = "button"
export let style:string|null = null;
</script>

<style>
button{
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--color,var(--on-background));
    background: var(--bgcolor,var(--background));
    border: 0;
    cursor: pointer;
    border-radius: var(--border-radius, 8px);
    min-height: 40px;
    min-width: 96px;
    font-size: 16px;
    font-family: inherit;
    margin: var(--margin);
    gap: 8px;
}
a{
    flex:1 0 0;
    display: flex;
    height: 100%;
    width:100%;
    align-items: center;
    justify-content: center;
    transition: 0.25s ease;
}
button:hover{
    box-shadow: 0px 2px 8px #0003;
}
</style>
