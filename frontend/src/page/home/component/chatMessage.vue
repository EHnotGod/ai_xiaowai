<template>
    <div class="all-massage">
    <div class="chat-message" v-for="(item, index) in chatStore.chatHistory" :key="index">
        <div class="user-message" v-if="item.type === 'user'">
            <!-- 文本 -->
            <p>{{ item.content }}</p>
        </div>
        <div class="send-message" v-if="item.type === 'user' && chatStore.picHistory[index/2] != ''">
            <!-- 图片 -->
             <div class="img-message">
                <img height="120px" :src="chatStore.picHistory[index/2]" style="height: 120px; width: auto;" />
            </div>
        </div>
        <!-- 大模型回复 -->
        <div class="ai-message" v-if="item.type === 'ai'">
            <div class="mark-text" v-html=markdown.render(item.content)></div>
        </div>
        <!-- <weather></weather> -->
    </div>
    <div class="ai-message" v-if=chatStore.loading>
        <div class="mark-text">
            <loadIng></loadIng>
        </div>
    </div>
</div>
</template>

<script setup>
import weather from "./weather.vue";
import loadIng from "../component/loading.vue";
import { useChatStore } from '@/api/counter.js';
const chatStore = useChatStore();
import MarkdownIt from "markdown-it";
import MarkdownItAbbr from "markdown-it-abbr";
import MarkdownItAnchor from "markdown-it-anchor";
import MarkdownItFootnote from "markdown-it-footnote";
import MarkdownItHighlightjs from "markdown-it-highlightjs";
import MarkdownItSub from "markdown-it-sub";
import MarkdownItSup from "markdown-it-sup";
import MarkdownItTasklists from "markdown-it-task-lists";
import MarkdownItTOC from "markdown-it-toc-done-right";

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
</script>

<style lang="less" scoped>
    .chat-message {
        display: flex;
        flex-direction: column;
        .user-message {
            margin-top: 15px;
            max-width: 70%;
            align-self: flex-end;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeup 0.2s ease-in-out forwards;
            p{
                font-size:16px;
                line-height: 1.5;
                background-color: #3a71e8;
                color: white;
                border-bottom-left-radius: 10px;
                border-top-left-radius: 10px;
                border-bottom-right-radius: 10px;
                padding:10px;
            }
        }
        .send-message {
            display: flex;
            flex-direction: column;
            opacity: 0;
            align-self:flex-end;
            transform: translateY(20px);
            animation: fadeup 0.2s ease-in-out forwards;
            .img-massage {
                margin-top: 4px;
                
            }
        }
        
        .ai-message {
            margin-top: 15px;
            align-self: flex-start;
            opacity: 0;
            max-width: 80%;
            transform: translateY(20px);
            animation: fadeup 0.2s ease-in-out forwards;
            .mark-text {
                font-size:16px;
                line-height: 1.5;
                background-color: #ffffff;
                border-bottom-right-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 10px;
                color: #333;
                padding:10px;
            }
        }
    }
    @keyframes fadeup {
        0%{
            opacity: 0;
            transform: translateY(20px);
        }
        100%{
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>