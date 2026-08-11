from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT = "/home/wsfoo/Gomoku-Versions/AI五子棋_专案说明.pptx"
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
DARK = RGBColor(25, 30, 40)
WOOD = RGBColor(214, 164, 92)
WHITE = RGBColor(248, 249, 251)
BLUE = RGBColor(64, 123, 255)
MUTED = RGBColor(180, 190, 205)

def box(slide, x, y, w, h, text, size=22, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    b = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    p = b.text_frame.paragraphs[0]
    p.text, p.alignment = text, align
    p.font.name, p.font.size, p.font.bold, p.font.color.rgb = "Microsoft YaHei", Pt(size), bold, color
    b.text_frame.word_wrap = True
    return b

def base(title, number):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill
    bg.solid(); bg.fore_color.rgb = DARK
    box(s, .65, .3, 11, .6, title, 28, WHITE, True)
    box(s, 11.8, .35, .7, .4, f"{number:02d}", 15, WOOD, True, PP_ALIGN.RIGHT)
    return s

def bullets(s, items, x=.9, y=1.35, w=11.5, size=22):
    for i, item in enumerate(items):
        box(s, x, y+i*.78, w, .58, "• " + item, size, WHITE)

s = base("AI 五子棋 · 专案说明", 1)
box(s, .8, 1.55, 7.5, .9, "Python + HTML 唯一版本", 38, WOOD, True)
box(s, .85, 2.65, 7.8, .7, "随机黑白棋 · 暂停继续 · 棋谱回放 · AI 对战", 21, MUTED)
for r in range(5):
    for c in range(5):
        q=s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9+c*.48), Inches(1.5+r*.48), Inches(.38), Inches(.38))
        q.fill.solid(); q.fill.fore_color.rgb = RGBColor(20,20,20) if (r+c)%3==0 else WHITE
        q.line.color.rgb = WOOD

s=base("专案目标",2)
bullets(s,["把多个实验版本整合成单一维护版本","保留可直接打开的 index.html 与 Python Flask 版","使用标准五子棋交叉点落子方式","提供适合学习、展示和局域网分享的中文专案"])

s=base("主要功能",3)
bullets(s,["可选择人机对战或同设备本地双人","15 × 15 交叉点棋盘，人机模式随机分配黑白棋","15 秒回合计时、暂停／继续与重新开始","棋型评分 AI：先求胜、再防守、最后比较攻守","固定回放面板：开头、单步、播放、末尾与返回棋局"])

s=base("游戏流程",4)
bullets(s,["开始新局 → 随机分配颜色 → 黑棋先手","玩家落子 → 更新棋盘 → 判断五连 → AI 计算最佳位置","暂停时保留剩余时间并禁止落子","进入回放时暂停真实对局；退出后恢复最后局面"])

s=base("AI 决策",5)
bullets(s,["候选点只取现有棋子附近，减少计算量","第一优先：找到电脑立即成五的位置","第二优先：阻挡玩家下一手成五","第三优先：依活四、冲四、活三等棋型综合评分"])

s=base("一个版本 · 两种启动方式",6)
bullets(s,["唯一游戏源码：根目录 index.html","直接启动：双击 index.html，或使用 GitHub Pages","Python 启动：根目录 app.py 提供同一份 index.html","Flask 监听 0.0.0.0:8000，可供同一 Wi-Fi 设备连接"])

s=base("Python 版启动",7)
box(s,.9,1.35,11.5,3.4,"python3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npython app.py",24,WHITE,True)
box(s,.9,5.25,11.5,.7,"本机：http://127.0.0.1:8000　局域网：http://你的IP:8000",21,WOOD,True)

s=base("线上游玩与后续扩充",8)
bullets(s,["线上网址：https://sheng13.github.io/Gomoku-Versions/","代码注解：CODE_WALKTHROUGH.md","可继续扩充难度选择、悔棋、音效、战绩保存与双人模式","所有功能应先测试，再同步直接版和 Python 版"])

prs.core_properties.title = "AI 五子棋专案说明"
prs.core_properties.author = "sheng13"
prs.save(OUT)
print(OUT)

