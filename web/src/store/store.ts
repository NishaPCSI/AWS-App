import type { User } from "../types/User"
import { writable, type Writable } from "svelte/store"

export const API_ENDPOINT = writable("http://13.218.46.83:8000")

export const USER_DATA:Writable<User> = writable()