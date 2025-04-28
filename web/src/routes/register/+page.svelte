<script lang="ts">
  import { API_ENDPOINT } from "../../store/store";
  import { hash_password } from "../../store/utils";
  import ThemedButton from "../../components/ThemedButton.svelte";
  import WavyBackground from "../../components/WavyBackground.svelte";
  import { goto } from "$app/navigation";

  let full_name_node: HTMLInputElement;
  let email_node: HTMLInputElement;
  let dob_node: HTMLInputElement;
  let password_node: HTMLInputElement;
  let confirm_password_node: HTMLInputElement;
  let error_text = "";

  const register = async () => {
    let hashed_password1 = await hash_password(password_node.value);
    let hashed_password2 = await hash_password(confirm_password_node.value);

    if (hashed_password1 !== hashed_password2) {
      error_text = "Passwords Do Not Match";
      return;
    } else {
      error_text = "";
    }

    let resp = await fetch(`${$API_ENDPOINT}/user/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email_node.value,
        password: hashed_password1,
        fullname: full_name_node.value,
        dob: dob_node.valueAsNumber,
      }),
    });

    if (!resp.ok) {
      error_text = (await resp.json()).detail;
      return;
    }

    goto(`/login`);
  };
</script>

<WavyBackground />
<a href="/"><div class="main-logo"></div></a>
<div class="center-container">
  <form on:submit|preventDefault={register}>
    <div class="logo-full"></div>

    <label for="full_name">Full Name</label>
    <input
      bind:this={full_name_node}
      required
      type="text"
      name="full_name"
      id="full_name"
    />

    <label for="email">Email</label>
    <input
      bind:this={email_node}
      required
      type="email"
      name="email"
      id="email"
    />

    <label for="dob">Date of Birth</label>
    <input bind:this={dob_node} required type="date" name="dob" id="dob" />

    <label for="password">Password</label>
    <input
      required
      bind:this={password_node}
      type="password"
      name="password"
      id="password"
    />

    <label for="confirm_password">Confirm Password</label>
    <input
      required
      bind:this={confirm_password_node}
      type="password"
      name="confirm_password"
      id="confirm_password"
    />

    <div class="error">{error_text}</div>
    <ThemedButton
      type={"submit"}
      --bgcolor="var(--on-background)"
      --color="var(--background)">Register</ThemedButton
    >
    <a href="/login">already have an account?</a>
  </form>
</div>

<style>
  .main-logo {
    height: 48px;
    display: block;
    width: 48px;
    background-image: url("https://group42-frontend.s3.us-east-1.amazonaws.com/logo.png");
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
    max-width: 360px;
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
