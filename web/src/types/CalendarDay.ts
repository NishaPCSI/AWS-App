import type { Task } from "./Task";

export interface CalendarDay {
    name: string,
    enabled: boolean,
    date:Date,
    tasks:Task[]
}