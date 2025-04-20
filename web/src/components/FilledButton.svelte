<button on:click={callback}>
    <span class="material-symbols-outlined">{icon_left}</span>
        <slot></slot>
    <span class="material-symbols-outlined">{icon_right}</span>
</button>

<script lang="ts">
export let callback:VoidFunction = () => {}
export let icon_left: string = "";
export let icon_right: string = "";
</script>

<style>
button{
    display: inline-flex;
    justify-content: space-between;
    align-items: center;
    color: var(--background);
    background: var(--primary);
    border: 0;
    cursor: pointer;
    border-radius: 30px;
    min-height: 40px;
    min-width: 150px;
    font-size: 16px;
    font-weight: 700;
    font-family: inherit;
    margin: 16px 0px;
    margin-right: 16px;
    gap: 8px;
    padding: 0 8px;
}
</style>
