"""AI 五子棋的 Flask 启动入口。"""

# 从 Flask 套件载入网站应用与静态文件传送功能。
from flask import Flask, send_from_directory

# 建立 Flask 应用；游戏源码只保留根目录这一份 index.html。
app = Flask(__name__)


# 将网站首页网址对应到五子棋页面。
@app.get("/")
def index():
    """显示五子棋游戏首页。"""
    # 直接传送唯一的 index.html，避免维护两份重复游戏代码。
    return send_from_directory(app.root_path, "index.html")


# 只有直接执行 app.py 时才启动开发服务器。
if __name__ == "__main__":
    # 监听所有网卡；同一局域网设备可使用「电脑 IP:8000」连接。
    app.run(host="0.0.0.0", port=8000, debug=True)
