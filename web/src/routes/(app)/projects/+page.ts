import { error } from "@sveltejs/kit"
import { API_ENDPOINT } from "../../../store/store"
import { get } from "svelte/store"
import type { PageLoad } from "./$types"

export const load:PageLoad = async ({ fetch }) => {
    let project_data = await fetch(`${get(API_ENDPOINT)}/project/all`, {
        credentials : 'include'
    })
    if(!project_data.ok){
        throw error(500, 'Couldnt Fetch User Projects')
    }
    return{
        project_data : await project_data.json()
    }
}