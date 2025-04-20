<button {style} class="material-symbols-outlined" on:click={on_click}>
    <slot></slot>
</button>

<script lang="ts">
export let on_click:VoidFunction;
export let style:string|undefined;
</script>

<style>
button{
    border:none;
    background-color: transparent;
}
</style>