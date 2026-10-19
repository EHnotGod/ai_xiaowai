<template>
    <div class="map-container">
        <div>
      <img src="https://s2.loli.net/2024/11/30/c3BuMjGf7FeCxo8.jpg" style="height: 680px; width: auto;" />
      
      <!-- 浮标点 -->
      <div
        v-for="(marker, index) in markers"
        :key="index"
        class="marker"
        :style="{ left: marker.x + 'px', top: marker.y + 'px' }"
        @click="openDialog(marker)"
      >
        <el-tooltip
            :content= "`<img style='height:100px' src=${marker.image} />`"
            raw-content
            placement="top"
            effect="light"
        >
            <el-link type="primary" :underline="false">
                <el-icon color="red" size="30px"><Location /></el-icon>
            </el-link>
        </el-tooltip>

      </div>
  
      <!-- 大图对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="selectedMarker.title"
        width="600px"
      >
        <img :src="selectedMarker.image" style="width: 100%;" />
      </el-dialog>
    </div>
    <div class="youce">
      <div style="display: flex;">
      <h1>查看3D世界</h1>
      <h5 style="padding-top: 20px;padding-left: 20px;">点击右上角可全屏</h5>
    </div>
    <div class="panorama-container">
        <iframe 
            src="https://www.720yun.com/vr/36ajz7mv5y1" 
            width="100%" 
            height="500px" 
            frameborder="0" 
            allowfullscreen>
        </iframe>
    </div>
</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { Location} from '@element-plus/icons-vue'
  // 浮标点数据
  const markers = ref([
    { x: 500, y: 185, title: '电子楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c02383bca.jpg'},
    { x: 580, y: 450, title: '海洋学院', image:'https://www.helloimg.com/i/2025/02/05/67a2c02396242.jpg'},
    { x: 430, y: 530, title: '湖西楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c022721fe.jpg'},
    { x: 690, y: 500, title: '北衡楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c022e173c.jpg'},

    { x: 440, y: 180, title: '体育场', image:'https://www.helloimg.com/i/2025/02/05/67a2c2a4d7d21.jpg'},
    { x: 580, y: 300, title: '图东环楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c2a543ac9.jpg'},
    { x: 220, y: 345, title: '泰园', image:'https://www.helloimg.com/i/2025/02/05/67a2c2a65314c.jpg'},
    { x: 720, y: 535, title: '南辰楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c2a6ae423.jpg'},

    { x: 430, y: 105, title: '闻天楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c3f949679.jpg'},
    { x: 520, y: 280, title: '图书馆', image:'https://www.helloimg.com/i/2025/02/05/67a2c3f9ac20a.jpg'},
    { x: 460, y: 300, title: '图西环楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c3fa270f7.jpg'},
    { x: 610, y: 180, title: '文学楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c3fab444a.jpg'},

    { x: 390, y: 400, title: '馨园', image:'https://www.helloimg.com/i/2025/02/05/67a2c56c4eba4.jpg'},
    { x: 330, y: 200, title: '学24', image:'https://www.helloimg.com/i/2025/02/05/67a2c56c55809.jpg'},
    { x: 615, y: 545, title: '知行会堂', image:'https://www.helloimg.com/i/2025/02/05/67a2c56ca9431.jpg'},
    { x: 580, y: 415, title: '学院楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c56dd979a.jpg'},
    
    { x: 520, y: 405, title: "'航'", image:'https://www.helloimg.com/i/2025/02/05/67a2e537c7d05.jpg'},
    { x: 110, y: 515, title: "快递驿站", image:'https://www.helloimg.com/i/2025/02/05/67a2df4126b8a.jpg'},
    { x: 520, y: 625, title: "南门", image:'https://www.helloimg.com/i/2025/02/05/67a2e537eb65f.jpg'},

    // 添加更多浮标点
  ]);
  const markers2 = ref([
    { x: 500, y: 185, title: '电子楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c02383bca.jpg'},
    { x: 580, y: 450, title: '海洋学院', image:'https://www.helloimg.com/i/2025/02/05/67a2c02396242.jpg'},
    { x: 430, y: 530, title: '湖西楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c022721fe.jpg'},
    { x: 690, y: 500, title: '北衡楼', image:'https://www.helloimg.com/i/2025/02/05/67a2c022e173c.jpg'},
    // 添加更多浮标点
  ]);
  // 控制对话框显示
  const dialogVisible = ref(false);
  const selectedMarker = ref({});
  
  // 打开对话框
  const openDialog = (marker) => {
    selectedMarker.value = marker;
    dialogVisible.value = true;
  };
  </script>
  
  <style>
  .map-container {
    position: relative;
    padding-left: 50px;
    padding-top: 20px;
    display: flex; /* 启用 Flexbox 布局 */
    flex-direction: row; /* 子元素横向排列（默认值，可省略） */
  }
  
  .marker {
    position: absolute;
    cursor: pointer;
  }
  .youce {
    padding: 20px;
  }
  </style>