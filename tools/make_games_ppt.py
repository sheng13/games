from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

ROOT = Path('/home/wsfoo/games')
OUT = ROOT / '小游戏网站_制作顺序.pptx'
prs = Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
NAVY=RGBColor(7,11,24); CARD=RGBColor(19,29,51); CYAN=RGBColor(103,232,249); PURPLE=RGBColor(167,139,250); WHITE=RGBColor(248,250,252); MUTED=RGBColor(174,187,208); GREEN=RGBColor(74,222,128); GOLD=RGBColor(250,204,21); RED=RGBColor(251,113,133)

def text(slide,x,y,w,h,value,size=20,color=WHITE,bold=False,align=PP_ALIGN.LEFT,font='Microsoft YaHei'):
    sh=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=sh.text_frame; tf.clear(); tf.word_wrap=True; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=tf.paragraphs[0]; p.text=value; p.alignment=align; p.font.name=font; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=color
    return sh

def rect(slide,x,y,w,h,fill=CARD,line=None,radius=True):
    sh=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h)); sh.fill.solid(); sh.fill.fore_color.rgb=fill; sh.line.color.rgb=line or fill; return sh

def base(title,num,subtitle=None):
    s=prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb=NAVY
    text(s,.65,.25,10.8,.55,title,28,WHITE,True); text(s,11.7,.25,.8,.5,f'{num:02}',16,CYAN,True,PP_ALIGN.RIGHT)
    bar=rect(s,.65,.9,1.1,.05,CYAN,CYAN,False)
    if subtitle:text(s,.65,1.0,12,.45,subtitle,14,MUTED)
    return s

def bullet_list(s,items,x,y,w,step=.72,size=20):
    for i,(head,body,color) in enumerate(items):
        text(s,x,y+i*step,.35,.5,'•',25,color,True)
        text(s,x+.36,y+i*step,w-.36,.5,head+'｜',size,color,True)
        text(s,x+1.75,y+i*step,w-1.75,.5,body,size,WHITE)

def code(s,x,y,w,h,lines):
    rect(s,x,y,w,h,RGBColor(3,7,18),RGBColor(51,65,85))
    text(s,x+.25,y+.15,w-.5,h-.3,lines,16,RGBColor(203,213,225),False,PP_ALIGN.LEFT,'DejaVu Sans Mono')

def card(s,x,y,w,h,icon,title,body,color=CYAN):
    rect(s,x,y,w,h,CARD,RGBColor(45,62,91)); text(s,x+.25,y+.2,.7,.65,icon,30,color,True,PP_ALIGN.CENTER)
    text(s,x+1,y+.18,w-1.25,.55,title,21,WHITE,True); text(s,x+.3,y+.92,w-.6,h-1.1,body,15,MUTED)

# 1
s=base('Python + HTML 小游戏网站',1,'从想法、页面、后端到测试与启动的完整制作顺序')
text(s,.75,1.65,7.3,1.35,'一个入口，三款游戏\n一套清楚的开发流程',38,WHITE,True)
text(s,.8,3.25,6.6,.65,'猜数字  ·  五子棋  ·  三子移动井字棋',20,CYAN,True)
for i,(ico,label,col) in enumerate([('🎯','猜数字',CYAN),('●','五子棋',GOLD),('X O','井字棋',PURPLE)]): card(s,8.3+i*1.45,1.75,1.25,3.4,ico,label,'',col)
text(s,.8,6.55,11.8,.4,'项目目录：/home/wsfoo/games',14,MUTED)

# 2
s=base('制作顺序总览',2,'先搭骨架，再逐个完成游戏，最后统一测试')
steps=[('1','规划',CYAN),('2','后端',PURPLE),('3','大厅',GREEN),('4','游戏',GOLD),('5','AI',RED),('6','测试',CYAN)]
for i,(n,label,col) in enumerate(steps):
    x=.7+i*2.08; rect(s,x,2.15,1.55,1.45,CARD,col); text(s,x+.15,2.28,1.25,.55,n,28,col,True,PP_ALIGN.CENTER); text(s,x+.15,2.9,1.25,.4,label,17,WHITE,True,PP_ALIGN.CENTER)
    if i<5:text(s,x+1.58,2.58,.48,.4,'→',25,MUTED,True,PP_ALIGN.CENTER)
text(s,1.0,4.45,11.3,1.05,'需求 → 文件结构 → Flask 路由 → HTML/CSS 页面 → JavaScript 规则与 AI → 浏览器测试',23,WHITE,True,PP_ALIGN.CENTER)
text(s,1.2,5.75,10.9,.55,'原则：每完成一层就先验证，再继续加下一层。',18,CYAN,True,PP_ALIGN.CENTER)

#3
s=base('第 1 步｜规划功能与文件',3,'先决定每个文件只负责一件事')
files=[('app.py','Flask 入口、页面路由、猜数字 API',PURPLE),('games.html','游戏大厅与选择入口',CYAN),('guess.html','猜数字操作页面',GREEN),('index.html','五子棋规则、AI、回放',GOLD),('tictactoe.html','三子移动井字棋、双人和 AI',RED)]
bullet_list(s,files,.85,1.45,11.7,.86,18)
code(s,7.7,5.55,4.8,1.05,'games/\n├─ app.py     ├─ games.html\n├─ guess.html ├─ index.html\n└─ tictactoe.html')
text(s,.85,5.65,6.2,.8,'先有清楚结构，后续增加游戏时只需新增页面与路由。',19,WHITE,True)

#4
s=base('第 2 步｜建立 Flask 网站骨架',4,'Python 负责接收网址请求，并把正确页面送给浏览器')
code(s,.75,1.4,5.7,4.8,"from flask import Flask, send_from_directory\n\napp = Flask(__name__)\n\n@app.get('/')\ndef index():\n    return send_from_directory(\n        app.root_path, 'games.html'\n    )\n\napp.run(port=8000, debug=True)")
card(s,7.0,1.45,5.45,1.15,'1','浏览器请求','GET http://127.0.0.1:8000/',CYAN)
card(s,7.0,3.0,5.45,1.15,'2','Flask 选择路由','/、/guess、/gomoku、/tictactoe',PURPLE)
card(s,7.0,4.55,5.45,1.15,'3','返回 HTML','浏览器显示对应游戏页面',GREEN)

#5
s=base('第 3 步｜制作游戏大厅',5,'首页只负责选择，不把所有游戏塞进同一个页面')
for i,(ico,title,path,col) in enumerate([('🎯','猜数字','/guess',CYAN),('●','五子棋','/gomoku',GOLD),('X O','井字棋','/tictactoe',PURPLE)]):
    x=.65+i*4.18; rect(s,x,1.55,3.75,3.55,CARD,col); text(s,x+.3,1.85,3.15,.75,ico,34,col,True,PP_ALIGN.CENTER); text(s,x+.3,2.75,3.15,.55,title,24,WHITE,True,PP_ALIGN.CENTER); text(s,x+.3,3.55,3.15,.45,path,17,MUTED,False,PP_ALIGN.CENTER); rect(s,x+.8,4.35,2.15,.5,col,col); text(s,x+.85,4.36,2.05,.42,'开始游戏',15,NAVY,True,PP_ALIGN.CENTER)
text(s,.8,5.75,11.7,.75,'所有游戏都有「返回游戏大厅」按钮，让网站形成完整导航。',21,CYAN,True,PP_ALIGN.CENTER)

#6
s=base('第 4 步｜完成猜数字',6,'这个游戏同时示范前端页面与 Python API 的合作')
# flow
labels=[('选择难度','HTML'),('建立新局','POST /api/new-game'),('提交数字','POST /api/guess'),('返回提示','太大／太小／答对')]
for i,(a,b) in enumerate(labels):
    x=.55+i*3.15; rect(s,x,1.55,2.65,1.25,CARD,[CYAN,PURPLE,GOLD,GREEN][i]); text(s,x+.18,1.72,2.3,.4,a,19,WHITE,True,PP_ALIGN.CENTER); text(s,x+.18,2.18,2.3,.35,b,13,MUTED,False,PP_ALIGN.CENTER)
    if i<3:text(s,x+2.67,1.92,.45,.4,'→',25,MUTED,True,PP_ALIGN.CENTER)
bullet_list(s,[('简单','1～50，12 次机会',GREEN),('普通','1～100，10 次机会',GOLD),('困难','1～500，9 次机会',RED)],1.0,3.55,5.3,.72,18)
code(s,7.0,3.38,5.4,2.3,"session['answer'] = 随机答案\nsession['attempts'] += 1\n\n猜小 → low\n猜大 → high\n相同 → correct")

#7
s=base('第 5 步｜完成五子棋',7,'棋盘、规则、AI 与回放都在浏览器端即时运行')
items=[('棋盘','建立 15 × 15 点击格与黑白棋状态',CYAN),('规则','从横、直、两条斜线检查连续五子',GREEN),('模式','人机对战／本地双人',PURPLE),('难度','随机 → 基础攻防 → 棋形综合评分',GOLD),('回放','保存每一步，支持滑杆、播放和悬浮预览',RED)]
bullet_list(s,items,.75,1.35,7.0,.83,18)
# mini board
for r in range(7):
    for c in range(7):
        q=s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.35+c*.48), Inches(1.55+r*.48), Inches(.34), Inches(.34)); q.fill.solid(); q.fill.fore_color.rgb=RGBColor(10,10,12) if (r==3 or c==3) and (r+c)%2 else WHITE; q.line.color.rgb=GOLD
text(s,8.25,5.3,3.6,.6,'历史记录 → 独立浮层放大',17,GOLD,True,PP_ALIGN.CENTER)

#8
s=base('第 6 步｜完成三子移动井字棋',8,'先放满三颗棋，再选择自己的棋移动到空格')
for i,(n,label,col) in enumerate([('1','放置 X／O',CYAN),('2','各有三颗',PURPLE),('3','选中棋子',GOLD),('4','移动到空格',GREEN),('5','判断三连',RED)]):
    x=.55+i*2.55; rect(s,x,1.55,2.15,1.35,CARD,col); text(s,x+.1,1.7,1.95,.45,n,24,col,True,PP_ALIGN.CENTER); text(s,x+.1,2.3,1.95,.35,label,15,WHITE,True,PP_ALIGN.CENTER)
text(s,.8,3.65,4.0,.55,'本地双人',23,CYAN,True); text(s,4.3,3.65,8.0,.55,'X 与 O 在同一设备轮流操作',18,WHITE)
text(s,.8,4.45,4.0,.55,'人机模式',23,PURPLE,True); text(s,4.3,4.45,8.0,.55,'玩家是 X，电脑是 O',18,WHITE)
text(s,.8,5.25,4.0,.55,'困难 AI',23,GOLD,True); text(s,4.3,5.25,8.0,.55,'Minimax 多步搜索 + Alpha-Beta 剪枝',18,WHITE)

#9
s=base('第 7 步｜设计三种 AI 难度',9,'难度差异来自决策深度，不只是改名称')
for i,(title,body,col) in enumerate([('简单','随机选择合法位置\n适合第一次玩',GREEN),('普通','先求胜、再阻挡\n加入基础位置偏好',GOLD),('困难','评估多步后续局面\n选择综合分最高动作',RED)]):
    x=.75+i*4.2; rect(s,x,1.55,3.75,3.85,CARD,col); text(s,x+.3,1.85,3.15,.6,title,27,col,True,PP_ALIGN.CENTER); text(s,x+.4,2.75,2.95,1.3,body,19,WHITE,False,PP_ALIGN.CENTER); text(s,x+.4,4.45,2.95,.4,['随机','即时攻防','搜索／评分'][i],16,MUTED,True,PP_ALIGN.CENTER)
text(s,.8,5.95,11.7,.55,'双人模式不需要 AI，因此页面会隐藏难度选择。',19,CYAN,True,PP_ALIGN.CENTER)

#10
s=base('第 8 步｜测试与除错',10,'每次修改都检查页面、路由、API 和浏览器脚本')
bullet_list(s,[('Python 语法','python3 -m py_compile app.py',CYAN),('路由测试','/、/guess、/gomoku、/tictactoe 都应返回 200',GREEN),('API 测试','确认三种猜数字范围与次数正确',PURPLE),('JS 语法','node --check 检查三个游戏脚本',GOLD),('实际操作','测试模式切换、胜负、回放与返回按钮',RED)],.8,1.4,11.8,.82,18)
code(s,1.0,5.75,11.2,.7,'测试结果：Routes, difficulty APIs, and JavaScript syntax passed')

#11
s=base('启动网站与继续扩充',11,'完成后用虚拟环境启动，浏览器从游戏大厅进入')
code(s,.85,1.45,5.75,3.3,'cd /home/wsfoo/games\npython3 -m venv .venv\nsource .venv/bin/activate\npython3 -m pip install -r requirements.txt\npython3 app.py')
card(s,7.1,1.5,5.25,1.25,'①','打开网站','http://127.0.0.1:8000/',CYAN)
card(s,7.1,3.15,5.25,1.25,'②','选择游戏','大厅进入三款游戏',PURPLE)
card(s,7.1,4.8,5.25,1.25,'③','下一步扩充','音效、战绩、线上双人、账号系统',GREEN)
text(s,.9,6.35,11.5,.45,'开发顺序：先能运行 → 再补规则 → 再做 AI → 最后优化画面与体验',18,GOLD,True,PP_ALIGN.CENTER)


# 12
s=base('关键程序代码地图',12,'知道功能在哪个文件，修改时才不会迷路')
items=[('Flask 路由','app.py：@app.get 把网址连接到 HTML 页面',PURPLE),('猜数字后端','app.py：start_game、new_game、guess',CYAN),('前端 API','guess.html：fetch() 发送难度和玩家猜测',GREEN),('五子棋核心','index.html：checkWin、findBestMove、drawHistory',GOLD),('井字棋核心','tictactoe.html：moves、minimax、computerTurn',RED)]
bullet_list(s,items,.8,1.35,11.8,.82,18)
code(s,1.0,5.75,11.2,.7,"查找代码：rg -n \"函数名称或网址\" app.py *.html")

# 13
s=base('程序代码怎样互相合作',13,'猜数字是最完整的前端 → 后端 → 前端范例')
code(s,.7,1.35,5.9,4.8,"// guess.html\nconst response = await fetch('/api/guess', {\n  method: 'POST',\n  headers: {'Content-Type':'application/json'},\n  body: JSON.stringify({guess: value})\n});\nconst data = await response.json();\nmessage.textContent = data.message;")
code(s,6.9,1.35,5.75,4.8,"# app.py\n@app.post('/api/guess')\ndef guess():\n    value = request.json['guess']\n    answer = session['answer']\n    if value < answer:\n        return jsonify(result='low')\n    if value > answer:\n        return jsonify(result='high')\n    return jsonify(result='correct')")
text(s,1.0,6.4,11.3,.45,'浏览器送 JSON → Flask 判断 → Flask 回 JSON → JavaScript 更新画面',18,CYAN,True,PP_ALIGN.CENTER)

# 14
s=base('正式上架网站｜GitHub + Render',14,'这个项目有 Flask API，不能只使用纯静态 GitHub Pages')
steps=[('1','上传 GitHub','把 app.py、HTML、requirements.txt 推到仓库',CYAN),('2','建立 Web Service','Render → New → Web Service → 连接仓库',PURPLE),('3','设置构建','pip install -r requirements.txt',GOLD),('4','设置启动','gunicorn app:app',GREEN),('5','设置密钥','环境变量 SECRET_KEY＝随机长字符串',RED),('6','完成发布','取得 https://名称.onrender.com',CYAN)]
for i,(n,title,body,col) in enumerate(steps):
    row=i//3; col_i=i%3; x=.55+col_i*4.25; y=1.35+row*2.2
    rect(s,x,y,3.85,1.75,CARD,col); text(s,x+.2,y+.14,.45,.45,n,20,col,True,PP_ALIGN.CENTER); text(s,x+.75,y+.12,2.8,.45,title,19,WHITE,True); text(s,x+.25,y+.72,3.35,.75,body,14,MUTED)
text(s,.75,6.05,11.8,.45,'requirements.txt 必须包含 Flask 与 gunicorn；每次推送 main 分支可自动重新部署。',17,GOLD,True,PP_ALIGN.CENTER)
text(s,.75,6.6,11.8,.3,'资料依据：Render 官方 Deploy a Flask App 文档（render.com/docs/deploy-flask）',11,MUTED,False,PP_ALIGN.CENTER)


# 15
s=base('基础知识｜HTML、CSS、JavaScript、Python',15,'四种技术各自负责不同工作')
for i,(title,body,col) in enumerate([('HTML','页面结构：标题、按钮、棋盘、表单',CYAN),('CSS','颜色、尺寸、排版、响应式与动画',PURPLE),('JavaScript','点击事件、游戏状态、规则、AI、更新画面',GOLD),('Python / Flask','网址路由、API、随机答案、Session',GREEN)]):
    x=.55+i*3.17; rect(s,x,1.4,2.8,3.9,CARD,col); text(s,x+.25,1.7,2.3,.55,title,23,col,True,PP_ALIGN.CENTER); text(s,x+.3,2.65,2.2,1.65,body,18,WHITE,False,PP_ALIGN.CENTER)
text(s,.8,5.85,11.7,.75,'浏览器执行 HTML + CSS + JavaScript；服务器执行 Python。',22,CYAN,True,PP_ALIGN.CENTER)

# 16
s=base('HTML 页面结构详解',16,'语义清楚的结构更容易维护，也有利于无障碍使用')
code(s,.65,1.25,6.0,5.3,"<!doctype html>\n<html lang=\"zh-Hans\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\"\n        content=\"width=device-width\">\n  <title>小游戏大厅</title>\n</head>\n<body>\n  <main>\n    <h1>小游戏大厅</h1>\n    <a href=\"/guess\">猜数字</a>\n  </main>\n</body>\n</html>")
bullet_list(s,[('head','放网页设定，不直接显示在页面主体',CYAN),('body','浏览器实际显示的内容',PURPLE),('main','页面最主要的内容区域',GREEN),('a href','点击后前往另一个网址',GOLD),('viewport','让页面在手机上正确缩放',RED)],7.0,1.35,5.5,.9,17)

# 17
s=base('CSS 排版与响应式详解',17,'同一份页面要同时适应电脑、平板和手机')
code(s,.7,1.35,5.75,4.95,".games {\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  gap: 24px;\n}\n\n@media (max-width: 650px) {\n  .games {\n    grid-template-columns: 1fr;\n  }\n}\n\n.game:hover {\n  transform: translateY(-7px);\n}")
bullet_list(s,[('Grid','把游戏卡片排成整齐栏位',CYAN),('gap','控制卡片之间的距离',PURPLE),('媒体查询','屏幕较窄时切成单栏',GREEN),('hover','鼠标经过时提供反馈',GOLD),('clamp/min/max','让尺寸随屏幕弹性变化',RED)],7.0,1.4,5.5,.88,17)

# 18
s=base('JavaScript 状态与事件',18,'游戏不是靠重新载入页面，而是修改状态后重新绘制')
code(s,.7,1.3,5.85,4.9,"let over = false;\nlet currentPlayer = 'X';\n\nbutton.addEventListener('click', () => {\n  if (over) return;\n  placePiece();\n  checkWinner();\n  render();\n});\n\nfunction render() {\n  status.textContent =\n    `轮到 ${currentPlayer}`;\n}")
bullet_list(s,[('状态','记录棋盘、当前玩家、剩余次数和胜负',CYAN),('事件','用户点击、选择模式、按重新开始',PURPLE),('规则','判断这次操作是否合法',GREEN),('渲染','把最新状态显示到 HTML',GOLD),('保护条件','游戏结束或 AI 思考时禁止重复点击',RED)],7.0,1.35,5.55,.9,17)

# 19
s=base('Flask 应用结构详解',19,'装饰器把 URL 与 Python 函数连接起来')
code(s,.7,1.3,6.0,5.1,"app = Flask(__name__)\n\n@app.get('/')\ndef index():\n    return send_from_directory(\n        app.root_path, 'games.html')\n\n@app.get('/guess')\ndef guess_page():\n    return send_from_directory(\n        app.root_path, 'guess.html')\n\n@app.post('/api/guess')\ndef guess():\n    return jsonify(result='low')")
bullet_list(s,[('GET','读取页面或资料；打开网址时使用',CYAN),('POST','提交玩家输入；不会放在网址列',PURPLE),('send_from_directory','安全地传送项目中的 HTML',GREEN),('jsonify','把 Python 数据转换成 JSON 回应',GOLD),('app.root_path','取得 app.py 所在项目目录',RED)],7.15,1.35,5.3,.9,17)

# 20
s=base('HTTP 请求与 JSON 流程',20,'浏览器与服务器通过请求／回应交换资料')
labels=[('浏览器','{ "guess": 42 }',CYAN),('POST /api/guess','Content-Type: application/json',PURPLE),('Flask','读取 request.get_json()',GOLD),('判断答案','比较 session 中的 answer',RED),('JSON 回应','{ "result": "low" }',GREEN)]
for i,(a,b,col) in enumerate(labels):
    x=.35+i*2.58; rect(s,x,1.55,2.2,1.55,CARD,col); text(s,x+.12,1.75,1.95,.4,a,18,col,True,PP_ALIGN.CENTER); text(s,x+.15,2.3,1.9,.45,b,12,WHITE,False,PP_ALIGN.CENTER)
    if i<4:text(s,x+2.2,2.05,.38,.4,'→',22,MUTED,True,PP_ALIGN.CENTER)
code(s,1.0,4.0,11.3,1.85,"fetch('/api/guess', {\n  method: 'POST', headers: {'Content-Type':'application/json'},\n  body: JSON.stringify({guess: Number(input.value)})\n}).then(response => response.json())")
text(s,1.0,6.25,11.3,.4,'HTTP 状态码：200 成功｜400 输入错误｜409 游戏已经结束',17,CYAN,True,PP_ALIGN.CENTER)

# 21
s=base('Session 与答案安全',21,'猜数字答案放在服务器 Session，不直接写进网页 JavaScript')
code(s,.7,1.35,5.8,4.7,"app.secret_key = os.environ.get(\n    'SECRET_KEY', secrets.token_hex(32))\n\ndef start_game():\n    session.update(\n        answer=secrets.randbelow(100)+1,\n        attempts=0,\n        finished=False\n    )")
bullet_list(s,[('为什么','若答案写在 HTML，玩家查看源码就能看到',CYAN),('Session','每个浏览器拥有各自独立的游戏资料',PURPLE),('签名','SECRET_KEY 防止客户端任意修改 Session',GREEN),('生产环境','在托管平台设置固定随机长密钥',GOLD),('注意','不要把真正密钥提交到 GitHub',RED)],7.0,1.35,5.55,.9,17)

# 22
s=base('猜数字后端规则逐步拆解',22,'先验证输入，再增加次数，最后判断胜负')
steps=[('1','确认游戏存在','没有答案就自动 start_game()',CYAN),('2','验证资料类型','必须是整数，bool 也要排除',PURPLE),('3','验证数字范围','根据难度检查 maximum',GOLD),('4','增加猜测次数','attempts += 1',GREEN),('5','比较答案','low / high / correct',RED),('6','结束条件','猜中或剩余次数为 0',CYAN)]
for i,(n,a,b,col) in enumerate(steps):
    row=i//3; c=i%3; x=.55+c*4.25; y=1.35+row*2.25
    rect(s,x,y,3.85,1.72,CARD,col); text(s,x+.2,y+.18,.45,.42,n,19,col,True,PP_ALIGN.CENTER); text(s,x+.75,y+.14,2.8,.45,a,18,WHITE,True); text(s,x+.3,y+.78,3.25,.55,b,14,MUTED)
text(s,.8,6.1,11.7,.45,'错误输入不消耗机会；合法猜测才会增加 attempts。',18,GOLD,True,PP_ALIGN.CENTER)

# 23
s=base('五子棋棋盘数据结构',23,'画面是 DOM 网格，真正规则依据二维数组')
code(s,.65,1.35,5.7,4.8,"const BOARD_SIZE = 15;\nlet board = Array(BOARD_SIZE)\n  .fill(null)\n  .map(() => Array(BOARD_SIZE).fill(0));\n\n// 0 = 空格\n// 1 = 黑棋\n// 2 = 白棋\n\nboard[row][column] = currentPlayer;")
card(s,6.85,1.4,5.6,1.2,'①','读取点击位置','playerMove(row, column)',CYAN)
card(s,6.85,2.95,5.6,1.2,'②','更新状态','board[row][column] = 玩家',PURPLE)
card(s,6.85,4.5,5.6,1.2,'③','更新画面','在对应 cell 加入棋子元素',GREEN)
text(s,.8,6.4,11.7,.4,'规则只读取 board，不依赖棋子颜色或画面位置。',17,GOLD,True,PP_ALIGN.CENTER)

# 24
s=base('五子棋胜负判断算法',24,'从最后一颗棋向两个相反方向统计连续棋子')
code(s,.65,1.3,6.25,5.2,"const dirs = [\n  [0,1],   // 横线\n  [1,0],   // 直线\n  [1,1],   // 左上到右下\n  [1,-1]   // 右上到左下\n];\n\nfor (const [dr, dc] of dirs) {\n  let count = 1;\n  count += countForward(dr, dc);\n  count += countBackward(dr, dc);\n  if (count >= 5) return true;\n}")
bullet_list(s,[('为什么从最后一手查','只有新落子可能产生新的五连',CYAN),('两个方向','横线要同时检查左边和右边',PURPLE),('边界检查','row/column 不可超出 0～14',GREEN),('停止条件','遇到空格、对手棋或边界就停止',GOLD),('复杂度','只检查四条线，速度很快',RED)],7.25,1.35,5.1,.9,16)

# 25
s=base('五子棋 AI 棋形评分',25,'困难模式用候选点与棋形分数平衡进攻和防守')
patterns=[('11111','成五',1000000,RED),('011110','活四',100000,GOLD),('11110','冲四',50000,PURPLE),('001110','活三',1000,CYAN),('001100','活二',100,GREEN)]
for i,(pat,name,val,col) in enumerate(patterns):
    y=1.35+i*.88; rect(s,.8,y,2.2,.6,CARD,col); text(s,.95,y+.05,1.9,.45,pat,20,col,True,PP_ALIGN.CENTER); text(s,3.25,y,2.0,.6,name,18,WHITE,True); text(s,5.0,y,2.0,.6,f'{val:,} 分',17,MUTED)
code(s,7.25,1.35,5.2,3.65,"combined = attackScore\n         + defenseScore * 1.1\n\n候选点：只检查已有棋子\n周围两格内的空位\n\n优先级：\n1. 自己立即成五\n2. 阻挡对手成五\n3. 综合棋形评分")
text(s,.9,6.15,11.5,.45,'候选点缩小搜索范围，避免每回合重复评估全部 225 个位置。',17,CYAN,True,PP_ALIGN.CENTER)

# 26
s=base('五子棋历史与回放实现',26,'保存每一步状态，回放时只渲染副本，不改变真实对局')
code(s,.65,1.3,5.8,4.95,"moveList.push({ r, c, player });\n\nfunction replayTo(step) {\n  const temp = emptyBoard();\n  for (let i=0; i<step; i++) {\n    const m = moveList[i];\n    temp[m.r][m.c] = m.player;\n  }\n  renderReplay(temp);\n}\n\n// 滑杆改变 step\n// 定时器每 0.6 秒前进一步")
bullet_list(s,[('记录','每次合法落子保存列、栏与玩家',CYAN),('重建','从空棋盘依序应用前 N 手',PURPLE),('播放','setInterval 自动增加 replayIndex',GREEN),('暂停真实局','回放期间禁止真实棋盘落子',GOLD),('悬浮预览','克隆历史棋盘到独立浮层，避免裁切',RED)],6.9,1.35,5.6,.9,16)

# 27
s=base('三子移动井字棋状态机',27,'放置阶段和移动阶段使用不同合法操作')
labels=[('开始','X 回合',CYAN),('放置阶段','每方少于 3 颗',PURPLE),('移动阶段','先选己方棋子',GOLD),('选择空格','移动棋子',GREEN),('判断三连','胜利或换人',RED)]
for i,(a,b,col) in enumerate(labels):
    x=.35+i*2.58; rect(s,x,1.45,2.18,1.45,CARD,col); text(s,x+.15,1.65,1.88,.4,a,18,col,True,PP_ALIGN.CENTER); text(s,x+.15,2.2,1.88,.35,b,13,WHITE,False,PP_ALIGN.CENTER)
    if i<4:text(s,x+2.18,1.95,.4,.4,'→',22,MUTED,True,PP_ALIGN.CENTER)
code(s,.9,3.75,5.55,2.15,"placed = { X: 0, O: 0 };\nselected = null;\ncurrent = 'X';\n\nif (placed[mark] < 3) place();\nelse selectThenMove();")
code(s,6.9,3.75,5.55,2.15,"合法移动 = { from, to }\n\nfrom = null → 放置新棋\nfrom = 位置 → 移动旧棋\nto 必须是空格")

# 28
s=base('Minimax 与 Alpha-Beta 剪枝',28,'困难井字棋 AI 模拟双方未来动作，再选择最安全路线')
card(s,.7,1.35,3.7,1.15,'MAX','电脑 O','寻找最高分动作',PURPLE)
card(s,4.82,1.35,3.7,1.15,'MIN','玩家 X','假设玩家选择最低分动作',CYAN)
card(s,8.95,1.35,3.7,1.15,'CUT','剪枝','跳过不可能更好的分支',GOLD)
code(s,.75,3.05,5.75,2.95,"function minimax(board, turn, depth) {\n  if (结束 || depth === 0)\n    return evaluate(board);\n\n  for (const move of legalMoves)\n    score = minimax(nextBoard,\n                    otherTurn, depth-1);\n}")
bullet_list(s,[('终局分','电脑胜为正分，玩家胜为负分',GREEN),('启发式','未结束时评估两连、中心和威胁',PURPLE),('深度限制','移动阶段可能循环，因此只搜索固定层数',GOLD),('Alpha-Beta','已经确定更差的分支无需继续计算',RED)],7.0,3.05,5.35,.72,15)

# 29
s=base('Git 版本管理与上传 GitHub',29,'先把本地代码保存成版本，再连接远端仓库')
code(s,.7,1.25,6.0,5.3,"cd /home/wsfoo/games\n\ngit status\ngit add app.py requirements.txt *.html\ngit commit -m \"Add three web games\"\n\n# 在 GitHub 建立空仓库后\ngit remote add origin \\\n  https://github.com/账号/games.git\ngit branch -M main\ngit push -u origin main")
bullet_list(s,[('.gitignore','排除 .venv、缓存、日志和本机密钥',CYAN),('先看 status','确认没有把不该上传的文件加入',PURPLE),('小步 commit','每完成一个功能就保存一个版本',GREEN),('不要上传密钥','SECRET_KEY 应放托管平台环境变量',GOLD),('自动部署','Render 可监看 main 分支的新提交',RED)],7.1,1.3,5.25,.92,16)

# 30
s=base('Render 部署逐项设置',30,'建立 Web Service 时照表填写')
settings=[('Service Type','Web Service',CYAN),('Runtime','Python 3',PURPLE),('Build Command','pip install -r requirements.txt',GOLD),('Start Command','gunicorn app:app',GREEN),('Environment','SECRET_KEY＝随机长字符串',RED),('Health Check Path','/',CYAN)]
for i,(a,b,col) in enumerate(settings):
    y=1.15+i*.82; rect(s,.75,y,3.2,.62,CARD,col); text(s,.95,y+.05,2.8,.45,a,16,col,True); rect(s,4.2,y,8.35,.62,RGBColor(3,7,18),RGBColor(51,65,85)); text(s,4.4,y+.05,7.9,.45,b,16,WHITE,False,font='DejaVu Sans Mono' if 'Command' in a else 'Microsoft YaHei')
text(s,.8,6.35,11.7,.38,'部署成功后取得 onrender.com 网址；可再到 Settings 绑定自己的网域。',17,GOLD,True,PP_ALIGN.CENTER)

# 31
s=base('为什么不能只用 GitHub Pages',31,'静态托管与 Python Web Service 的能力不同')
rect(s,.75,1.35,5.7,4.8,CARD,CYAN); text(s,1.0,1.65,5.2,.55,'GitHub Pages',25,CYAN,True,PP_ALIGN.CENTER)
bullet_list(s,[('可以','显示 HTML、CSS、JavaScript',GREEN),('可以','运行浏览器端五子棋与井字棋',GREEN),('不可以','执行 app.py 或 Flask API',RED),('结果','猜数字后端功能无法使用',GOLD)],1.15,2.45,4.9,.72,16)
rect(s,6.85,1.35,5.7,4.8,CARD,PURPLE); text(s,7.1,1.65,5.2,.55,'Render Web Service',25,PURPLE,True,PP_ALIGN.CENTER)
bullet_list(s,[('可以','安装 requirements.txt',GREEN),('可以','运行 Flask + Gunicorn',GREEN),('可以','处理 /api/guess 请求',GREEN),('适合','当前完整小游戏网站',CYAN)],7.25,2.45,4.9,.72,16)

# 32
s=base('常见错误与解决方法',32,'看到错误先判断发生在安装、端口、路径还是部署阶段')
items=[('externally-managed-environment','使用 python3 -m venv .venv，不要破坏系统 Python',RED),('ModuleNotFoundError: flask','启用虚拟环境后 pip install -r requirements.txt',PURPLE),('Address already in use','关闭旧 8000 进程，或换成 8001 端口',GOLD),('页面 404','检查 Flask 路由与 HTML 文件名是否一致',CYAN),('改目录后 venv 失效','重新建立 .venv，因为激活脚本包含旧绝对路径',GREEN),('Render 启动失败','查看日志，并确认 gunicorn app:app 与依赖文件',RED)]
bullet_list(s,items,.65,1.25,12,.82,16)

# 33
s=base('上线前检查清单',33,'逐项通过后再公开网址')
checks=[('□','所有页面返回 200',CYAN),('□','三种游戏可以返回大厅',PURPLE),('□','简单／普通／困难模式正常',GOLD),('□','双人模式不会触发 AI',GREEN),('□','手机宽度没有横向溢出',RED),('□','SECRET_KEY 未写进 GitHub',CYAN),('□','requirements.txt 包含 Flask 与 gunicorn',PURPLE),('□','Render 日志没有异常',GOLD),('□','重新部署后网址仍可打开',GREEN)]
for i,(mark,label,col) in enumerate(checks):
    row=i//3;c=i%3;x=.65+c*4.2;y=1.3+row*1.65;rect(s,x,y,3.8,1.25,CARD,col);text(s,x+.2,y+.25,.55,.55,mark,24,col,True,PP_ALIGN.CENTER);text(s,x+.85,y+.2,2.65,.7,label,16,WHITE,True)

# 34
s=base('后续扩充路线',34,'先从资料保存开始，再进入真正线上多人功能')
road=[('阶段 1','音效、主题、教学提示','纯前端改善',CYAN),('阶段 2','胜负统计、排行榜','数据库 SQLite / PostgreSQL',PURPLE),('阶段 3','注册、登录、个人战绩','账号与密码安全',GOLD),('阶段 4','线上双人房间','WebSocket / Flask-SocketIO',GREEN),('阶段 5','部署监控与自动测试','CI/CD、日志、健康检查',RED)]
for i,(a,b,c,col) in enumerate(road):
    y=1.2+i*1.05;rect(s,.8,y,2.0,.72,CARD,col);text(s,1.0,y+.1,1.6,.45,a,17,col,True,PP_ALIGN.CENTER);text(s,3.1,y,4.0,.72,b,18,WHITE,True);text(s,7.35,y,4.9,.72,c,16,MUTED)
text(s,.9,6.55,11.5,.35,'建议顺序：先完成数据库，再做账号，最后才做线上即时对战。',16,CYAN,True,PP_ALIGN.CENTER)

# 35
s=base('学习与讲解建议',35,'如何用这份 PPT 实际做一次完整展示')
bullet_list(s,[('第一段','先展示游戏大厅与三款游戏，让观众知道成果',CYAN),('第二段','用文件结构说明每个文件负责什么',PURPLE),('第三段','以猜数字示范浏览器与 Flask API 合作',GREEN),('第四段','用五子棋与井字棋说明状态、规则和 AI',GOLD),('第五段','现场执行测试与本机启动命令',RED),('第六段','说明 GitHub、Render 与正式网址',CYAN),('最后','分享遇到的错误、解决方式和后续扩充',PURPLE)],.8,1.2,11.8,.76,17)
text(s,.9,6.65,11.5,.35,'讲解重点：先说「为什么」，再说「怎么写」，最后实际操作证明结果。',16,GOLD,True,PP_ALIGN.CENTER)

prs.core_properties.title='小游戏网站制作顺序'
prs.core_properties.subject='Python Flask + HTML/CSS/JavaScript 教学简报'
prs.core_properties.author='Codex'
prs.save(OUT)
print(OUT)
