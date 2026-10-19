# 原版后端运行说明

本目录以原项目七份 Python 文件为基础整理，保留原 FastAPI 路由、MySQL SQL、模型调度、内存会话和图片字典、流式返回及 FAISS 检索实现。改动限于环境变量配置、资源路径和显式建库入口。原包没有提供依赖清单或 SQL 建表文件，`requirements.in` 和 `schema.sql` 是根据原源码补充的运行资料，后者不是原数据库 DDL 的备份。

| 原文件 | 原有用途 |
| --- | --- |
| `main.py` | FastAPI 接口、MySQL、聊天流及图片上传 |
| `lang.py` | m3e-small、LangChain 切分、FAISS 建库与校园检索 |
| `千问测试.py` | 用千问判断需要的校园、天气、时间工具 |
| `天气查询.py` | 用千问提取城市，调用易源天气接口 |
| `时间查询.py` | 获取北京时间和星期，原文件未改动 |
| `联网查询.py` | 调用博查搜索并拼接网页摘要 |
| `basehead.py` | 读取注册时使用的默认头像 |

新增 `config.py` 只负责读取 `.env` 和解析本地资源路径，不包含业务替代实现。

## 安装与配置

使用 Python 3.12。依赖保持兼容原来的 LangChain 0.3 / `langchain-huggingface` 0.1 导入路径；模型依赖包含 PyTorch，安装体积较大。

在项目根目录打开 PowerShell：

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

请确认这里的 `python` 是 Python 3.12；也可以使用 `uv venv --python 3.12 .venv` 创建环境。`requirements.txt` 由 `requirements.in` 解析后锁定；更新时可运行：

```powershell
uv pip compile --python .venv/Scripts/python.exe --output-file requirements.txt requirements.in
```

按自己的运行环境填写 `.env`：

- `DB_HOST`、`DB_PORT`、`DB_USER`、`DB_PASSWORD`、`DB_NAME`：原 MySQL 数据库连接。
- `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`：原聊天模型，默认模型名保留 `qwen-vl-max`。
- `TOOL_API_KEY`、`TOOL_BASE_URL`、`TOOL_MODEL`：原工具选择和天气城市提取模型，模型名保留 `qwen-max-latest`；工具 key/base URL 留空时沿用聊天配置。
- `BOCHA_API_KEY`、`BOCHA_SEARCH_URL`：原博查联网搜索。
- `WEATHER_APPCODE`、`WEATHER_HOST`、`WEATHER_PATH`：原阿里云市场易源天气服务。
- `CORS_ORIGINS`：逗号分隔的前端来源，默认保留原来的 `*`。

没有把历史密钥和数据库口令带入源码或示例配置。服务商的模型可用性、套餐及额度由自己的账户决定。聊天沿用原逻辑，会先调用工具选择模型，再按需要调用天气、联网、校园检索和回答模型。

## 准备原 MySQL 表

安装并启动 MySQL。以有建库权限的账户为例，在 `backend/` 目录运行；命令会交互式询问自己的密码：

```powershell
mysql -u root -p --execute="CREATE DATABASE IF NOT EXISTS web CHARACTER SET utf8mb4;"
mysql -u root -p --database=web --execute="source schema.sql"
```

`DB_NAME` 使用其他名称时，相应调整命令。`schema.sql` 根据原 SQL 补齐 `user`、`user-session`、`conversations` 三张表及原代码用到的列。现有数据库应先自行核对结构；脚本不迁移原有数据。

## 准备原模型、知识资料与头像

路径相对于 `backend/` 解析，也可以在 `.env` 中使用绝对路径：

| 配置 | 原默认路径 | 所需内容 |
| --- | --- | --- |
| `EMBEDDING_MODEL_PATH` | `m3e-small` | 原 m3e-small 本地模型目录 |
| `KNOWLEDGE_DIR` | `linces` | 自己有权使用的 UTF-8 `.txt` 校园资料 |
| `INDEX_DIR` | `camp` | 用下面命令在本机生成的 FAISS 索引 |
| `AVATAR_PATH` | `nailong.png` | 注册账户时读取的默认头像文件 |

模型、校园知识资料和索引不随源码公开分发。默认头像 `nailong.png` 已从原包原样保留。已有原项目资源可在本机继续使用；缺少模型时，可根据 [m3e-small 官方模型说明](https://huggingface.co/moka-ai/m3e-small) 自行取得模型，并遵守模型许可。素材权利归属见[素材说明](../docs/ASSETS.md)。

准备好模型和至少一份 `.txt` 后，显式运行原来的建库函数：

```powershell
.venv\Scripts\python.exe lang.py
```

原 `faiss_vector()` 的切分参数仍是 `chunk_size=200`、`chunk_overlap=10`、句号分隔，原 `HuggingFaceEmbeddings`、`FAISS.from_documents`、`save_local` 及 `similarity_search(k=5)` 均保留。此次仅把导入 `lang.py` 时自动建库改为上述显式入口，避免每次启动都覆盖索引。知识资料更新后重新执行该命令。

原 `FAISS.load_local(..., allow_dangerous_deserialization=True)` 保留，因此 `INDEX_DIR` 应指向自己运行上述命令生成的索引；索引文件不放入公开仓库。

## 启动与原接口

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

接口文档：<http://127.0.0.1:8000/docs>。原前端配置的后端地址需与此一致。

| 路径 | 原请求和返回 |
| --- | --- |
| `POST /login` | `{username,password}` → `true` / `false` |
| `POST /zhuce` | `{username,password}` → `true` / `false` |
| `POST /sdk_run` | `{text,con_id,imggg,username,history,pichistory,iswifi}` → 每行 `{"response":"增量文本"}` |
| `POST /upload` | multipart `file`，可选 query `con_id` → JSON 字符串会话 ID |
| `POST /upload-avatar` | `{username,image}` → `{message}` |
| `POST /get-avatar` | `{username}` → `{username,base64}` 或 `{error}` |
| `POST /history` | `{username}` → `{history:[{session_id,created_at}]}` |
| `POST /get_conversation` | `{session_id}` → 原 `conversations` / `picconversations` 结构 |

消息和图片历史仍按原实现用 `******` 拼接，登录仍返回布尔值，接口仍依据请求中的用户名和会话 ID 操作数据。原型的口令保存、认证和资源访问方式也原样保留，不能据此宣称具备生产级权限管理。

## 本次验证范围

已检查原文件的配置差异和 Python 语法，并在 Windows / Python 3.12 下完成依赖解析。没有安装并验证完整 PyTorch/FAISS 模型运行环境，没有连接真实 MySQL，也没有调用真实千问、博查或易源付费服务。之前另写实现的测试不属于本目录原实现的验证结果。

可重复执行语法检查，不会导入模型或调用 API：

```powershell
python -m compileall -q -l .
```
