from config import LLM_API_KEY, EMBEDDING_MODEL_PATH, KNOWLEDGE_DIR, INDEX_DIR
import os
import openai
from langchain.chains.qa_with_sources.stuff_prompt import template
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy.dialects.mysql.mariadb import loader

api_key=LLM_API_KEY
openai.api_key = api_key

### 加载文档
### 构建向量模型路径
### 切分文档设置
### 初始化embedding模型
### 将切分后的文档进行向量化，并且存储下来
### 返回的是切分文档数据
import os


def faiss_vector():
    ### 1.构建向量模型路径
    EMBEDDING_MODEL = EMBEDDING_MODEL_PATH

    ### 2.加载文档
    data = []
    linces_folder = KNOWLEDGE_DIR

    # 遍历linces文件夹中的所有.txt文件
    for filename in os.listdir(linces_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(linces_folder, filename)
            loader = TextLoader(file_path, encoding="utf-8")
            data.extend(loader.load())

    ### 3.切分文档设置
    text_split = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10, separators="。")
    split_data = text_split.split_documents(data)

    ### 4.初始化embedding模型
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    ### 5.将切分后的文档进行向量化，并且存储下来
    db = FAISS.from_documents(split_data, embeddings)
    db.save_local(INDEX_DIR)

    ### 6.返回的是切分文档数据
    return split_data
def get_faiss_vector():
    EMBEDDING_MODEL = EMBEDDING_MODEL_PATH
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.load_local(folder_path=INDEX_DIR,embeddings=embeddings ,allow_dangerous_deserialization=True)
    return db


def school_content(question):
    db = get_faiss_vector()
    docs = db.similarity_search(question, k=5)
    related_docs = get_related_content(docs)
    PROMPT_TEMPLATE = """
    {content}
    """
    prompt = PromptTemplate(input_variables=["content"], template=PROMPT_TEMPLATE)
    my_prompt = prompt.format(content=related_docs, question=question)
    return my_prompt

def get_related_content(docs):
    related_docs = []
    for doc in docs:
        related_docs.append(doc.page_content.replace("\n\n", "\n"))
    return "\n".join(related_docs)

def system_prompt():
    prompt = """
            角色定义： 你是一个智能校园助手，专为大学新生设计，帮助他们快速适应校园生活。你提供以下服务：

            报到流程指导：帮助新生了解报到的每个步骤，如注册、领取校园卡等。
            课程安排查询：查询课程表、课堂信息、学分要求等。
            智能对话支持：解答新生的疑惑，提供及时帮助。
            图像识别支持：识别校园建筑或活动，提供相关信息。
            要求：

            个性化服务：根据新生的个人信息（如专业、兴趣）提供定制化帮助。
            亲和力：语气友好、幽默、温暖，避免机械性回答。
            情绪感知：识别新生的情绪变化，给予情感回应，舒缓他们的压力。
            特征：热心、耐心、鼓励性强，语言自然且富有温暖感。
            目标用户：大学新生，帮助他们顺利适应大学生活。
        """

    return prompt

# def connect_qianfan(question):
#     my_prompt = define_prompt(question)
#     print("提示词：\n", my_prompt)
#
#     client = OpenAI(
#         api_key=LLM_API_KEY,
#         base_url="https://aistudio.baidu.com/llm/lmapi/v3",  # aistudio 大模型 api 服务域名
#     )
#     chat_completion = client.chat.completions.create(
#         messages=[{'role': 'system', 'content': system_prompt()}, {'role': 'user', 'content': my_prompt}],  # 使用该会话的历史记录
#         model="ernie-4.0-turbo-8k",
#         stream=True
#     )
#     for chunk in chat_completion:
#         try:
#             # 添加 AI 的回复到对话历史中
#             if chunk.model_dump()['choices'][0]['delta']['content'] != "" and chunk.model_dump()['choices'][0]['delta']['content'] != None:
#                 print(chunk.model_dump()['choices'][0]['delta']['content'])
#         except Exception as e:
#             print(f"Error processing chunk: {e}")


if __name__ == "__main__":
    faiss_vector()
