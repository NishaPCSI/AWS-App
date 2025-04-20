<div out:fade class="absolute-wrapper">
    <span in:fly={{x:-300}} out:fly={{x:300}}>
        <slot></slot>
    </span>
</div>

<script lang="ts">
import { fade, fly } from "svelte/transition";
</script>

<style>
.absolute-wrapper{
    position: fixed;
    top: 0;
    display: flex;
    left: 0;
    width: 100%;
    height: 100%;
    align-items: center;
    justify-content: center;
    backdrop-filter: var(--backdrop-filter);
}
:global(.absolute-wrapper > span > *){
    box-shadow: 2px 2px 10px #515151bd;
    border-radius: 16px;
}
</style>