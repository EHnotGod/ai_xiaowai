<template>
    <div style="height:4px" ></div>
    <div class="weather-content">
        <div class="weather-item">
            <div class="day-time">12/05</div>
            <div class="day-weather">
                <img class="weather-icon" src="@/assets/static/qing.png"></img>
                <p>晴</p>
            </div>
            <div class="temperature">12-18°C</div>
        </div>
    </div>
</template>

<script setup>

</script>

<style lang="less" scoped>
    .weather-content{
        background: linear-gradient(to bottom left,#2c305b,#6b6f91);
        color:#ffffff;
        border-radius: 4px;
        .weather-item{
            display: flex;
            align-items: center;
            justify-content: space-around;
            font-size: 15px;
            padding: 7px 0;
            .day-time{
                flex:1;
                text-align: center;
            }
            .day-weather{
                display: flex;
                flex:1;
                align-items:center;
                
                .weather-icon{
                    width:30px;
                    height: 30px;
                }
                p{
                    font-size: 15px;
                    padding-left: 10px;
                }
            }
            .temperature{
                flex:1;
                text-align: center;
            }
        }
    }
</style>

