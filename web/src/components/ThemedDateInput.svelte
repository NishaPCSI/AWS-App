<span data-icon={icon}>
    <input required type="date" bind:value={value} placeholder={placeholder}>
</span>

<script lang="ts">
export let placeholder:string;
export let value: string;
export let icon: string = '';
</script>

<style>
input:invalid{
    color: #777;
}
input{
    background: var(--background-overlay);
    border: none;
    width: 100%;
    padding: 4px 8px;
    font-size: 20px;
    margin-top: 8px;
    border-radius: 8px;
    font-family: 'Poppins';
}
span{
    position: relative;
}
span::after{
    content: attr(data-icon);
    position: absolute;
    height: 100%;
    aspect-ratio: 1/1;
    font-family: 'Material Symbols Outlined';
    right: 8px;
    font-size: 24px;
    line-height: 38px;
}
</style>