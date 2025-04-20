import { API_ENDPOINT } from "../../../store/store"
import { get } from "svelte/store"
import { error } from "@sveltejs/kit"
import { get_today_iso, project_list_by_id } from "../../../store/utils"
import { chunk_task_data_by_priority } from "../../../store/utils"
import {TaskStatus, type Task } from "../../../types/Task"
import type { PageLoad } from "./$types"

export const filter_task_data = (_mid:{[key: string]: Task[]}) => {
    let _fin:{[key: string]: Task[]} = {};

    Object.entries(_mid).forEach(([x,y],_) => {
        let __task_list = y.filter(x=>x.status != TaskStatus.Finished)
        if (__task_list.length != 0) _fin[x] =__task_list
    })
    return _fin
}

export const load:PageLoad = async ({ fetch }) => {
    let task_data = await fetch(`${get(API_ENDPOINT)}/task/all`, {
        credentials : 'include'
    })
    if (!task_data.ok){
        throw error(500, 'Couldnt Fetch User Tasks')
    }
    let project_data = await fetch(`${get(API_ENDPOINT)}/project/all`, {
        credentials : 'include'
    })
    if(!project_data.ok){
        throw error(500, 'Couldnt Fetch User Projects')
    }
    return{
        task_data: filter_task_data(chunk_task_data_by_priority(await task_data.json())),
        project_data : project_list_by_id(await project_data.json())
    }

}
