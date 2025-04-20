<div class="wavybackground">
    <div class="shape-container"></div>
</div>

<style>
.wavybackground{
    z-index: -1;
    background: var(--background);
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
}

.shape-container{
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: url('/bgshape.svg');
    animation: flow 15s infinite;
}

@keyframes flow{
    0%,100%{
        background-position: center;
        background-size: 220vh;
    }
    33%{
        background-position: center left;
        background-size: 280vh;
    }

    66%{
        background-position: center right;
        background-size: 280vh;
    }
}
</style>