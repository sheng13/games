# Python 小游戏网站

一个使用 Flask、HTML、CSS、JavaScript 与 Socket.IO 制作的响应式小游戏网站。支持电脑与手机浏览器，并可继续加入更多游戏。

## 游戏

- 猜数字：简单、普通、困难三档
- AI 五子棋：三档 AI、本地双人、计时、历史与回放
- 三子移动井字棋：三档 AI、本地双人，每方三颗棋，放满后移动
- 局域网联机双人：两台设备用 6 位房间代码对战五子棋或井字棋

## 项目结构

```text
.
├── app.py               # Flask 入口、页面路由、猜数字 API
├── online.py            # Socket.IO 联机房间与服务器端规则
├── games.html           # 游戏大厅
├── guess.html           # 猜数字
├── index.html           # AI 五子棋
├── tictactoe.html       # 三子移动井字棋
├── online.html          # 局域网联机双人页面
├── static/              # 浏览器端依赖
├── requirements.txt     # Python 依赖
└── tools/               # PPT 等辅助生成脚本
```

## 安装与启动

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

本机打开：

```text
http://127.0.0.1:8000/
```

同一局域网的其他设备打开：

```text
http://服务器局域网IP:8000/
```

查询服务器 IP：

```bash
hostname -I
```

如果运行在虚拟机中，通常需要使用桥接网络，且防火墙必须允许 TCP 8000。

## 主要路由

| 路由 | 功能 |
|---|---|
| `/` | 游戏大厅 |
| `/guess` | 猜数字 |
| `/gomoku` | AI／本地双人五子棋 |
| `/tictactoe` | AI／本地双人井字棋 |
| `/online` | 局域网联机双人 |

## 联机玩法

1. 两台设备连接同一个局域网。
2. 第一台打开 `/online`，选择游戏并建立房间。
3. 保持页面开启，把 6 位代码告诉第二位玩家。
4. 第二台打开相同网址并输入代码。
5. 房间创建者刷新或关闭页面后，房间会结束。

## 后续增加游戏

1. 新增一个 HTML 页面。
2. 在 `app.py` 加入页面路由。
3. 在 `games.html` 加入游戏卡片。
4. 若需实时联机，在 `online.py` 增加服务器端状态和规则。
5. 完成桌面、手机和双客户端测试后提交。
