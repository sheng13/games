# AI 五子棋代码注解指南

`index.html` 内已经针对 HTML 区块、CSS 元件、游戏状态、计时器、落子、AI、历史与回放加入行内注释。本文件补充各函数的输入、输出与副作用，阅读时可与原始代码对照。

## 页面与棋盘

- `createBoard()`：清空画面后建立 15 × 15 格子，并把点击事件绑定到 `playerMove()`。
- `board`：二维数组；`0` 是空格、`1` 是玩家黑子、`2` 是电脑白子。
- `moveList`：依顺序保存 `{r, c, player}`，是棋谱回放的唯一资料来源。
- `historyBoards`：保存最近五个棋盘快照，用于右侧缩略图。

## 开始、暂停与计时

- `startTimer(resetTime)`：`true` 开始新回合并重设 15 秒；`false` 从暂停时剩余秒数继续。
- `updateTimerUI()`：根据剩余比例改变进度条宽度，最后四秒改成红色。
- `handleTimeout()`：时间归零后结束游戏，并根据当前玩家判定胜负。
- `toggleGamePause()`：暂停时停止计时并禁止落子；继续时保留原本剩余时间。
- `resetGame()`：停止计时与回放、清空所有状态，并开始全新对局。

## 玩家与 AI

- `playerMove(r, c)`：检查格子、回合、暂停和回放状态，通过后落黑子并安排 AI 回合。
- `executeMove(r, c, player)`：同时更新资料、画面、历史与胜负状态。
- `checkWin(...)`：从最后落子向横、直与两条斜线计数，连续五子即获胜。
- `getCandidates(board)`：只挑选现有棋子附近的位置，减少 AI 搜索量。
- `scoreLine(line)`：按照成五、活四、冲四、活三等棋型计算分数。
- `evaluateBoard(board, player)`：扫描整盘四个方向，计算指定一方的局势分数。
- `findBestMove(board)`：先找 AI 必胜点，再阻挡玩家必胜点，最后比较攻守综合分数。
- `aiMove()`：取得最佳位置、落白子、显示原因，并把回合交还玩家。

## 历史与回放

- `saveHistory()`：每次落子后复制棋盘，最多保留最近五份缩略图。
- `drawHistory()`：把历史快照绘制成右侧小棋盘。
- `enterReplay()`：暂停真实对局后进入独立回放模式，防止背景继续计时或落子。
- `renderReplay()`：依 `replayIndex` 只画指定手数，不改变真实 `board`。
- `replayTo(index)`：跳到指定手数。
- `replayStep(delta)`：向前或向后浏览一手，并自动暂停播放。
- `replaySeek(value)`：回应滑杆变化。
- `replayToggle()`：开始或暂停每 0.6 秒播放一手的回放计时器。
- `exitReplay()`：回到最后一手真实棋局，并恢复进入回放前的暂停状态。

## 两种启动方式

### 直接打开

双击仓库根目录的 `index.html`，或访问 GitHub Pages。

### Python Flask

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
