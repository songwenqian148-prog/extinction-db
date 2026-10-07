import html
import os
import re
import sqlite3

import requests
from flask import Flask, render_template, request

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # dotenv optional
    pass

app = Flask(__name__)

DATA_DB = "data.db"
IMAGE_DB = "extinction.db"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 时间轴数据，附带灾难等级
timeline_data = [
    {"name":"寒武纪末灭绝事件", "age":"约4.85亿年前", "rank":"B", "percent":"30%~50%物种消失", "color":"#f1c40f", "label":"B级 中度灭绝"},
    {"name":"奥陶纪末大灭绝", "age":"约4.43亿年前", "rank":"S", "percent":"约85%物种消失", "color":"#e74c3c", "label":"S级 顶级大灭绝"},
    {"name":"晚奥陶世后一次灭绝", "age":"约4.40亿年前", "rank":"A", "percent":"50%~70%物种消失", "color":"#e67e22", "label":"A级 重大灭绝"},
    {"name":"泥盆纪早期灭绝事件", "age":"约4.1亿年前", "rank":"C", "percent":"小于30%物种消失", "color":"#27ae60", "label":"C级 小型灭绝"},
    {"name":"泥盆纪晚期（弗拉斯-法门）大灭绝", "age":"约3.59亿年前", "rank":"S", "percent":"约75%物种消失", "color":"#e74c3c", "label":"S级 顶级大灭绝"},
    {"name":"石炭纪雨林崩溃事件", "age":"约3.07亿年前", "rank":"C", "percent":"小于30%物种消失", "color":"#27ae60", "label":"C级 小型灭绝"},
    {"name":"中二叠世灭绝事件", "age":"约2.6亿年前", "rank":"B", "percent":"30%~50%物种消失", "color":"#f1c40f", "label":"B级 中度灭绝"},
    {"name":"二叠纪末大灭绝（大死亡）", "age":"约2.52亿年前", "rank":"S", "percent":"约96%物种消失", "color":"#e74c3c", "label":"S级 顶级大灭绝"},
    {"name":"早三叠世灭绝事件", "age":"约2.47亿年前", "rank":"C", "percent":"小于30%物种消失", "color":"#27ae60", "label":"C级 小型灭绝"},
    {"name":"三叠纪末大灭绝", "age":"约2.01亿年前", "rank":"A", "percent":"50%~70%物种消失", "color":"#e67e22", "label":"A级 重大灭绝"},
    {"name":"侏罗-白垩灭绝事件", "age":"约1.45亿年前", "rank":"C", "percent":"小于30%物种消失", "color":"#27ae60", "label":"C级 小型灭绝"},
    {"name":"白垩纪末大灭绝（恐龙灭绝）", "age":"约0.66亿年前", "rank":"S", "percent":"约76%物种消失", "color":"#e74c3c", "label":"S级 顶级大灭绝"},
]

all_events = [item["name"] for item in timeline_data]


# --------------------------------------------------------------------------- #
# 各时代的美术主题：配色、背景氛围与时代说明
# --------------------------------------------------------------------------- #
def _theme(era, tagline, accent, accent2, glow1, glow2, bg_mid):
    return {
        "era": era,
        "tagline": tagline,
        "accent": accent,
        "accent2": accent2,
        "accent_rgb": _hex_to_rgb(accent),
        "glow1": _hex_to_rgb(glow1),
        "glow2": _hex_to_rgb(glow2),
        "bg_mid": bg_mid,
    }


def _hex_to_rgb(value):
    value = value.lstrip("#")
    return ",".join(str(int(value[i:i + 2], 16)) for i in (0, 2, 4))


DEFAULT_THEME = _theme("深时", "显生宙 · 灭绝事件数据库", "#38bdf8", "#22d3ee", "#38bdf8", "#22d3ee", "#0f1720")

EVENT_THEMES = {
    # 寒武纪：原始海洋的青绿色
    "寒武纪末灭绝事件": _theme("寒武纪", "海洋生命的第一次大爆发与危机", "#22d3ee", "#0ea5e9", "#22d3ee", "#0ea5e9", "#0e2230"),
    # 奥陶纪：冰川深海的冷蓝
    "奥陶纪末大灭绝": _theme("奥陶纪", "冰川降临，海洋底栖世界崩塌", "#60a5fa", "#3b82f6", "#60a5fa", "#3b82f6", "#101f36"),
    "晚奥陶世后一次灭绝": _theme("晚奥陶世", "海侵与缺氧的连环打击", "#7dd3fc", "#38bdf8", "#7dd3fc", "#38bdf8", "#0e1f2e"),
    # 泥盆纪：珊瑚礁的暖绿
    "泥盆纪早期灭绝事件": _theme("早泥盆世", "珊瑚礁世界的繁荣与波动", "#2dd4bf", "#14b8a6", "#2dd4bf", "#14b8a6", "#0d2624"),
    # 泥盆纪晚期：缺氧的浑浊色调
    "泥盆纪晚期（弗拉斯-法门）大灭绝": _theme("晚泥盆世", "缺氧的海洋与珊瑚礁的崩塌", "#a3b18a", "#84a98c", "#84a98c", "#708090", "#1c2118"),
    # 石炭纪：雨林的翠绿
    "石炭纪雨林崩溃事件": _theme("石炭纪", "巨型森林的繁盛与雨林崩溃", "#4ade80", "#22c55e", "#4ade80", "#22c55e", "#0e2418"),
    # 中二叠世：干旱大陆的赭黄
    "中二叠世灭绝事件": _theme("中二叠世", "干旱大陆与火山前兆", "#fbbf24", "#f59e0b", "#fbbf24", "#f59e0b", "#2a2110"),
    # 二叠纪末：火山与“大死亡”的暗红
    "二叠纪末大灭绝（大死亡）": _theme("二叠纪末", "西伯利亚暗色岩与大死亡", "#fb7185", "#ef4444", "#fb7185", "#ef4444", "#2a1114"),
    # 早三叠世：高温荒芜的焦黄
    "早三叠世灭绝事件": _theme("早三叠世", "高温缺氧下的荒芜世界", "#f59e0b", "#d97706", "#f59e0b", "#d97706", "#2a1d0e"),
    # 三叠纪末：火山裂谷的紫色
    "三叠纪末大灭绝": _theme("三叠纪末", "火山裂谷与恐龙的崛起", "#c084fc", "#a855f7", "#c084fc", "#a855f7", "#231430"),
    # 侏罗—白垩：温暖巨兽时代的碧绿
    "侏罗-白垩灭绝事件": _theme("侏罗—白垩纪", "温暖湿润的巨兽时代", "#34d399", "#10b981", "#34d399", "#10b981", "#0f241d"),
    # 白垩纪末：撞击火光的橙红
    "白垩纪末大灭绝（恐龙灭绝）": _theme("白垩纪末", "小行星撞击与恐龙灭绝", "#fb923c", "#f97316", "#fb923c", "#f97316", "#2c1410"),
}

ERA_KEYWORDS = [
    ("寒武", "寒武纪末灭绝事件"),
    ("奥陶", "奥陶纪末大灭绝"),
    ("泥盆", "泥盆纪晚期（弗拉斯-法门）大灭绝"),
    ("石炭", "石炭纪雨林崩溃事件"),
    ("二叠", "二叠纪末大灭绝（大死亡）"),
    ("三叠", "三叠纪末大灭绝"),
    ("侏罗", "侏罗-白垩灭绝事件"),
    ("白垩", "白垩纪末大灭绝（恐龙灭绝）"),
]


def resolve_theme(text):
    """根据选中的事件或提问内容，匹配最贴合的时代美术主题。"""
    if not text:
        return DEFAULT_THEME, False
    for name in all_events:
        if name in text:
            return EVENT_THEMES.get(name, DEFAULT_THEME), True
    for keyword, name in ERA_KEYWORDS:
        if keyword in text:
            return EVENT_THEMES.get(name, DEFAULT_THEME), True
    return DEFAULT_THEME, False


# --------------------------------------------------------------------------- #
# 数据库 -> 结构化上下文（给 DeepSeek 当“知识库”）
# --------------------------------------------------------------------------- #
def build_db_context():
    """把四张表的记录整理成紧凑的文本，作为大模型的检索上下文。"""
    conn = sqlite3.connect(DATA_DB)
    events = conn.execute(
        "SELECT event_id, event_name, start_ma, end_ma, brief_desc, source "
        "FROM extinction_events ORDER BY event_id"
    ).fetchall()
    causes = conn.execute(
        "SELECT event_id, cause_type, description, source "
        "FROM extinction_causes ORDER BY event_id"
    ).fetchall()
    species = conn.execute(
        "SELECT event_id, species_name, taxon_group, source "
        "FROM extinct_species ORDER BY event_id"
    ).fetchall()
    records = conn.execute(
        "SELECT date, fact, names, places, source FROM extinction_records ORDER BY id"
    ).fetchall()
    conn.close()

    lines = ["【灭绝事件表】(事件ID | 名称 | 起止年代Ma | 简述 | 来源)"]
    for eid, name, start, end, brief, src in events:
        lines.append(f"{eid} | {name} | {start}-{end} Ma | {brief} | {src}")

    lines.append("")
    lines.append("【灭绝诱因表】(事件ID | 诱因类型 | 描述 | 来源)")
    for eid, ctype, desc, src in causes:
        lines.append(f"{eid} | {ctype} | {desc} | {src}")

    lines.append("")
    lines.append("【灭绝物种表】(事件ID | 物种 | 类群 | 来源)")
    for eid, sp, taxon, src in species:
        lines.append(f"{eid} | {sp} | {taxon} | {src}")

    lines.append("")
    lines.append("【补充记录表】(年代 | 史实 | 相关物种/学者 | 化石地点 | 来源)")
    for date, fact, names, places, src in records:
        lines.append(f"{date} | {fact} | {names} | {places} | {src}")

    return "\n".join(lines)


SYSTEM_PROMPT = (
    "你是“史前灭绝事件数据库”的智能问答助手，服务于一个 SQLite 灭绝事件数据库。\n"
    "回答要求：\n"
    "1. 以【数据库内容】为主要事实依据，可以结合通识做解释性、背景性的扩展，使回答更丰富；"
    "但凡涉及具体年代、百分比、物种名称、诱因、文献来源等事实性数据，必须来自数据库，不得编造。\n"
    "2. 使用简体中文，条理清晰，可用小标题、要点列表和表格，回答尽量充实。\n"
    "3. 主动引用相关的事件名称、灭绝物种（含类群）、发生年代与文献来源。\n"
    "4. 若数据库中确实没有相关记录，明确说明“数据库中暂无相关记录”，不要臆测。\n"
    "5. 如果问题与史前灭绝事件数据库无关，礼貌拒绝并引导用户提出相关主题的问题。\n"
    "6. 回答结尾用一行“来源：”列出引用的文献来源。\n"
)


def ask_deepseek(question):
    """调用 DeepSeek chat API；失败时抛出带说明的异常。"""
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY（请在 .env 中设置）")

    context = build_db_context()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"【数据库内容】\n{context}\n\n【用户问题】\n{question}",
        },
    ]

    resp = requests.post(
        f"{DEEPSEEK_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": 0.4,
            "stream": False,
        },
        timeout=90,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"DeepSeek 接口返回 {resp.status_code}: {resp.text[:200]}")
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


# --------------------------------------------------------------------------- #
# 轻量 Markdown -> HTML（先转义再做有限格式转换，避免注入）
# --------------------------------------------------------------------------- #
def _inline_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def _is_table_sep(line):
    return "-" in line and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line) is not None


def md_to_html(text):
    text = html.escape(text or "")
    lines = text.split("\n")
    out = []
    i, n = 0, len(lines)
    list_tag = None

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    while i < n:
        line = lines[i].rstrip()

        # 表格
        if line.strip().startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            close_list()
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{_inline_md(c)}</th>" for c in header)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{_inline_md(c)}</td>" for c in row) + "</tr>"
                for row in rows
            )
            out.append(
                f"<div class='table-wrap'><table class='md-table'><thead><tr>{thead}</tr>"
                f"</thead><tbody>{tbody}</tbody></table></div>"
            )
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)

        if heading:
            close_list()
            level = min(len(heading.group(1)) + 2, 6)
            out.append(f"<h{level}>{_inline_md(heading.group(2))}</h{level}>")
        elif bullet:
            if list_tag != "ul":
                close_list()
                out.append("<ul>")
                list_tag = "ul"
            out.append(f"<li>{_inline_md(bullet.group(1))}</li>")
        elif ordered:
            if list_tag != "ol":
                close_list()
                out.append("<ol>")
                list_tag = "ol"
            out.append(f"<li>{_inline_md(ordered.group(1))}</li>")
        elif line.strip() == "":
            close_list()
        else:
            close_list()
            out.append(f"<p>{_inline_md(line)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# 路由
# --------------------------------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def index():
    event_info = None
    img_list = []
    badge_info = None
    ai_question = ""
    ai_answer = None
    ai_error = None
    theme = DEFAULT_THEME
    theme_active = False

    conn_img = sqlite3.connect(IMAGE_DB)
    total_img = conn_img.execute("SELECT COUNT(*) FROM fossil_image").fetchone()[0]
    conn_img.close()

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        event_name = request.form.get("event_name", "").strip()

        # AI 智能问答分支
        if question:
            ai_question = question
            theme, theme_active = resolve_theme(question)
            try:
                ai_answer = md_to_html(ask_deepseek(question))
            except Exception as err:  # noqa: BLE001
                ai_error = str(err)
        elif event_name:
            theme, theme_active = resolve_theme(event_name)
            # 读取事件数据库 data.db，联查事件+原因
            conn_data = sqlite3.connect(DATA_DB)
            row = conn_data.execute(
                """
                SELECT e.event_name, e.brief_desc, c.description
                FROM extinction_events e
                LEFT JOIN extinction_causes c ON e.event_id = c.event_id
                WHERE e.event_name = ?
                """,
                (event_name,),
            ).fetchone()
            conn_data.close()

            conn_img = sqlite3.connect(IMAGE_DB)
            images = conn_img.execute(
                "SELECT image_title, image_url FROM fossil_image WHERE event_name = ?",
                (event_name,),
            ).fetchall()
            conn_img.close()

            if row:
                event_info = {"name": row[0], "desc": row[1], "cause": row[2]}
                img_list = images
                for t in timeline_data:
                    if t["name"] == event_name:
                        badge_info = t
                        break

    return render_template(
        "index.html",
        data=event_info,
        images=img_list,
        all_events=all_events,
        total_img=total_img,
        timeline=timeline_data,
        badge=badge_info,
        ai_question=ai_question,
        ai_answer=ai_answer,
        ai_error=ai_error,
        theme=theme,
        theme_active=theme_active,
    )


if __name__ == "__main__":
    app.run(debug=True)
