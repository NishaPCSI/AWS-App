<script lang="ts">
  import { API_ENDPOINT } from "../../store/store";
  import ThemedButton from "../../components/ThemedButton.svelte";
  import WavyBackground from "../../components/WavyBackground.svelte";
  import { hash_password } from "../../store/utils";
  import { goto } from "$app/navigation";

  let email_node: HTMLInputElement;
  let password_node: HTMLInputElement;
  let error_text = "";

  const login = async () => {
    let hashed_password = await hash_password(password_node.value);
    let resp = await fetch(`${$API_ENDPOINT}/user/login`, {
      credentials: "include",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email_node.value,
        password: hashed_password,
      }),
    });

    if (!resp.ok) {
      error_text = (await resp.json()).detail;
      return;
    }

    goto(`/home`);
  };
</script>

<WavyBackground />
<a href="/"><div class="main-logo"></div></a>
<div class="center-container">
  <form on:submit|preventDefault={login}>
    <div class="logo-full"></div>
    <label for="email">Email</label>
    <input
      bind:this={email_node}
      required
      type="email"
      name="email"
      id="email"
    />
    <label for="password">Password</label>
    <input
      required
      bind:this={password_node}
      type="password"
      name="password"
      id="password"
    />
    <div class="error">{error_text}</div>
    <ThemedButton
      type={"submit"}
      --bgcolor="var(--on-background)"
      --color="var(--background)">Login</ThemedButton
    >
    <a href="/register">create an account?</a>
  </form>
</div>

<style>
  .main-logo {
    height: 48px;
    display: block;
    width: 48px;
    background-image: url("/logo.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    margin: 32px;
    position: absolute;
    z-index: 1;
  }
  .center-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
  form {
    display: flex;
    flex-direction: column;
    max-width: 320px;
    width: 100%;
    gap: 8px;
    padding: 32px;
    background: var(--background-overlay);
    border-radius: 16px;
    backdrop-filter: blur(30px);
    box-shadow: 0 2px 8px #0003;
  }
  form input {
    font-family: "Poppins", sans-serif;
    background: var(--background-tinted);
    font-size: 16px;
    padding: 8px;
    border-radius: 8px;
    border: solid #0003 1px;
  }
  form a {
    text-align: center;
  }
  .logo-full {
    width: 100%;
    max-width: 200px;
    margin: 16px auto;
    height: 96px;
    background: url("https://group42-frontend.s3.us-east-1.amazonaws.com/logo-full.png")
      no-repeat center;
    background-size: contain;
  }
  .error {
    color: #ea3c3c;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.1px;
    line-height: 20px;
  }
</style>
