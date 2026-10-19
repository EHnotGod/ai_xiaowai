<template>
    <div class="we-content">
      <div class="carousel-container">
        <!-- 轮播图 -->
        <el-carousel :interval="3000" type="card" height="400px">
          <el-carousel-item v-for="(image, index) in images" :key="index" name="你好">
            <img :src="image" alt="轮播图" class="carousel-image" />
          </el-carousel-item>
        </el-carousel>

        <!-- 文本框 -->
        <div class="text-box">
          <div class="about-section">
            <h1>关于我们的AI对话项目——小崴</h1>
            <p>我们是2023级数据科学与人工智能实验班（以上为往届实验班同学的项目记录）的MilkDragon团队，专注于将人工智能与深度学习技术相结合，致力于开发更加智能、自然、便捷的对话系统。我们的项目小崴——智能校园助手，旨在为校园内的师生提供高效、个性化的互动体验，同时推动AI对话系统在校园场景中的创新应用。</p>
            <h2>项目特色</h2>
            <ul>
                <li><strong>智能校园助手</strong>小崴是专为校园场景设计的AI助手，能够帮助师生解决日常学习、生活中的问题，例如课程查询、校园导航、活动提醒等，成为校园生活中的得力助手。</li>
                <li><strong>先进的大模型算法</strong>我们采用最新的大模型技术，使小崴能够理解复杂的语义和上下文，还能够联网查询，天气查询等，提供更加智能的对话体验。</li>
                <li><strong>多领域知识库支持：</strong>小崴整合了校园相关的多领域知识库，涵盖学术、生活、娱乐等多个方面，无论是日常咨询还是专业问题，都能提供精准的回答和服务。</li>
                <li><strong>安全与隐私保护</strong>我们严格遵守隐私保护法规，对用户数据进行加密处理，确保所有对话数据的安全性和隐私性。</li>
            </ul>
            
            <h2>技术优势</h2>
            <p>小崴的AI对话系统依托于先进的自然语言处理（NLP）技术，结合深度学习算法，通过大量数据训练，能够在多种校园场景下高效地理解和生成语言。此外，系统具备自我优化能力，能够通过用户反馈不断改进对话质量和准确性。</p>
            
            <h2>未来展望</h2>
            <p>我们将持续优化小崴的功能，探索更多校园场景的应用，例如智能课程助手、学术辅导、校园生活管家等。我们的目标是让小崴成为校园内不可或缺的智能助手，帮助师生提高学习和生活效率，打造更加智能化的校园环境。</p>
            <p>通过小崴，我们希望能够为校园生活带来更多便利，同时也为AI对话系统在垂直领域的应用探索新的可能性。</p>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const images = ref([
  'https://www.helloimg.com/i/2025/02/05/67a2bf3d7f5b1.jpg',
  'https://www.helloimg.com/i/2025/02/05/67a2bf3e999f0.jpg',
  'https://www.helloimg.com/i/2025/02/05/67a2bf3e9d751.jpg'
]);
</script>


<style scoped>
    /* .ces{
        font-family: "NAME";
    }
    .ElImage{
        width:150px;
    } */
    .we-content {
        padding-left: 50px;
        padding-right: 50px;
        padding-top: 20px;
    }
    .carousel-container {
  text-align: center;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-box {
  margin-top: 20px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
  text-align: left;
}

.text-box p {
  margin: 0;
  font-size: 16px;
  color: #333;
}
</style>
