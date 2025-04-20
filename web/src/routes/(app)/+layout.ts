import { redirect } from "@sveltejs/kit"
import { API_ENDPOINT, USER_DATA } from "../../store/store"
import { get } from "svelte/store"
import type { LayoutLoad } from "./$types"


export const load:LayoutLoad = async ({ fetch, url }) => {
    let user_data = await fetch(`${get(API_ENDPOINT)}/user/me`, {
        credentials : 'include'
    })
    if ([401,403].includes(user_data.status)) {
        throw redirect(302, '/login')
    }
    USER_DATA.set(await user_data.json())
    return {
        activeTab : url.pathname.split('/')[1]
    }
}