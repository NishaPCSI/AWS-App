<div class="header flex-div align-center">
    Projects
    <FilledButton icon_left="add_circle" callback={()=>{add_project = !add_project}}>Add</FilledButton>
</div>

{#each data.project_data as project}
    <div class="card-container flex-div dir-column">
        <div class="name">{project.name}</div>
        <div class="phase">{ProjectPhase[project.phase]}</div>
        <div class="description">{project.description}</div>
        <div class="button-wrapper flex-div dir-row-reverse">
            <ThemedButton href={`/projects/${project.pid}`}>View</ThemedButton>
        </div>
    </div>
{/each}
{#if add_project}
    <AbsoluteCenterWrapper --backdrop-filter="blur(8px)">
        <AddProjectForm
            update_data={update_data}
            secondaryCallback={()=> {add_project = false}}
        />
    </AbsoluteCenterWrapper>
{/if}


<script lang="ts">
import { API_ENDPOINT } from "../../../store/store";
import AbsoluteCenterWrapper from "../../../components/AbsoluteCenterWrapper.svelte";
import AddProjectForm from "../../../components/AddProjectForm.svelte";
import FilledButton from "../../../components/FilledButton.svelte";
import ThemedButton from "../../../components/ThemedButton.svelte";
import { type Project, ProjectPhase} from "../../../types/Project";


let add_project:boolean = false;

export let data:{
    project_data:Project[]
};

const update_data = async () => {
    let project_data = await fetch(`${$API_ENDPOINT}/project/all`, {
        credentials : 'include'
    })
    data.project_data = await project_data.json()
}

</script>

<style>
.card-container{
    background-color: var(--foreground);
    height: fit-content;
    min-height: 288px;
    border-radius: 16px;
    padding: 24px;
    gap: 8px;
    max-width: 700px;
    margin-bottom: 16px;
}
.name{
    font-weight: 700;
}
.button-wrapper{
    margin-top: auto;
}
.header{
    font-size: 28px;
    font-weight: 700;
    margin: 16px;
    gap: 16px;
}

</style>