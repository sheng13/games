"""局域网实时双人房间：五子棋与三子移动井字棋。"""
import secrets
from flask import request
from flask_socketio import SocketIO, emit, join_room

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")
rooms = {}
player_rooms = {}


def room_code():
    while True:
        code = f"{secrets.randbelow(1_000_000):06d}"
        if code not in rooms:
            return code


def public_state(room):
    return {
        "code": room["code"], "game": room["game"], "board": room["board"],
        "turn": room["turn"], "started": len(room["players"]) == 2,
        "winner": room["winner"], "placed": room.get("placed"),
    }


def gomoku_win(board, row, col, mark):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for sign in (1, -1):
            r, c = row + dr * sign, col + dc * sign
            while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == mark:
                count += 1; r += dr * sign; c += dc * sign
        if count >= 5:
            return True
    return False


def ttt_win(board, mark):
    return any(all(board[i] == mark for i in line) for line in (
        (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)))


@socketio.on("create_room")
def create_room(data):
    game = (data or {}).get("game")
    if game not in ("gomoku", "tictactoe"):
        return emit("game_error", {"message": "不支持的游戏。"})
    code = room_code()
    room = {"code": code, "game": game, "players": {request.sid: "X"},
            "turn": "X", "winner": None,
            "board": [[""] * 15 for _ in range(15)] if game == "gomoku" else [""] * 9}
    if game == "tictactoe": room["placed"] = {"X": 0, "O": 0}
    rooms[code] = room; player_rooms[request.sid] = code; join_room(code)
    emit("room_joined", {"player": "X", **public_state(room)})


@socketio.on("join_game")
def join_game(data):
    code = str((data or {}).get("code", "")).strip()
    room = rooms.get(code)
    if not room: return emit("game_error", {"message": "找不到这个房间。"})
    if len(room["players"]) >= 2: return emit("game_error", {"message": "房间已经满了。"})
    room["players"][request.sid] = "O"; player_rooms[request.sid] = code; join_room(code)
    emit("room_joined", {"player": "O", **public_state(room)})
    socketio.emit("state", public_state(room), to=code)


@socketio.on("make_move")
def make_move(data):
    code = player_rooms.get(request.sid); room = rooms.get(code)
    if not room or len(room["players"]) != 2: return emit("game_error", {"message": "请等待另一位玩家加入。"})
    mark = room["players"].get(request.sid)
    if room["winner"]: return emit("game_error", {"message": "这一局已经结束。"})
    if room["turn"] != mark: return emit("game_error", {"message": "还没轮到你。"})
    try:
        if room["game"] == "gomoku":
            row, col = int(data["row"]), int(data["col"])
            if not (0 <= row < 15 and 0 <= col < 15) or room["board"][row][col]: raise ValueError
            room["board"][row][col] = mark
            if gomoku_win(room["board"], row, col, mark): room["winner"] = mark
        else:
            to = int(data["to"]); source = data.get("from")
            if not 0 <= to < 9 or room["board"][to]: raise ValueError
            if room["placed"][mark] < 3:
                if source is not None: raise ValueError
                room["placed"][mark] += 1
            else:
                source = int(source)
                if not 0 <= source < 9 or room["board"][source] != mark: raise ValueError
                room["board"][source] = ""
            room["board"][to] = mark
            if ttt_win(room["board"], mark): room["winner"] = mark
    except (KeyError, TypeError, ValueError):
        return emit("game_error", {"message": "这个移动不合法。"})
    if not room["winner"]: room["turn"] = "O" if mark == "X" else "X"
    socketio.emit("state", public_state(room), to=code)


@socketio.on("restart_online")
def restart_online():
    code = player_rooms.get(request.sid); room = rooms.get(code)
    if not room or len(room["players"]) != 2: return
    room["turn"] = "X"; room["winner"] = None
    room["board"] = [[""] * 15 for _ in range(15)] if room["game"] == "gomoku" else [""] * 9
    if room["game"] == "tictactoe": room["placed"] = {"X": 0, "O": 0}
    socketio.emit("state", public_state(room), to=code)


@socketio.on("disconnect")
def disconnected():
    code = player_rooms.pop(request.sid, None); room = rooms.get(code)
    if not room: return
    room["players"].pop(request.sid, None)
    socketio.emit("opponent_left", {"message": "另一位玩家已离开房间。"}, to=code)
    rooms.pop(code, None)
    for sid, value in list(player_rooms.items()):
        if value == code: player_rooms.pop(sid, None)
