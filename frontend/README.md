# AI 小崴前端

使用 Vue 3、Pinia、Vue Router、Element Plus 和 Vite。保留原项目的蓝绿渐变、侧边导航、聊天界面及校园入口卡片，清理了硬编码的个人服务器地址、外链照片和未确认授权的字体 / 图片。

## 本地启动

需要 Node.js 24 和 npm。先按 [后端文档](../backend/README.md) 启动 API，再运行：

```powershell
cd frontend
Copy-Item .env.example .env
npm ci
npm run dev
```

Linux / macOS 将复制命令替换为 `cp .env.example .env`，其余 npm 命令相同。

浏览器打开 `http://localhost:5173`。开发服务只监听本机，端口固定为 5173。如需更换访问来源，请同步修改后端 `CORS_ORIGINS`。

## 环境变量

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `http://localhost:8000` | 后端地址；不要在末尾添加接口路径 |
| `VITE_CAMPUS_MAP_URL` | 空 | 可选的 HTTP(S) 校园地图页面；需自行取得嵌入授权 |

`VITE_` 变量会打包进浏览器代码，**不要放模型密钥、数据库口令或其他秘密**。修改变量后重启开发服务；生产构建需要重新执行 `npm run build`。

## 功能与边界

- 注册后自动登录；令牌保存在当前标签页的 `sessionStorage`。退出登录会清空当前聊天和头像，并尝试撤销后端令牌；未连接后端时仍完成本地退出。
- 问答需要登录及后端模型配置。前端以 NDJSON 增量显示回复，支持跨网络分块的 JSON / 中文文本；服务端错误和中断会直接提示。
- 图片先上传再发送提问，支持 PNG、JPEG、WebP，单张最大 5 MiB。图片理解能力取决于部署者所选模型。头像上限为 2 MiB。
- 历史记录由后端按用户隔离，支持查看和继续会话；聊天进行期间禁止重复发送和切换会话。
- 校园信息页是原项目收录的学校网站快捷入口，不是教务系统数据查询；链接未做实时可用性承诺，部分页面需要校园网络或身份认证。
- 原地图仅为静态图片和可点击点位，没有路径规划。地图图片、校园照片及第三方全景未随开源包发布。配置 `VITE_CAMPUS_MAP_URL` 后可嵌入自有地图页面，目标页面需允许 iframe 嵌入。
- 原联网查询与天气服务未随项目提供，界面明确标注未配置，发送请求固定 `iswifi: false`。没有展示静态天气作为实时数据。
- AI 输出使用关闭 HTML 的 Markdown 解析，并经 DOMPurify 清洗后展示；代码块支持语法高亮。

## 构建与验证

```powershell
npm test
npm run build
npm run preview
```

构建输出在 `dist/`，不纳入 Git。路由使用 Hash 模式，静态托管通常不需要额外的前端路由重写。`npm test` 覆盖 NDJSON 的任意字节分块、中文、多行、无末尾换行、错误事件与损坏数据，以及旧账号的迟到 401 不能清除新账号会话等登录隔离行为。

## API 约定

所有请求统一通过 `src/api/client.js` 使用 `VITE_API_BASE_URL`。除 `/health`、`/login`、`/zhuce` 外，接口发送 `Authorization: Bearer <token>`。具体请求字段及错误行为见 [后端接口表](../backend/README.md)。不要重新添加旧的线上个人服务器地址。

原始位图、学校标识、第三方品牌图、团队照片和未知字体均未分发；当前标识和图形使用原生 CSS、文字与本仓库自绘 SVG，无需额外图床或字体服务。代码使用仓库根目录的 MIT 许可证。
