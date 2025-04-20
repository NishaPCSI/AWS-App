<WavyBackground --background="linear-gradient(#3ac4b5,#40a4b0)" />
<div class="main-logo"></div>
<main class="content">
    <h1>Task<br>Planner</h1>
    <div class="text">
        now complete your task<br>
        more efficiently!
    </div>
        <div class="btn-wrapper flex-div wrap just-center">
            <ThemedButton
                href={"/login"} 
                --border-radius="32px" 
                --margin="8px">
                Login
            </ThemedButton>
            <ThemedButton 
                href="/register"
                --border-radius="32px" 
                --margin="8px" 
                --color=var(--background) 
                --bgcolor="var(--on-background)">
                Register
            </ThemedButton>
    </div>
</main>

<script lang="ts">
import ThemedButton from "../components/ThemedButton.svelte";
import WavyBackground from "../components/WavyBackground.svelte";
</script>

<style>
.text{
    color: var(--background);
}
.btn-wrapper{
    width:fit-content;
}
.main-logo{
    height: 48px;
    width: 48px;
    background-image: url("/logo.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    margin: 32px;
}
.content{
    bottom: 0;
    position: absolute;
    font-size: min(3em, 7vw);
    padding :15vh min(64px,6vw)
}
</style>