import { API_ENDPOINT } from "../../../store/store"
import { get } from "svelte/store"
import { error } from "@sveltejs/kit"
import type { Project } from "../../../types/Project";
import { chunk_task_data_by_deadline } from "../../../store/utils";
import type { PageLoad } from "./$types";

export const _getMonthCalendar = async (y:number,m:number,fetch:any = window.fetch) => {
    var firstDay = new Date(y, m, 1);
    var lastDay = new Date(y, m + 1,1);

    return await fetch(`${get(API_ENDPOINT)}/calendar/task/${firstDay.getTime()}/${lastDay.getTime()}`,{
        credentials: 'include'
    })
}


export const load:PageLoad = async ({ fetch }) => {
    let _date = new Date()
    let task_data = await _getMonthCalendar(_date.getFullYear(), _date.getMonth(),fetch)

    if (!task_data.ok){
        throw error(500, 'Couldnt Fetch Calendar Data')
    }

    let chunked_data = chunk_task_data_by_deadline(await task_data.json())

    let project_data = await fetch(`${get(API_ENDPOINT)}/project/all`, {
        credentials : 'include'
    })
    
    if (!project_data.ok){
        throw error(500, 'Couldnt Fetch User Projects')
    }
    let _pd: Project[] = await project_data.json()
    
    let project_list: { [key:string]: string} = {} 
    _pd.forEach( x =>{
        project_list[x.pid] = x.name
    }) 
    return {
        task_data : chunked_data,
        project_list : project_list,
    }
}
