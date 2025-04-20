import type { User } from "../types/User"
import { writable, type Writable } from "svelte/store"

export const API_ENDPOINT = writable("http://127.0.0.1:8000")

export const USER_DATA:Writable<User> = writable()