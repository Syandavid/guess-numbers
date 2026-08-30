# 猜数字

一个可在手机浏览器、桌面浏览器直接玩，也能「添加到主屏幕」的记忆训练 PWA。

看一眼闪过的数字，然后说出来；点屏幕（或按空格 / 回车）揭晓答案。项目同时支持本地练习、每日记录、挑战模式和 Firebase 多人房间。

线上地址：<https://syandavid.github.io/guess-numbers/>

## 本地预览

仓库文件都在根目录。在项目根目录启动静态服务器：

```bash
python -m http.server 8080
```

然后访问 <http://127.0.0.1:8080/>。手机预览时，电脑和手机连同一 Wi-Fi，用电脑当前局域网 IP 访问，例如 `http://192.168.x.x:8080/`。

不要用 `file://` 打开完整体验，否则无法注册 Service Worker，也不能安装为 PWA。

## GitHub Pages

本项目按 `main` 分支根目录发布：

<https://syandavid.github.io/guess-numbers/>

如需重新配置，打开仓库 **Settings → Pages**，选择 **Deploy from a branch**、分支 `main`、目录 `/ (root)`。

## 添加到主屏幕

「添加到主屏幕」必须使用 HTTPS（本机 `localhost` / `127.0.0.1` 除外）。

- iPhone Safari：分享 → 添加到主屏幕。
- Android Chrome：菜单 → 添加到主屏幕或安装应用。
- 电脑 Chrome / Edge：地址栏安装图标，或菜单里的安装选项。

## 玩法

1. 首页点 **开始**，电脑上也可按空格或回车。
2. 屏幕中央出现橙色「准备」，随后短暂显示数字。
3. 数字消失后出现「请说」，说出刚才看到的数字。
4. 再点屏幕或按键揭晓绿色答案。
5. 可进入难度设置调整闪现时长、数字位数和数字大小。

挑战模式和多人房间需要匿名登录；本地练习不需要账号。

## Firebase 后端

多人房间、每日记录和挑战数据使用 Firebase 项目 `guessnums-9f588` 的匿名认证与 Firestore。`.firebaserc`、`firebase.json`、`firestore.rules` 和 `firestore.indexes.json` 是部署配置，不包含服务账号密钥。

如果本机已安装 Firebase CLI，可在仓库根目录执行：

```bash
firebase use guessnums-9f588
firebase deploy --only firestore:rules,firestore:indexes
```

不要把服务账号 JSON、私钥、密码或其他令牌提交到仓库。

## 房间安全边界

房间数字必须在闪现阶段发送到参与者浏览器，因此这是面向普通用户的记忆游戏，不是具备服务器裁判能力的防作弊系统。Firestore Rules 负责登录、房间成员和字段写入边界；不能阻止拥有开发者工具经验的参与者检查自己浏览器收到的数据。

## 文件

- `index.html` — 页面、样式与游戏逻辑
- `manifest.webmanifest` — PWA 清单
- `sw.js` — Service Worker 与离线缓存
- `firestore.rules` — Firestore 访问规则
- `scripts/validate_project.py` — 不访问网络的项目完整性检查
- `sfx/` — 游戏音效

无需安装、无需构建。HTTPS 下添加到主屏幕后即可离线使用。

## 维护约定

- `main` 始终保持可部署；新功能使用 `feat/` 分支，修复使用 `fix/` 分支。
- 提交前运行 `python scripts/validate_project.py`。
- 有用户可见变化时更新 `CHANGELOG.md`，稳定节点使用 `v0.x.y` 标签。
- 任何 Firebase Rules 变更都要单独检查读取范围、写入字段和删除权限。

详细流程见 [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md)。
