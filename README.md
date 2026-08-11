# AI 五子棋

将多个五子棋 HTML 版本整合后的单一版本。直接用浏览器打开 `index.html` 即可游玩，不需要安装依赖或启动服务器。

## 功能

- 15 × 15 五子棋棋盘
- 玩家执黑，对战电脑白棋
- 攻守兼顾的棋型评分 AI
- AI 优先检查胜棋，并阻挡玩家即将形成的五连
- 每手 15 秒限时挑战与进度条
- 横、直、斜线五连胜负判断
- AI 落子原因提示
- 对局历史缩略棋盘
- 完整棋谱回放与滑杆控制
- 重新开始游戏

## 使用方式

1. 下载或 clone 这个仓库。
2. 使用 Chrome、Edge 或 Firefox 打开 `index.html`。
3. 点击棋盘空位落下黑棋，电脑会自动回应。

```bash
git clone https://github.com/sheng13/Gomoku-Versions.git
cd Gomoku-Versions
```

然后双击 `index.html` 即可。

## 项目结构

```text
Gomoku-Versions/
├── index.html    # 完整游戏，包含 HTML、CSS 与 JavaScript
└── README.md     # 项目说明
```

## 版本整理

