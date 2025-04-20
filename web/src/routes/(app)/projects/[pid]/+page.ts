import { error } from "@sveltejs/kit"
import { API_ENDPOINT } from "../../../../store/store"
import { get } from "svelte/store"
import type { PageLoad } from "./$types"

export const load:PageLoad = async ({ fetch, params}) => {
    let project_data = await fetch(`${get(API_ENDPOINT)}/project/details/${params.pid}`, {
        credentials : 'include'
    })

    let existing_data = await fetch(`${get(API_ENDPOINT)}/project/members/${params.pid}`,{
        credentials:'include'
    })

    if(!project_data.ok || !existing_data.ok){
        throw error(500, 'Couldnt Fetch Project Details')
    }

    return{
        project_data : await project_data.json(),
        existing_members: await existing_data.json()
    }
}