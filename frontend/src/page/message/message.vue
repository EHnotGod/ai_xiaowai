<template>
    <div class="page-content-insidebox scroll" id="page-content">
      <!-- 快速查询模块 -->
      <div class="quick-access-container">
        <el-row>
          <el-col :span="24">
            <h2 class="section-title">信息快速查询</h2>
          </el-col>
        </el-row>
  
        <el-row :gutter="20">
          <el-col
            v-for="(item, index) in quickAccessItems"
            :key="index"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card
              class="quick-access-item"
              :class="item.bgColor"
              @click="handleItemClick(item)"
            >
              <div class="item-content">
                <i :class="item.icon"></i>
                <h3>{{ item.label }}</h3>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // 快速查询模块数据
  const quickAccessItems = ref([
     { label: '山威主页', icon: 'fa fa-graduation-cap', bgColor: 'bg-gold', url: 'https://www.wh.sdu.edu.cn/' },
     { label: '信息服务', icon: 'fa fa-calendar-alt', bgColor: 'bg-blue', url: 'https://service.sdu.edu.cn/tp_up/view?m=up' },
     { label: '自习室查询', icon: 'fa fa-chalkboard', bgColor: 'bg-green', url: 'http://msg.wh.sdu.edu.cn:9008/free-classroom-select.html;jsessionid=BEB4A3D5F779A9964279A97D8B0ECEDA' },
     { label: '图书馆预约', icon: 'fa fa-book-open', bgColor: 'bg-red', url: 'https://libseat.sdu.edu.cn/home/web/seat/area/156' },
     { label: '校园指南', icon: 'fa fa-bus-alt', bgColor: 'bg-purple', url: 'https://pd.qq.com/s/q6krhqej?shareSource=5&businessType=2' },
     { label: '志愿学时', icon: 'fa fa-file-alt', bgColor: 'bg-orange', url: 'http://222.194.64.76/index.jsp' },
     { label: '学院官网', icon: 'fa fa-university', bgColor: 'bg-dark', url: 'https://math.wh.sdu.edu.cn/' },
     { label: '培养方案', icon: 'fa fa-file-alt', bgColor: 'bg-teal', url: 'https://math.wh.sdu.edu.cn/info/1360/26723.htm' },
     { label: '空调电费', icon: 'fa fa-bolt', bgColor: 'bg-pink', url: 'https://gyktgd.wh.sdu.edu.cn/dianbiao/AuthServlet.se' },
     { label: '新闻资讯', icon: 'fa fa-newspaper', bgColor: 'bg-cyan', url: 'https://math.wh.sdu.edu.cn/xyxw.htm' },
     { label: '通知公告', icon: 'fa fa-calendar-check', bgColor: 'bg-lime', url: 'https://math.wh.sdu.edu.cn/tzgg.htm' },
     { label: '失物招领', icon: 'fa fa-graduation-cap', bgColor: 'bg-indigo', url: 'https://msg.wh.sdu.edu.cn/index.html' },
  ]);
  
  // 点击事件处理
  const handleItemClick = (item) => {
    console.log('访问模块:', item.label);
    if (item.url) {
      window.open(item.url, '_blank');
    }
  };
  </script>
  
  <style scoped>
/* 快速查询样式 */
.quick-access-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  color: #333;
  font-size: 28px; /* 字体更大 */
  border-bottom: 2px solid #c4a267;
  padding-bottom: 10px;
  margin-bottom: 30px;
}

.quick-access-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px; /* 更小的内边距 */
  border-radius: 8px; /* 边角更圆润 */
  color: white;
  text-align: center;
  transition: all 0.3s ease;
  text-decoration: none;
  min-height: 120px; /* 方块高度变小 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.quick-access-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.quick-access-item i {
  font-size: 3em; /* 图标变大 */
  margin-bottom: 10px;
}

.item-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 马卡龙色系 */
.bg-gold { background-color: #f8d68d; }
.bg-blue { background-color: #82c7d0; }
.bg-green { background-color: #a1d99e; }
.bg-red { background-color: #fbb7b1; }
.bg-purple { background-color: #d4bde7; }
.bg-orange { background-color: #ffd478; }
.bg-teal { background-color: #8ac5c5; }
.bg-pink { background-color: #f7a0b6; }
.bg-dark { background-color: #e0e0e0; }
.bg-cyan { background-color: #a1e2e2; }
.bg-lime { background-color: #d7f1a1; }
.bg-indigo { background-color: #9fa2d8; }

/* 响应式设计 */
@media (max-width: 1024px) {
  .quick-access-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-access-item {
    padding: 10px;
    min-height: 100px; /* 更小的高度 */
  }

  .quick-access-item i {
    font-size: 2.5em; /* 图标适应 */
  }
}

@media (max-width: 480px) {
  .quick-access-grid {
    grid-template-columns: 1fr;
  }
}

  /* 响应式设计 */
  @media (max-width: 1024px) {
    .quick-access-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  @media (max-width: 768px) {
    .quick-access-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  
    .quick-access-item {
      padding: 15px;
      min-height: 120px;
    }
  
    .quick-access-item i {
      font-size: 2em;
    }
  }
  
  @media (max-width: 480px) {
    .quick-access-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>