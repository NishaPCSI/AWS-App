<div class="heading">
    Settings
</div>
<div class="card-container flex-div wrap">
    <div class="avatar">
        <input class="avatar-input" type="file" bind:this={input_field} alt="upload avatar" id="avatar" name="file" accept=".png" on:change={submitPhoto}>
        <label for="avatar">
            {#if $USER_DATA.avatar}
                <img src={`${$API_ENDPOINT}/static/avatars/${$USER_DATA.uid}.png?${rng}`} alt="user avatar">
            {:else}
                <img src={`${$API_ENDPOINT}/static/avatars/account_circle.svg`} alt="user avatar">
            {/if}
        </label>
    </div>
    <div>
        <div class="meta">Logged in as</div>
        <div class="user">{$USER_DATA.fullname}</div>
    </div>
</div>
<div class="error">{avatar_error_text}</div>
<div class="card-container flex-div wrap dir-column">
    <EditableInputField label={"Name"} bind:value={$USER_DATA.fullname} callback={()=>send_update({fullname:$USER_DATA.fullname})}/>
    <EditableInputField label={"Email"} type={"email"} bind:value={$USER_DATA.email} callback={()=>{send_update({email:$USER_DATA.email})}}/>
    <EditableDateField label={"D.O.B"} bind:value={dob_middleman} callback={()=>{send_update({dob:input_to_epoch(dob_middleman)})}}/>
    <EditableInputField label={"Password"} bind:value={password_field} callback={async ()=>{send_update({password:await hash_password(password_field)})}}/>
    <ThemedButton --bgcolor="var(--primary)" --color="var(--background)" style={"width: min-content;padding: 0 16px;"} icon={"close"} callback={logout}>Logout</ThemedButton>
</div>



<div class="error">{error_text}</div>

<script lang="ts">
import { epoch_to_input, hash_password, input_to_epoch } from "../../../store/utils";
import EditableDateField from "../../../components/EditableDateField.svelte";
import EditableInputField from "../../../components/EditableInputField.svelte";
import ThemedButton from "../../../components/ThemedButton.svelte";
import { API_ENDPOINT,USER_DATA } from "../../../store/store";
import { goto } from "$app/navigation";


let input_field:HTMLInputElement;
let error_text:string = '';
let avatar_error_text:string = '';
let rng = Math.random()
let dob_middleman = epoch_to_input($USER_DATA.dob)
let password_field = '';

const submitPhoto = async () => {
    if (input_field.files === null || input_field.files.length === 0) return

    let form_data = new FormData()
    form_data.append('file', input_field.files[0])

    let _resp = await fetch(`${$API_ENDPOINT}/upload`, {
        method: 'POST',
        credentials:'include',
        body: form_data
    })
    
    avatar_error_text = ''
    
    if (!_resp.ok){
        avatar_error_text = await _resp.text()
        return
    }
    $USER_DATA.avatar = true
    rng = Math.random()
}

const logout = async () => {
    await fetch(`${$API_ENDPOINT}/user/logout`,{
        method:'POST',
        credentials:'include',
    })
    goto('/login')
}

const send_update = async (data:any) => {
    let _resp = await fetch(`${$API_ENDPOINT}/user/change`,{
        method:'POST',
        credentials:'include',
        headers:{
            'Content-Type' : 'application/json'
        },
        body:JSON.stringify({
            uid:$USER_DATA.uid,
            ...data
        })
    })
    if (!_resp.ok){
        error_text = JSON.stringify((await _resp.json())['detail'][0]['msg'])
        return
    }
    error_text = ''
}


</script>

<style>
.heading{
    font-weight: 700;
    font-size: 32px;
}
.card-container{
    background-color: var(--foreground);
    height: fit-content;
    border-radius: 16px;
    padding: 24px;
    gap: 32px;
    max-width: 800px;
    margin-bottom: 16px;
}
.avatar-input{
    display: none;
}
.avatar {
    max-width: 200px;
    width: 100%;
    overflow: hidden;
    border-radius: 100%;
}
.avatar label{
    display: block;
    position: relative;
    aspect-ratio: 1/1;
}
.avatar label:hover::after{
    content: 'edit';
    font-size: 32px;
    font-family: 'Material Symbols Outlined';
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background-color: #00000030;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    position: absolute;
    border-radius: 100px;
}
.avatar img {
    height: 100%;
    width: 100%;
    object-fit: cover;
}
.meta{
    font-size: 20px;
}
.user{
    font-size: 28px;
    font-weight: 700;
}
.error{
    color: red;
    font-weight: 700;
    margin: 8px;
}
</style>