<div class="header">
    Notifications
</div>
{#if data.notif_data.length === 0}
    <div class="heading">All notifications cleared!</div>
{/if}

<div class="card-grid-container">
    {#each data.notif_data as notification (notification.nid)}
    <div animate:flip={{duration : 200}}>
        <CardContainer 
        title={epoch_to_input(notification.date_added)}
        description={notification.content}
        btn_pri={"Delete"}
        btn_pri_icon={"delete"}
        btn_pri_callback={()=>delete_notification(notification.nid)}
        />
    </div>
    {/each}
</div>

<script lang="ts">
import { epoch_to_input } from "../../../store/utils";
import CardContainer from "../../../components/CardContainer.svelte";
import type { Notification } from "../../../types/Notification";
import { API_ENDPOINT } from "../../../store/store";
import { flip } from "svelte/animate";


const delete_notification = async (nid:string) => {
    let _resp = await fetch(`${$API_ENDPOINT}/notification/remove/${nid}`,{
        method:'POST',
        credentials:'include'
    })

    if (!_resp.ok){
        console.log(await _resp.text())
        return
    }

    data.notif_data = data.notif_data.filter((x)=>{return x.nid != nid})
}

export let data:{
    notif_data: Notification[]
};
</script>

<style>
.header{
    font-size: 28px;
    font-weight: 700;
    margin: 16px;
}
.heading{
    font-size: 24px;
    margin: 16px;
}
</style>