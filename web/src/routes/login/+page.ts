import { API_ENDPOINT } from "../../store/store"
import { get } from "svelte/store"
import { error, redirect } from "@sveltejs/kit"
import type { PageLoad } from "./$types"

export const load:PageLoad = async ({ fetch }) => {
    let user_data = await fetch(`${get(API_ENDPOINT)}/user/me`, {
        credentials : 'include'
    })

    if (user_data.ok) {
        throw redirect(302, '/home')
    }
}