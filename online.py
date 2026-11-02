"""局域网实时双人房间：五子棋、三子移动井字棋与西洋棋。"""
import copy
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


def chess_board():
    return [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP"] * 8, *([[""] * 8 for _ in range(4)]), ["wP"] * 8,
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]


def reset_room(room):
    room["turn"], room["winner"], room["check"] = "X", None, False
    if room["game"] == "gomoku":
        room["board"] = [[""] * 15 for _ in range(15)]
    elif room["game"] == "tictactoe":
        room["board"], room["placed"] = [""] * 9, {"X": 0, "O": 0}
    else:
        room["board"] = chess_board()
        room["castle"] = {"X": {"k": True, "q": True}, "O": {"k": True, "q": True}}
        room["en_passant"] = None


def public_state(room):
    return {
        "code": room["code"], "game": room["game"], "board": room["board"],
        "turn": room["turn"], "started": len(room["players"]) == 2,
        "winner": room["winner"], "placed": room.get("placed"),
        "check": room.get("check", False),
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


def mark_color(mark):
    return "w" if mark == "X" else "b"


def color_mark(color):
    return "X" if color == "w" else "O"


def chess_inside(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def chess_attacked(room, board, row, col, by_mark):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and color_mark(piece[0]) == by_mark:
                if any(m["row"] == row and m["col"] == col
                       for m in chess_pseudo(room, board, r, c, attacks=True)):
                    return True
    return False


def chess_king(board, mark):
    target = mark_color(mark) + "K"
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return r, c
    return None


def chess_in_check(room, board, mark):
    king = chess_king(board, mark)
    return bool(king and chess_attacked(room, board, king[0], king[1], "O" if mark == "X" else "X"))


def chess_pseudo(room, board, row, col, attacks=False):
    piece = board[row][col]
    if not piece:
        return []
    color, kind = piece
    mark = color_mark(color)
    moves = []

    def add(r, c, **extra):
        if chess_inside(r, c) and (not board[r][c] or board[r][c][0] != color):
            moves.append({"row": r, "col": c, **extra})

    def slide(dr, dc):
        r, c = row + dr, col + dc
        while chess_inside(r, c):
            if not board[r][c]:
                moves.append({"row": r, "col": c})
            else:
                if board[r][c][0] != color:
                    moves.append({"row": r, "col": c})
                break
            r, c = r + dr, c + dc

    if kind == "P":
        direction = -1 if color == "w" else 1
        if attacks:
            for dc in (-1, 1):
                if chess_inside(row + direction, col + dc):
                    moves.append({"row": row + direction, "col": col + dc})
        else:
            if chess_inside(row + direction, col) and not board[row + direction][col]:
                moves.append({"row": row + direction, "col": col})
                home = 6 if color == "w" else 1
                if row == home and not board[row + direction * 2][col]:
                    moves.append({"row": row + direction * 2, "col": col})
            for dc in (-1, 1):
                r, c = row + direction, col + dc
                if chess_inside(r, c) and board[r][c] and board[r][c][0] != color:
                    moves.append({"row": r, "col": c})
                elif room.get("en_passant") == {"row": r, "col": c, "mark": "O" if mark == "X" else "X"}:
                    moves.append({"row": r, "col": c, "en_passant": True})
    elif kind == "N":
        for dr, dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
            add(row + dr, col + dc)
    elif kind in ("B", "R", "Q"):
        directions = []
        if kind in ("B", "Q"): directions += [(1,1),(1,-1),(-1,1),(-1,-1)]
        if kind in ("R", "Q"): directions += [(1,0),(-1,0),(0,1),(0,-1)]
        for direction in directions: slide(*direction)
    elif kind == "K":
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc: add(row + dr, col + dc)
        if not attacks and not chess_in_check(room, board, mark):
            opponent = "O" if mark == "X" else "X"
            for side, key, rook_col in ((1, "k", 7), (-1, "q", 0)):
                dest = col + side * 2
                clear = all(not board[row][c] for c in range(min(col, rook_col) + 1, max(col, rook_col)))
                rook = board[row][rook_col]
                if (room["castle"][mark][key] and rook == color + "R" and clear
                        and not chess_attacked(room, board, row, col + side, opponent)
                        and not chess_attacked(room, board, row, dest, opponent)):
                    moves.append({"row": row, "col": dest, "castle": True})
    return moves


def chess_apply_board(board, fr, fc, move, promotion="Q"):
    result = copy.deepcopy(board)
    piece = result[fr][fc]
    result[fr][fc] = ""
    if move.get("en_passant"):
        result[fr][move["col"]] = ""
    result[move["row"]][move["col"]] = piece
    if move.get("castle"):
        rook_from = 7 if move["col"] > fc else 0
        rook_to = move["col"] - 1 if move["col"] > fc else move["col"] + 1
        result[fr][rook_to], result[fr][rook_from] = result[fr][rook_from], ""
    if piece[1] == "P" and move["row"] in (0, 7):
        result[move["row"]][move["col"]] = piece[0] + promotion
    return result


def chess_legal_moves(room, row, col):
    piece = room["board"][row][col]
    if not piece:
        return []
    mark = color_mark(piece[0])
    return [move for move in chess_pseudo(room, room["board"], row, col)
            if not chess_in_check(room, chess_apply_board(room["board"], row, col, move), mark)]


def chess_has_moves(room, mark):
    color = mark_color(mark)
    return any(room["board"][r][c].startswith(color) and chess_legal_moves(room, r, c)
               for r in range(8) for c in range(8))


def update_castle_rights(room, piece, fr, fc, target, tr, tc):
    mark = color_mark(piece[0])
    if piece[1] == "K":
        room["castle"][mark] = {"k": False, "q": False}
    if piece[1] == "R":
        home = 7 if mark == "X" else 0
        if fr == home and fc in (0, 7): room["castle"][mark]["q" if fc == 0 else "k"] = False
    if target and target[1] == "R":
        victim = color_mark(target[0]); home = 7 if victim == "X" else 0
        if tr == home and tc in (0, 7): room["castle"][victim]["q" if tc == 0 else "k"] = False


@socketio.on("create_room")
def create_room(data):
    game = (data or {}).get("game")
    if game not in ("gomoku", "tictactoe", "chess"):
        return emit("game_error", {"message": "不支持的游戏。"})
    code = room_code()
    room = {"code": code, "game": game, "players": {request.sid: "X"}}
    reset_room(room)
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


@socketio.on("get_chess_moves")
def get_chess_moves(data):
    code = player_rooms.get(request.sid); room = rooms.get(code)
    if not room or room["game"] != "chess" or room["turn"] != room["players"].get(request.sid): return
    try:
        row, col = int(data["row"]), int(data["col"])
        piece = room["board"][row][col]
        if not piece or color_mark(piece[0]) != room["turn"]: raise ValueError
        emit("chess_moves", {"row": row, "col": col, "moves": chess_legal_moves(room, row, col)})
    except (KeyError, TypeError, ValueError, IndexError):
        emit("game_error", {"message": "无法选择这个棋子。"})


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
        elif room["game"] == "tictactoe":
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
        else:
            fr, fc, tr, tc = (int(data[k]) for k in ("from_row", "from_col", "to_row", "to_col"))
            if not all(0 <= value < 8 for value in (fr, fc, tr, tc)): raise ValueError
            piece = room["board"][fr][fc]
            if not piece or color_mark(piece[0]) != mark: raise ValueError
            move = next((m for m in chess_legal_moves(room, fr, fc) if m["row"] == tr and m["col"] == tc), None)
            if not move: raise ValueError
            promotion = str(data.get("promotion", "Q")).upper()
            if promotion not in ("Q", "R", "B", "N"): raise ValueError
            target = room["board"][tr][tc]
            update_castle_rights(room, piece, fr, fc, target, tr, tc)
            room["board"] = chess_apply_board(room["board"], fr, fc, move, promotion)
            room["en_passant"] = ({"row": (fr + tr) // 2, "col": fc, "mark": mark}
                                       if piece[1] == "P" and abs(tr - fr) == 2 else None)
    except (KeyError, TypeError, ValueError, IndexError):
        return emit("game_error", {"message": "这个移动不合法。"})
    if not room["winner"]:
        room["turn"] = "O" if mark == "X" else "X"
        if room["game"] == "chess":
            room["check"] = chess_in_check(room, room["board"], room["turn"])
            if not chess_has_moves(room, room["turn"]):
                room["winner"] = mark if room["check"] else "draw"
    socketio.emit("state", public_state(room), to=code)


@socketio.on("restart_online")
def restart_online():
    code = player_rooms.get(request.sid); room = rooms.get(code)
    if not room or len(room["players"]) != 2: return
    reset_room(room)
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
