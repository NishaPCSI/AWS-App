<div class="custom-select flex-div align-center">
    <span>{label} : </span>
    <select bind:value={value}>
        {#each Object.keys(options) as val }
            <option value={val}>{options[val]}</option>
        {/each}
    </select>
</div>

<script lang="ts">
export let label:string;
export let options:any;
export let value:string;
</script>

<style>
.custom-select{
    margin-top: 8px;
}
.custom-select span{
    margin: 0 8px;
    width: 50%;
}
select {
    padding: 0.5em 2em 0.5em 0.5em;
    border: none;
    width: 50%;
    font: inherit;
    line-height: inherit;
}
</style>