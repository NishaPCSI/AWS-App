<nav>
    <a class="unselectable" href="/">
        <img class="header-logo unselectable" src="/logo-abbr.png" alt="App Logo">
    </a>
    <a href="/account" class="account-anc unselectable flex-div align-center">
        <span>{data.fullname}</span>
        <span class="material-symbols-outlined account">account_circle</span>
    </a>
</nav>

<script lang="ts">
import type { User } from "../types/User";
export let data:User;
</script>

<style>
nav{
    display: flex;
    height: 64px;
    align-items: center;
    padding: 18px;
    background: #fffa;
    grid-area: nav;
    margin: 16px 0;
    z-index: 1;
    position: relative;
}

nav a{
    display: flex;
}
.header-logo{
    width: 72px;
}
.account-anc {
    margin-left: auto;
    gap: 8px;
    font-weight: 700;
    font-size: min(3vw,14px);
    text-align: right;
}
.account{
    font-size: 48px;
    font-variation-settings:
        'FILL' 1,
        'wght' 300,
        'GRAD' 0,
        'opsz' 0;
    color: var(--on-background);
}
</style>