export interface Project{
    pid : string
    name : string
    phase : ProjectPhase
    uid : string
    description : string
}

export enum Priority{
    Low = 0,
    Medium = 1,
    High = 2,
    Critical = 3
}

export enum ProjectPhase {
    Planning,
    Designing,
    Implementing,
    Testing,
    Deployed
}