# AI 五子棋

将多个五子棋 HTML 版本整合后的单一版本。直接用浏览器打开 `index.html` 即可游玩，不需要安装依赖或启动服务器。

## 功能

- 15 × 15 五子棋棋盘
- 每局随机分配黑白棋，黑棋先手
- 攻守兼顾的棋型评分 AI
- AI 优先检查胜棋，并阻挡玩家即将形成的五连
- 每手 15 秒限时挑战与进度条
- 横、直、斜线五连胜负判断
- AI 落子原因提示
- 对局历史缩略棋盘
- 完整棋谱回放、单步、滑杆与返回棋局
- 开始／暂停／继续与重新开始
- 棋子落在标准网格线交叉点

## 使用方式

1. 下载或 clone 这个仓库。
2. 使用 Chrome、Edge 或 Firefox 打开 `index.html`。
3. 点击棋盘交叉点落子，电脑会自动回应。

```bash
git clone https://github.com/sheng13/Gomoku-Versions.git
cd Gomoku-Versions
```

然后双击 `index.html` 即可。

## 项目结构

```text
Gomoku-Versions/
├── index.html    # 唯一游戏源码
├── app.py        # Flask 与局域网入口
├── requirements.txt
├── CODE_WALKTHROUGH.md
├── AI五子棋_专案说明.pptx
└── README.md
```

只保留根目录 `index.html` 这一份最终游戏源码。直接打开、GitHub Pages 与 Python Flask 都使用相同文件。

## Python 与 IP 启动

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

本机打开 `http://127.0.0.1:8000/`；同一 Wi-Fi 的设备使用 `http://电脑IP:8000/`。

使用 `hostname -I` 查询电脑 IP。

## 版本整理

