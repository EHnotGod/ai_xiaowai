<template>
  <el-dialog v-model="dialogVisible" title="历史会话" width="30%">
    <el-table :data="history" style="width: 100%">
      <el-table-column prop="session_id" label="会话ID">
        <template #default="{ row }">
          <el-button type="text" @click="selectSession(row.session_id)">{{ row.session_id }}</el-button>
        </template>
      </el-table-column>
      <!-- 新增：显示创建时间 -->
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          <span>{{ row.created_at }}</span>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>

  <el-dialog v-model="conversationDialogVisible" title="对话记录" width="50%">
    <div class="chat-message" v-for="(item, index) in messageList" :key="index">
        <div class="user-message" v-if="item.type === 'user'">
            <p>{{ item.content }}</p>
        </div>
        <div class="send-message" v-if="item.type === 'user' && picRecords[index/2] != ''">
             <div class="img-message">
                <img height="120px" :src="picRecords[index/2]" style="height: 70px; width: auto;" />
            </div>
        </div>
        <div class="ai-message" v-if="item.type === 'ai'">
            <div class="mark-text" v-html=markdown.render(item.content)></div>
        </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { API_BASE_URL } from '@/api/config.js';
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  username: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['select-session']);
import { userInformation } from '@/api/user.js';
const UserStore = userInformation();

const dialogVisible = ref(false);
const history = ref([]);
const conversationDialogVisible = ref(false);
const conversationRecords = ref([]);
import MarkdownIt from "markdown-it";
import MarkdownItAbbr from "markdown-it-abbr";
import MarkdownItAnchor from "markdown-it-anchor";
import MarkdownItFootnote from "markdown-it-footnote";
import MarkdownItHighlightjs from "markdown-it-highlightjs";
import MarkdownItSub from "markdown-it-sub";
import MarkdownItSup from "markdown-it-sup";
import MarkdownItTasklists from "markdown-it-task-lists";
import MarkdownItTOC from "markdown-it-toc-done-right";
function parseMessageString(str) {
  const messageList = [];
  const regex = /\{'type': '([^']+)', 'content': '([^']*)'\}/g;
  let match;
  while ((match = regex.exec(str)) !== null) {
    messageList.push({
      type: match[1],
      content: match[2].replace(/\\n/g, '\n') // 处理换行符
    });
  }
  return messageList;
}

// 调用函数并存储结果
const messageList = ref([]);
const picRecords = ref([]);
// 创建 markdown-it 实例
const markdown = new MarkdownIt()
  .use(MarkdownItAbbr)
  .use(MarkdownItAnchor)
  .use(MarkdownItFootnote)
  .use(MarkdownItHighlightjs)
  .use(MarkdownItSub)
  .use(MarkdownItSup)
  .use(MarkdownItTasklists)
  .use(MarkdownItTOC)
  .use((md) => {
    md.renderer.rules.image = (tokens, idx, options, env, self) => {
      const token = tokens[idx];
      const src = token.attrGet('src');
      const alt = token.content;
      return `<img src="${src}" alt="${alt}" style="max-width: 100%; height: auto;" />`;
    };
  });
// 打开对话框并加载历史会话
const openDialog = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: UserStore.username }),
    });

    if (!response.ok) {
      throw new Error('获取历史会话失败');
    }

    const data = await response.json();
    // 根据created_at排序
    history.value = data.history
      .map(session => ({ session_id: session.session_id, created_at: session.created_at }))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));  // 按日期倒序排序
    dialogVisible.value = true;
  } catch (error) {
    console.error('获取历史会话失败', error);
  }
};

const selectSession = async (sessionId) => {
  console.log('选择的会话ID:', sessionId);
  emit('select-session', sessionId);
  dialogVisible.value = false;

  try {
    const response = await fetch(`${API_BASE_URL}/get_conversation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sessionId }),
    });

    if (!response.ok) {
      throw new Error('获取对话记录失败');
    }

    const data = await response.json();
    conversationRecords.value = data.conversations[0]['message'];
    picRecords.value = data.picconversations[0]['picmessage']
    .split("******")
    .map((message) => structuredClone(message));
    messageList.value = parseMessageString(conversationRecords.value);
    
    console.log(messageList.value);
    conversationDialogVisible.value = true;
  } catch (error) {
    console.error('获取对话记录失败', error);
  }
};

defineExpose({
  openDialog,
});
</script>
<style scoped>
.chat-message {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end; /* 将内容右对齐 */
}

.user-message {
  text-align: right;
  color: blue;
  max-width: 80%;
}

.send-message {
  display: flex;
  justify-content: flex-end; /* 图片右对齐 */
  width: 100%;
}

.img-message img {
  border-radius: 8px;
  margin-top: 10px;
}

.ai-message {
  max-width: 80%;
  text-align: left;
  color: green;
  align-self: flex-start; /* AI 消息左对齐 */
}
</style>