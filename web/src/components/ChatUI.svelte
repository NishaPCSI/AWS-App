<div use:accordion={isOpen} class="chat-ui">
    <div class="flex-div" transition:fade>
        <button class="open-button main" on:click={()=>{isOpen = !isOpen}}>contact_support</button>
        {#if isOpen}
            <button class="open-button right" on:click={()=>{isOpen = !isOpen}}>close</button>
        {/if}
    </div>
    {#if isOpen}
    <div class="chat-content" transition:fade>
        <div class="answer-block">
            <!-- <div class="msg-sent">
                {question}
            </div> -->
            <div class="msg-recieved">
                {@html qaMap[question]}
            </div>
        </div>
        <div class="buttoncontainer">
            {#each Object.keys(qaMap) as text}
                <button class="send-message" on:click={()=>{question=text}}>
                    {text}
                </button>
            {/each}
        </div>
    </div>
    {/if}
</div>

<script lang="ts">
import { fade } from "svelte/transition";
import { USER_DATA } from "../store/store";

let question = 'Hi'

let isOpen:boolean = false;

const qaMap:{[key:string] : string} = {
    'Hi' : `Hello ${$USER_DATA.fullname}, how can we help you today?`,
    'How to add a new project?' : "You can click on Project Tab & click the add button to make a new project.",
    'How to add a new task?' : "You can click on Tasks Tab & click the add button to make a new task.",
    'How to add a member in a project?' : "Open the project you want & click the add member button.",
    'What happens to tasks of a user after they are removed from a project' : "All the tasks related to that user gets deleted.",
    'How does a user know if they are added/removed to/from a project' : 'The added user gets notified, that they got added into the project.',
    'Need more help' : 'contact us by emailing at <a style="text-decoration:underline;" href="mailto:help@example.com">help@example.com</a>'
}

const accordion = (node:HTMLDivElement, isOpen:boolean) => {
    let initialHeight = '54px';
    let initialWidth = '54px';
    node.style.height = isOpen ? '100%' : initialHeight;
    node.style.width = isOpen ? '100%' : initialWidth;
    node.style.overflow = "hidden";
    return {
        update(isOpen:boolean) {
            let animation = node.animate(
                [
                    {
                        width: '100%',
                        height: '100%',
                        overflow: 'hidden',
                        padding:'16px',
                    },
                    {
                        width: initialWidth,
                        height: initialHeight,
                        overflow: 'hidden',
                        padding: '0px',
                    },
                ],
                { duration: 250, fill: 'both', easing:'ease-out' }
            );
            animation.pause();
            if (!isOpen) {
                animation.play();
            } else {
                animation.reverse();
            }
        }
    };
}
</script>

<style>
.chat-ui{
    width: 100%;
    height: 100%;
    max-width: 500px;
    max-height: 700px;
    position: fixed;
    bottom: 32px;
    right: 32px;
    overflow-x: hidden;
    overflow-x: auto;
    box-shadow: 0px 2px 8px #0003;
    background-color: white;
    border-radius: 32px;
    z-index: 1;
}
@media only screen and (max-width:600px){
    .chat-ui{
        bottom: 92px;
        right: 0;
    }
}
.chat-content{
    background-color: white;
    display: flex;
    flex-direction: column;
    padding: 8px;
    height: 100%;
}
.answer-block{
    margin-bottom: 16px;
    margin-right: 64px;
}
.msg-recieved{
    background: var(--background);
    border-radius: 24px;
    padding: 16px;
    height: 100%;
    margin-bottom: auto;
}
/* .msg-sent{
    text-align: right;
} */
.buttoncontainer {
    display: flex;
    flex-direction: column;
    margin-bottom: 36px;
    align-items: flex-end;
    margin-top: auto;
}
.send-message{
    text-align: right;
    color: var(--background);
    background: var(--primary);
    border: 0;
    cursor: pointer;
    border-radius: 16px;
    min-height: 48px;
    font-size: 16px;
    font-weight: 700;
    font-family: inherit;
    margin-bottom: 16px;
    padding: 8px 16px;
}
.open-button{
    font-family: 'Material Symbols Outlined';
    font-size: 28px;
    height: 54px;
    width: 54px;
    border-radius: 100px;
    flex-shrink: 0;
    background:none;
    border: none;
}
.open-button.right{
    margin-left: auto;
}
.open-button.main{
    font-size: 32px;
    color: var(--primary);
}
</style>