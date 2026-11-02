"""Flask 网站：猜数字游戏与原有五子棋。"""
import os
import secrets
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_file, send_from_directory, session
from online import socketio

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
socketio.init_app(app)
app.config["LUXFATUM_INSTALLER"] = os.environ.get("LUXFATUM_INSTALLER", "")
DIFFICULTIES = {
    "easy": {"maximum": 50, "attempts": 12, "label": "简单"},
    "normal": {"maximum": 100, "attempts": 10, "label": "普通"},
    "hard": {"maximum": 500, "attempts": 9, "label": "困难"},
}


def start_game(difficulty="normal"):
    difficulty = difficulty if difficulty in DIFFICULTIES else "normal"
    config = DIFFICULTIES[difficulty]
    session.update(answer=secrets.randbelow(config["maximum"]) + 1,
                   attempts=0, finished=False, difficulty=difficulty)


@app.get("/")
def index():
    return send_from_directory(app.root_path, "games.html")


@app.get("/guess")
def guess_page():
    return send_from_directory(app.root_path, "guess.html")

@app.post("/api/new-game")
def new_game():
    difficulty = (request.get_json(silent=True) or {}).get("difficulty", "normal")
    start_game(difficulty)
    config = DIFFICULTIES[session["difficulty"]]
    return jsonify(message=f"{config['label']}模式：请输入 1 到 {config['maximum']} 的整数。",
                   attempts=0, remaining=config["attempts"], maximum=config["maximum"])


@app.post("/api/guess")
def guess():
    if "answer" not in session:
        start_game()
    config = DIFFICULTIES[session.get("difficulty", "normal")]
    if session.get("finished"):
        return jsonify(error="这一局已经结束，请开始新游戏。"), 409
    value = (request.get_json(silent=True) or {}).get("guess")
    if isinstance(value, bool) or not isinstance(value, int):
        return jsonify(error="请输入一个整数。"), 400
    if not 1 <= value <= config["maximum"]:
        return jsonify(error=f"数字必须在 1 到 {config['maximum']} 之间。"), 400
    session["attempts"] += 1
    attempts, answer = session["attempts"], session["answer"]
    remaining = config["attempts"] - attempts
    if value == answer:
        session["finished"] = True
        return jsonify(result="correct", message=f"答对了！答案就是 {answer}。", attempts=attempts, remaining=remaining)
    if remaining == 0:
        session["finished"] = True
        return jsonify(result="lost", message=f"次数用完了，正确答案是 {answer}。", attempts=attempts, remaining=0)
    direction = "大" if value > answer else "小"
    return jsonify(result="high" if value > answer else "low", message=f"{value} 太{direction}了，再试一次！", attempts=attempts, remaining=remaining)


@app.get("/online")
def online_game():
    response = send_from_directory(app.root_path, "online.html", max_age=0)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response

@app.get("/tictactoe")
def tictactoe():
    return send_from_directory(app.root_path, "tictactoe.html")


@app.get("/snake")
def snake():
    return send_from_directory(app.root_path, "snake.html")


@app.get("/2048")
def game_2048():
    return send_from_directory(app.root_path, "2048.html")


@app.get("/chess")
def chess():
    return send_from_directory(app.root_path, "chess.html")


@app.get("/gomoku")
def gomoku():
    return send_from_directory(app.root_path, "index.html")


@app.get("/tetris")
def tetris():
    return send_from_directory(app.root_path, "tetris.html")


@app.get("/breakout")
def breakout():
    return send_from_directory(app.root_path, "breakout.html")


@app.get("/minesweeper")
def minesweeper():
    return send_from_directory(app.root_path, "minesweeper.html")


@app.get("/luxfatum/download")
def download_luxfatum():
    installer = app.config.get("LUXFATUM_INSTALLER")
    if not installer:
        abort(404, description="LuxFatum installer is not configured.")
    installer_path = Path(installer).expanduser()
    if not installer_path.is_absolute():
        installer_path = Path(app.root_path) / installer_path
    if not installer_path.is_file():
        abort(404, description="LuxFatum installer is unavailable.")
    return send_file(installer_path, as_attachment=True)



if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True, allow_unsafe_werkzeug=True)
