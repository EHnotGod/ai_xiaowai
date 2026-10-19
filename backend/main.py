from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, CORS_ORIGINS, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
import uuid

from fastapi.responses import StreamingResponse
from openai import OpenAI, BaseModel
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import base64
import json
import pymysql
from 千问测试 import usewhattools
from 时间查询 import get_beijing_time
from 天气查询 import weather
from 联网查询 import web_content
from starlette.middleware.cors import CORSMiddleware
from lang import system_prompt, school_content
from basehead import nailong

app = FastAPI()

# 配置 CORS 中间件，允许来自 http://localhost:5173 的请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # 允许的源，确保与前端的地址匹配
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)
class Login(BaseModel):
    username: str
    password: str
# 数据库连接配置
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,  # 替换为你的数据库用户名
    "password": DB_PASSWORD,  # 替换为你的数据库密码
    "database": DB_NAME,  # 替换为你的数据库名
    "cursorclass": pymysql.cursors.DictCursor,  # 返回字典格式的结果
}
# 用于存储每个会话的对话记录
conversations = {}
img_global = {}
class Conversation(BaseModel):
    text: str
    con_id: str=None
    imggg: bool=False
    username: str=None
    history:list=None
    pichistory:list=None
    iswifi:bool=False
@app.post("/sdk_run")
async def run(item:Conversation):
    global img_global,conversations
    con_id = item.con_id
    text = item.text
    username = item.username
    print(con_id)
    print(text)

    if con_id not in conversations:
        conversations[con_id] = [
                {'role': 'user', 'content': "你是谁？"},
                {'role': 'assistant', 'content': system_prompt()},
        ]
    tools = usewhattools(text)
    print(tools)
    prompt = ""
    if "时间查询" in tools:
        prompt += "时间信息：" + get_beijing_time() + "\n"
    if "天气查询" in tools:
        prompt += "天气信息：" + weather(text) + "\n"
    if item.iswifi:
        prompt += "联网信息：" + web_content(text) + "\n"
    if "校园知识查询" in tools:
        prompt += "校园知识信息：" + school_content(text) + "\n"
    if prompt == "":
        all_content = text
    else:
        all_content = "基于以下已知信息，简洁地来回答用户的问题（假如需要输出图片，请把图片链接以Markdown格式输出）:" + prompt + "用户的问题：" + text
    if item.imggg:
        content = [
                {
                    "type": "text",
                    "text": all_content
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{img_global[con_id]}"
                  }
                }]
    else:
        content = [
            {
                "type": "text",
                "text": all_content
            }]

    conversations[con_id].append({'role': 'user', 'content': content})

    # 设置 OpenAI 客户端
    client = OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
    )

    # 调用 OpenAI 接口进行对话生成
    try:
        chat_completion = client.chat.completions.create(
            messages=conversations[con_id],  # 使用该会话的历史记录
            model=LLM_MODEL,
            stream=True,
        )
        # chat_comp = qianfan.ChatCompletion()
        # chat_completion = chat_comp.do(model="Yi-34B-Chat", messages=conversations[con_id], stream=True)
    except:
        print(666666666666666666666666666666666666666666666666666666666666666666666666)
        conversations[con_id].pop()
    # 流式响应
    def event_stream():
        global conversations
        ai_response = ""
        try:
            for chunk in chat_completion:
                try:
                    # 添加 AI 的回复到对话历史中
                    s = chunk.model_dump()['choices'][0]['delta']['content']
                    d = dict()
                    d["response"] = s
                    ai_response += s
                    yield json.dumps(d) + "\n"
                except Exception as e:
                    print(f"Error processing chunk: {e}")
            conversations[con_id].append({'role': 'assistant', 'content': ai_response})
            print(username)
            if item.username != "":
                connection = pymysql.connect(**DB_CONFIG)
                history = item.history
                history.append({'type': 'ai', 'content': ai_response})
                print(64, history)
                history_str = "******".join(map(str, history))
                print(history_str)
                pichistory = item.pichistory
                if item.imggg:
                    pichistory.append(f"data:image/jpeg;base64,{img_global[con_id]}")
                else:
                    pichistory.append("")
                pichistory_str = "******".join(map(str, pichistory))
                try:
                    with connection.cursor() as cursor:
                        # 查询用户是否存在
                        print(999999)
                        sql = "SELECT * FROM `user-session` WHERE user_id = %s AND session_id = %s"
                        cursor.execute(sql, (username, con_id))
                        userlog = cursor.fetchone()
                        print(userlog)

                        if userlog is None:
                            print(666)
                            # 插入新用户会话
                            sql = "INSERT INTO `user-session` (user_id, session_id) VALUES (%s, %s)"
                            cursor.execute(sql, (username, con_id))
                            connection.commit()  # 确保插入的变化被提交

                            # 插入新会话记录
                            sql = "INSERT INTO `conversations` (session_id, message, picmessage) VALUES (%s, %s, %s)"
                            cursor.execute(sql, (con_id, history_str, pichistory_str))
                            connection.commit()  # 确保插入的变化被提交
                        else:
                            # 更新现有会话记录
                            sql = "UPDATE `conversations` SET message = %s, picmessage = %s WHERE session_id = %s"
                            cursor.execute(sql, (history_str, pichistory_str, con_id))
                            connection.commit()  # 确保更新的变化被提交

                        return True
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return False
                finally:
                    if connection:
                        connection.close()
        except:
            pass
    # 返回流式响应
    return StreamingResponse(event_stream())

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        con_id: str = None):
    global img_global
    if con_id is None:
        con_id = str(uuid.uuid4())
    binary_data = await file.read()  # Read the binary data
    base64_encoded = base64.b64encode(binary_data).decode('utf-8')
    img_global[con_id] = base64_encoded
    print(con_id)
    print(777777)
    return con_id


@app.post("/login")
async def login(item: Login):
    username = item.username
    password = item.password
    # 连接数据库
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 查询用户是否存在
            sql = "SELECT * FROM user WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if user is None:
                # 用户不存在
                return False
            # 检查密码是否正确
            if user["password"] != password:
                return False
            # 登录成功
            return True
    finally:
        connection.close()

@app.post("/zhuce")
async def zhuce(item: Login):
    username = item.username
    password = item.password
    # 连接数据库
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 查询用户是否存在
            sql = "SELECT * FROM user WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if user is None:
                sql = "INSERT INTO user (username, password, base64) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, password, nailong()))
                connection.commit()  # 确保插入的变化被提交
                return True
            return False
    finally:
        connection.close()


class AvatarUpload(BaseModel):
    username: str  # 用户名
    image: str  # Base64编码的图片

@app.post("/upload-avatar")
async def upload_avatar(avatar: AvatarUpload):
    try:
        # 解码Base64图片
        image_data = avatar.image

        # 将Base64编码保存到数据库
        connection = pymysql.connect(**DB_CONFIG)
        try:
            with connection.cursor() as cursor:
                # 更新对应用户的base64字段
                sql = "UPDATE user SET base64 = %s WHERE username = %s"
                cursor.execute(sql, (avatar.image, avatar.username))
                connection.commit()  # 提交事务
        finally:
            connection.close()  # 关闭数据库连接

        return {"message": "头像上传成功"}
    except:
        pass

class UsernameRequest(BaseModel):
    username: str  # 用户名
# 通过POST请求查询头像
@app.post("/get-avatar")
async def get_avatar(request: UsernameRequest):
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        try:
            with connection.cursor() as cursor:
                # 查询对应用户的base64字段
                sql = "SELECT base64 FROM user WHERE username = %s"
                cursor.execute(sql, (request.username,))
                result = cursor.fetchone()  # 获取查询结果
                if result:
                    return {"username": request.username, "base64": result['base64']}
                else:
                    return {"error": "用户不存在"}
        finally:
            connection.close()  # 关闭数据库连接
    except Exception as e:
        return {"error": str(e)}


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)
class Request(BaseModel):
    username: str  # 用户名
@app.post("/history")
async def get_history(request: Request):
    username = request.username
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT session_id, created_at
                FROM `user-session`
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (username,))
            result = cursor.fetchall()
            # 返回session_id和created_at字段
            return {"history": [{"session_id": row["session_id"], "created_at": row["created_at"]} for row in result]}
    finally:
        connection.close()


# 定义请求体模型
class ConversationRequest(BaseModel):
    session_id: str
@app.post("/get_conversation")
async def get_conversation(request: ConversationRequest):
    session_id = request.session_id
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # 查询指定session_id的所有消息
            sql = "SELECT message FROM conversations WHERE session_id = %s ORDER BY id"
            cursor.execute(sql, (session_id,))
            conversations = cursor.fetchall()
            sql = "SELECT picmessage FROM conversations WHERE session_id = %s ORDER BY id"
            cursor.execute(sql, (session_id,))
            picconversations = cursor.fetchall()

            message = {"conversations": [{"message": row["message"]} for row in conversations],
                       "picconversations": [{"picmessage": row["picmessage"]} for row in picconversations]}
            print(message)
        if not conversations:
            raise HTTPException(status_code=404, detail="Session not found")

        return message

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if connection:
            connection.close()