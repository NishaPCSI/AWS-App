import { error } from "@sveltejs/kit"
import { API_ENDPOINT } from "../../../store/store"
import { get } from "svelte/store"
import type { PageLoad } from "./$types"

export const load:PageLoad = async ({ fetch, params}) => {
    let notif_data = await fetch(`${get(API_ENDPOINT)}/notification/all`, {
        credentials : 'include'
    })
    if(!notif_data.ok){
        throw error(500, 'Couldnt Fetch User Notifications')
    }
    return{
        notif_data: await notif_data.json()
    }
}