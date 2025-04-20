<span>
    <span class="label">{label}</span>
    <span class="input-wrapper">
        {#if type == 'email'}
            <input type="email" bind:this={input} bind:value={value} required {disabled}>
        {:else if type == 'text'}
            <input type="text" bind:this={input} bind:value={value} required {disabled}>
        {/if}
        <button on:click={helper}>{disabled ? "edit" : "check"}</button>
    </span>
</span>

<script lang="ts">
let disabled:boolean = true;
let input:HTMLInputElement;

export let type:string = 'text';
export let label:string;
export let value:string;
export let callback:VoidFunction;

const helper = () => {
    if (!input.reportValidity()) return
    if (!disabled) callback()
    disabled = !disabled
}

</script>

<style>
span.input-wrapper{
    display: flex;
    align-items: center;
}
span.label{
    margin:16px 8px;
    font-weight: 700;
    font-size: 20px;
}
input{
    background: var(--background-overlay);
    border: none;
    padding: 4px 8px;
    width: 100%;
    font-size: 20px;
    border-radius: 8px;
    font-family: 'Poppins';
    margin-bottom: 2px;
}
input:disabled{
    background-color: white;
    border-bottom: 2px var(--background) solid;
    margin-bottom: 0px;
    color: black;
}
button{
    background-color: var(--primary);
    border: none;
    height: 40px;
    margin-left: 8px;
    aspect-ratio: 1/1;
    border-radius: 10px;
    font-family: 'Material Symbols Outlined';
    font-size: 24px;
    color: var(--background);
}
</style>