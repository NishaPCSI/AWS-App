import type { Project } from "./Project"

export interface Task{
    name : string
    description : string|null
    deadline : number 
    priority : number
    status : TaskStatus
    pid : string|null
    notify : boolean
    tid: string,
    project : Project|null
}

export enum TaskStatus{
    NotTouched,
    Working,
    Finished,
    Halted
}