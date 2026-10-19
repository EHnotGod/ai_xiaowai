# 后端运行与接口

这是历史项目的开源整理版。保留 FastAPI、OpenAI 兼容模型调用、校园知识检索、图片提问、账户和聊天记录。原包没有提供数据库建表脚本和依赖清单，本目录提供新的明确表结构，**不能直接连接原数据库当作迁移工具**。

推荐 Python 3.12（支持 Python 3.11+）。从项目根目录开始，在 PowerShell 中运行：

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python.exe -m app.build_index
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Linux / macOS：

```sh
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python -m app.build_index
.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

也可用 `uv venv --python 3.12 .venv` 创建环境。接口文档：<http://127.0.0.1:8000/docs>；健康状态：<http://127.0.0.1:8000/health>。修改 `.env` 或重建索引后请重启后端。不要提交 `.env`、`data/`、模型缓存或个人知识文档。

## 配置与数据库

默认使用 `backend/data/xiaowai.db`，启动时创建 `users`、`access_tokens`、`conversations` 表。开发环境无需安装 MySQL。要用 MySQL，先自行创建一个 UTF-8 数据库和专用账户，再修改 `DATABASE_URL`；格式见 `.env.example`。URL 中密码包含 `@`、`:`、`/` 等字符时须进行 URL 编码。自动建表不负责已有表的版本迁移。

`LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 都需要填写；选用服务商账户中实际可用的 OpenAI Chat Completions 兼容模型。图片提问要求该模型支持 `image_url`。未填写时账户、历史等接口仍可运行，聊天返回明确的 HTTP 503，健康接口的 `llm_configured` 为 `false`。这仅表示配置是否齐全，不代表服务商连通性或余额已经验证。

`CORS_ORIGINS` 是逗号分隔的前端地址，默认只允许本机 5173 端口。`TOKEN_TTL_HOURS` 默认为 24；服务端时间戳以 UTC 储存并返回。其余配置见 `.env.example`。

## 知识库与 RAG

`knowledge/demo-campus.txt` 是原创虚构校园资料，随项目按 MIT 发布，**不代表任何真实学校规则**。如要使用真实校园资料，应先确认公开使用和再分发权限。个人本地资料请放入 `knowledge/local/`（已加入 Git 忽略，可自行创建），默认会递归检索其中的 UTF-8 `.txt`；执行 `python -m app.build_index` 更新索引。准备随开源项目公开的资料才放在其他受 Git 跟踪的知识目录，并确认其许可。也可用 `KNOWLEDGE_DIR` 指向项目外部的个人资料目录。

索引使用 LangChain `Document` 和递归文本切分器，生成可检查的 JSON 文本与向量；请求时检索相关片段，连同最近对话和相应图片发送给所配置的模型服务。索引在显式运行构建命令时创建，后端导入时不会建库、下载模型或加载原包的 FAISS/pickle 文件。数据更新后需重新构建并重启服务。缺失索引时聊天返回 503，不会把未检索到的结果当作校园事实。

两种检索模式的能力不同：

| 模式 | 用途 | 依赖与限制 |
| --- | --- | --- |
| `RAG_MODE=lexical`（默认） | 无需模型下载的字符 n-gram 哈希向量演示 | 只体现字面相似度；不是原 m3e 语义模型，同义词和复杂问题效果有限 |
| `RAG_MODE=huggingface` | 使用 LangChain HuggingFaceEmbeddings 做语义检索 | 单独安装可选依赖，首次显式建库可能下载模型，内存与磁盘开销较大 |

保留原项目 m3e-small 检索思路的方法：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-rag.txt
# 在 .env 设置 RAG_MODE=huggingface；EMBEDDING_MODEL=moka-ai/m3e-small
.venv\Scripts\python.exe -m app.build_index
```

`EMBEDDING_MODEL` 也可以指向自行取得、确认来源和许可的本地模型目录。构建阶段允许下载指定模型；服务运行期间仅从本机缓存加载，不自动下载，且关闭远程模型代码执行。改变模式或模型后必须重建索引。向量用余弦相似度在小型 JSON 索引内检索，未沿用原 FAISS 二进制索引；适用于教学规模知识库。可选模型依赖及真实服务商调用未纳入离线自动测试。

参考：[LangChain 文本切分器](https://reference.langchain.com/python/langchain-text-splitters)、[Hugging Face 集成](https://docs.langchain.com/oss/python/integrations/embeddings/huggingfacehub)、[m3e-small 模型说明及许可](https://huggingface.co/moka-ai/m3e-small)。模型及其权重遵循自身许可，项目 MIT 不替代第三方许可。

## 接口约定

请求体和响应均为 JSON（图片文件上传除外）。路径保留原名称；鉴权是必要的不兼容修复：登录现在返回 token，后续接口需 `Authorization: Bearer <access_token>`。账户隔离依据 token，不能再通过请求里的 `username` 访问其他人的资料。`username` 若提供，必须为本人。

| 方法与路径 | 请求 | 成功响应 |
| --- | --- | --- |
| `GET /health` | 无需登录 | 模型配置、知识索引和功能状态 |
| `POST /zhuce` | `{username,password}`，用户名 2–32 字，字母数字、中文、`_ . -`；密码 8–128 字 | `true`，重名 409 |
| `POST /login` | `{username,password}` | `{access_token,token_type,username,expires_in}`，错误 401 |
| `POST /logout` | 无请求体，需 token | 撤销当前 token |
| `POST /history` | `{}` 或 `{username}` | `{history:[{session_id,created_at}]}` |
| `POST /get_conversation` | `{session_id}` | `{session_id,messages:[{type,content,picture?}],pictures:[...]}` |
| `POST /upload` | multipart `file`；可选 query `con_id` | JSON 字符串形式的会话 ID |
| `POST /sdk_run` | `{text,con_id?,imggg?,iswifi?}` | NDJSON 流，见下文 |
| `POST /get-avatar` | `{}` 或 `{username}` | `{username,base64}`，未设置时 `null` |
| `POST /upload-avatar` | `{image,username?}`，image 为 data URL | `{message}` |

图片限 JPEG/PNG/WebP、5 MiB，校验媒体类型和文件头。上传图片后用返回的 `con_id` 调用 `/sdk_run`，并设置 `imggg:true`。图片 data URL 会随本次完整回答存入对应用户的会话历史；前端历史中的 `picture` 可直接显示。同会话已有回答在生成时，新的提问和图片上传返回 409。

聊天按行返回 UTF-8 JSON：

```json
{"response":"增量文本"}
{"response":"后续文本"}
{"done":true,"con_id":"会话 ID","sources":[{"source":"demo-campus.txt","score":0.5}]}
```

发生上游错误时，流中返回 `{error,con_id}`，本轮不保存。客户端应区分 `error` 与 `done`，不能把 HTTP 200 当作回答完整。客户端提交的旧 `history` 和 `pichistory` 字段仅为兼容接收，不作为可信历史；历史以服务端记录为准。旧 `conversations` / `picconversations` 字段保留，但值改为 JSON 字符串，不再提供 Python 表达式；新客户端使用 `messages`。

原型中的第三方天气和联网搜索没有带入历史密钥，当前没有配置实现；`iswifi:true` 明确返回 503，`/health` 标识这两项不可用。普通聊天、校园资料问答与图片问答仍可按上述方式使用。没有接入真实教务系统或个人课程表。

## 安全范围与验证

密码使用带独立随机盐的 PBKDF2-HMAC-SHA256（600,000 次）保存；随机 bearer token 在数据库仅保存 SHA-256 摘要，可过期和退出撤销。会话、头像及图片操作检查资源所属用户。这里没有管理员角色或 RBAC，也未实现短信验证、密码重置、登录限速、审计系统或多实例会话并发协调。当前按单进程运行，请勿使用多个 worker 承担同一会话的并发写入；会话锁仅在当前进程内生效。该整理版仍是校园项目原型，公开部署前需自行补充运营所需能力、HTTPS 和备份策略。

运行离线测试：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest -q
```

测试使用临时 SQLite 数据库、临时知识索引及假的模型流，覆盖注册登录、token 失效、跨用户访问拒绝、图片校验、完整流保存及失败不保存，不调用付费 API。已在 Python 3.12 上验证默认 SQLite/离线检索流程；没有连接真实 MySQL、调用服务商模型或下载 m3e 权重验证。鉴权头的标准形式见 [FastAPI 安全文档](https://fastapi.tiangolo.com/tutorial/security/)。
