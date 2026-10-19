# AI 小崴 · 原版前端

本目录保留原 Vue 3、Pinia、Element Plus 页面、样式、图片、字体和业务脚本。没有重做界面，也没有改为新的登录或聊天协议。

## 启动

使用 Node.js 24。在仓库根目录打开 PowerShell：

```powershell
cd frontend
Copy-Item .env.example .env
npm ci
npm run dev
```

Linux / macOS 使用 `cp .env.example .env`，其余 npm 命令相同。默认地址由 Vite 输出。

`.env` 中只有公开的 `VITE_API_BASE_URL`，默认 `http://localhost:8000`。它代替原代码里的旧服务器地址；模型和其他服务密钥只配置在后端。

## 保留的原页面与流程

- 原校徽侧栏、展开/收起、登录注册弹窗、头像及历史记录。
- 原问答页面、图片上传、流式显示及“联网查询”开关。
- 原校园地图、19 个建筑热点、720 全景和 12 个信息入口。
- 原关于页面、轮播、图片和包图小白体。

登录仍使用原布尔返回、用户名状态和原历史格式，与[原版后端](../backend/README.md)配合使用；没有新增 Token 登录接口。

原图床部分地址已返回 404，页面中保留原地址及原包已有的全部本地素材，没有使用新设计替代。详见[素材说明](../docs/ASSETS.md)。

## 构建

```powershell
npm run build
npm run preview
```

依赖清单保留原包内容，锁文件做了同主版本内的兼容更新。原大包构建警告保留，不为了减少体积而改组件注册或页面。构建输出 `dist/` 不提交 Git。
