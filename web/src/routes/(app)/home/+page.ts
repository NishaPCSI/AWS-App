import { API_ENDPOINT } from "../../../store/store"
import { get } from "svelte/store"
import { error, redirect } from "@sveltejs/kit"
import type { Project } from "../../../types/Project"
import { get_today_iso, project_list_by_id } from "../../../store/utils"
import type { PageLoad } from "./$types"

export const load:PageLoad = async ({ fetch }) => {
    let project_data = await fetch(`${get(API_ENDPOINT)}/project/all`, {
        credentials : 'include'
    })
    let task_data = await fetch(`${get(API_ENDPOINT)}/calendar/task/${get_today_iso()}/${get_today_iso()}`, {
        credentials : 'include'
    })
    let note_data = await fetch(`${get(API_ENDPOINT)}/note/all`, {
        credentials : 'include'
    })
    if (!task_data.ok){
        throw error(500, 'Couldnt Fetch User Tasks')
    }
    if (!project_data.ok){
        throw error(500, 'Couldnt Fetch User Projects')
    }
    if (!note_data.ok){
        throw error(500, 'Couldnt Fetch User Notes')
    }

    return {
        task_data : await task_data.json(),
        project_list : project_list_by_id(await project_data.json()),
        note_data : await note_data.json()
    }
}
