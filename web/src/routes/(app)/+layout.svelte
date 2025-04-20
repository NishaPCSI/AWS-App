<div class="base-grid-layout">
    <Header data={$USER_DATA} />
    <Sidebar activeTab={data.activeTab}/>
    <div class="padded-container">
        <slot></slot>
    </div>
    <ChatUi />
</div>

<style>
.base-grid-layout{
    display: grid;
    grid-template: "nav nav" min-content
                    "sidebar content" 1fr / 120px 1fr;

    min-height: 100vh;
}

.padded-container{
    padding: 0 32px;
    grid-area: content;
}
@media only screen and (max-width: 600px){
    .padded-container{
        padding: 0 8px;
    }
    .base-grid-layout{
        grid-template: "nav" min-content "content" 1fr "sidebar" 80px / 1fr;
    }
}
</style>

<script lang="ts">
import { USER_DATA } from "../../store/store";
import Header from "../../components/Header.svelte";
import Sidebar from "../../components/Sidebar.svelte";
import ChatUi from "../../components/ChatUI.svelte";

export let data:{
    activeTab : string,
};
</script>