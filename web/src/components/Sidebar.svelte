<!-- SIDERAIL CONTAINER -->
<div class="siderail headline4">
    {#each Object.entries(tabArray) as [tab,label]}
        {@const low_label = label.toLowerCase()}
        <a href={`/${low_label}`} class="rail-item-wrapper">
            <div class:active={activeTab == low_label} class="rail-item material-symbols-outlined">{tab}</div>
            <div class="icon-label">{label}</div>
        </a>
    {/each}
</div>

<style>
.siderail{
    height: 100vh;
    padding: 0 12px;
    backdrop-filter: blur(8px);
    background-color: var(--primary-transparent);
    display: flex;
    flex-direction: column;
    text-align: center;
    position: fixed;
    justify-content: center;
    grid-column: nav-start;
    grid-row: nav-start / sidebar-end;
}
@media only screen and (max-width : 600px){
    .siderail{
        grid-area: sidebar;
        z-index: 1;
    }
}
.rail-item-wrapper{
    padding: 8px 0px;
    margin: 4px 0px;
}
.rail-item{
    max-width: 72px;
    width: 100%;
    font-size: min(5vw,28px);
}
.icon-label{
    height: 16px;
    font-size: min(3vw,14px);
    text-transform: capitalize;
    color: var(--on-background);
}
.siderail .rail-item{
    color: var(--on-background);
    padding: 6px 8px;
    border-radius: 100px;
}
.siderail .rail-item.active{
    color: var(--on-background);
    background-color: var(--primary);
    font-variation-settings: 'FILL' 1;
}
@media only screen and (max-width : 600px){
    .siderail{
        bottom: 0;
        flex-direction: row;
        width: 100%;
        height: min-content;
        border: none;
    }
    .rail-item-wrapper{
        flex-grow: 1;
    }
    .rail-item{
        height: min-content;
        align-self: center;
    }
}
</style>

<script lang="ts">
export let activeTab:string;
//  all the tabs with material icon and name go here
const tabArray = {
    "home" : "Home",
    "notifications" : "Notifications",
    "calendar_month" : "Calendar",
    "edit_square" : "Tasks",
    "assignment" : "Projects",
} 
</script>