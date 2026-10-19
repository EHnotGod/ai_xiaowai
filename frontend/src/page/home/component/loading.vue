<template>
    <div class="circle-container">
        <span class="circle"></span>
        <span class="circle"></span>
        <span class="circle"></span>
    </div>
</template>

<script setup>

</script>

<style lang="less" scoped>
    .circle-container{
        display:flex;
        align-items: center;
        .circle {
            width:7px;
            height:7px;
            border-radius: 50px;
            background-color: #3b24a0;
            margin:0 4px;
            animation: colohange 1s linear infinite;
        }
        .circle:nth-child(1){
            animation-delay:0s;
        }
        .circle:nth-child(2){
            animation-delay:0.33s;
        }
        .circle:nth-child(3){
            animation-delay:0.67s;
        }
    }
    @keyframes colohange {
            0% {
                background-color: #92abe4;
            }
            33.33% {
                background-color: #92abe4;
            }
            66.67% {
                background-color: #92abe4;
            }
            
        }
</style>

