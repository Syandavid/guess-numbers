# 猜数字

一个可在手机浏览器、桌面浏览器直接玩，也能「添加到主屏幕」当轻量 App 用的静态 PWA。

看一眼闪过的数字，然后说出来；点屏幕（或按空格 / 回车）揭晓绿色答案。

## 怎么在本地打开

### 只想先看一眼

用浏览器直接打开本目录里的 `index.html`（`file://`）就能玩。

> 用 `file://` 打开可以玩游戏，但无法注册 Service Worker，也不能「添加到主屏幕」。完整 PWA 需要本地 HTTP 服务。

### 完整体验（离线缓存、安装到主屏幕）

在本目录启动任意静态服务器，例如：

```bash
cd guess-numbers/web
python3 -m http.server 8080
```

然后访问 http://127.0.0.1:8080/

手机预览：电脑和手机连同一 Wi-Fi，用电脑的局域网 IP 访问，例如 `http://192.168.x.x:8080/`。

## 怎么长期托管（GitHub Pages）

任意静态托管都可以。GitHub Pages 免费、适合一直开着。

1. 新建一个 GitHub 仓库，把本目录的文件放进仓库：
   - **仓库根目录**（推荐）：`index.html`、`sw.js`、`manifest.webmanifest` 和图标都在根上；或
   - **`/docs` 目录**：把同样这些文件放进 `docs/`。
2. 打开仓库 **Settings → Pages**。
3. **Build and deployment** 里 Source 选 **Deploy from a branch**。
4. Branch 选 `main`（或你的默认分支），文件夹选 `/ (root)` 或 `/docs`（与第 1 步一致），保存。
5. 等一两分钟，访问 `https://<用户名>.github.io/<仓库名>/`。

也可以把仓库做成 User/Organization site（仓库名 `username.github.io`），文件放根目录后，地址就是 `https://username.github.io/`。

> 从本仓库附带的 `guess-numbers-web-prod.zip` 部署时：解压后 **`index.html` 就在 zip 根目录**，可直接拖到仓库根或 `/docs`，不必再套一层文件夹。

## 其它静态托管

Netlify、Cloudflare Pages、Vercel 等都可以：把本目录（或 zip 解压后的根文件）丢上去即可，无需构建命令。

- **Netlify**：拖放 zip / 文件夹，或连接 Git 仓库，Publish directory 留空（根目录）。
- **Cloudflare Pages**：连接 Git 或直接上传，构建命令留空。

## 添加到主屏幕（PWA）

「添加到主屏幕」**必须使用 HTTPS**（本机 `localhost` / `127.0.0.1` 除外）。GitHub Pages / Netlify / Cloudflare Pages 默认都是 HTTPS。

### iPhone Safari

1. 用 **Safari** 打开页面（不要用微信内置浏览器）。
2. 点底部分享按钮 → **添加到主屏幕**。
3. 从主屏幕点「猜数字」图标，会以全屏独立窗口打开，并可离线使用。

### Android Chrome

打开页面 → 菜单 → **安装应用** / **添加到主屏幕**。

### 电脑 Chrome / Edge

地址栏右侧的安装图标，或菜单里的「安装猜数字」。

## 玩法

1. 首页点 **开始**（电脑上也可按 **空格** 或 **回车**）。
2. 屏幕中央出现橙色 **准备**，约 1.5 秒后闪出一串数字。
3. 数字消失后出现白色 **请说**，请把刚才看到的数字说出来。
4. 再点一次屏幕（或空格 / 回车）出现**绿色答案**。
5. 再点一次进入下一轮橙色 **准备**。点 **重玩** 用同一串数字再闪一次。点 **退出** 或按 **Esc** 返回上一屏 / 首页。

长数字会自动缩小并折行，保证完整显示在舞台内。

首页可进 **难度设置**：

- 闪现时长：0.05–1.00 秒（含极快 / 很快 / 快 / 普通 / 慢）
- 数字位数：1–15 位，或随机区间
- 数字大小：50%–100%

设置保存在本机（localStorage）。无需账号。

## 电脑与手机布局

- **手机**：全屏铺满。
- **宽屏电脑**：居中一块约 480px 宽的手机舞台，四周深色背景。
- 键盘：**空格 / 回车** 等同于点屏幕；**Esc** 退出或返回。

## 文件

- `index.html` — 页面、样式与游戏逻辑
- `manifest.webmanifest` — PWA 清单（名称：猜数字，竖屏，深色，theme-color）
- `sw.js` — Service Worker（缓存名 `guess-numbers-v9`；`index.html` 网络优先，方便更新）
- `icon.svg` / `icon-192.png` / `icon-512.png` / `apple-touch-icon.png` — 图标

无需安装、无需构建。HTTPS 下添加到主屏幕后即可离线使用。
