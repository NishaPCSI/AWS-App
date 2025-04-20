<span data-icon={icon}>
    <textarea bind:value={value} {required} rows="5" placeholder={placeholder}></textarea>
</span>

<script lang="ts">
export let placeholder:string;
export let icon: string = '';
export let value:string;
export let required:boolean = false;
</script>

<style>
textarea{
    background: var(--background-overlay);
    border: none;
    width: 100%;
    padding: 4px 8px;
    font-size: 20px;
    margin-top: 8px;
    border-radius: 8px;
    font-family: 'Poppins';
    resize: none;
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