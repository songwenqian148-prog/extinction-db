import sqlite3
import os

DB_PATH = "extinction.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ========== 1. 创建图片关联表 ==========
cur.execute("""
CREATE TABLE IF NOT EXISTS fossil_image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT,
    image_title TEXT,
    image_url TEXT
)
""")
cur.execute("DELETE FROM fossil_image")

# ========== 2. 12次灭绝事件，36条图片记录 ==========
image_data = [
# 1 寒武纪末灭绝事件 B级
("寒武纪末灭绝事件", "寒武纪海洋复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Cambrian_sea_reconstruction.jpg/1200px-Cambrian_sea_reconstruction.jpg"),
("寒武纪末灭绝事件", "奇虾复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anomalocaris_recon.jpg/1200px-Anomalocaris_recon.jpg"),
("寒武纪末灭绝事件", "三叶虫寒武纪化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Cambrian_trilobite_fossil.jpg/1200px-Cambrian_trilobite_fossil.jpg"),

# 2 奥陶纪末大灭绝 S级
("奥陶纪末大灭绝", "奥陶纪海洋生态复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ordovician_sea.png/1200px-Ordovician_sea.png"),
("奥陶纪末大灭绝", "三叶虫化石标本", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Trilobite_fossil.jpg/1200px-Trilobite_fossil.jpg"),
("奥陶纪末大灭绝", "笔石复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Graptolite_reconstruction.jpg/1200px-Graptolite_reconstruction.jpg"),

#3 晚奥陶世后一次灭绝 A级
("晚奥陶世后一次灭绝", "奥陶纪冰川想象图", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Ordovician_glaciation.jpg/1200px-Ordovician_glaciation.jpg"),
("晚奥陶世后一次灭绝", "奥陶纪腕足类化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Brachiopod_fossils.jpg/1200px-Brachiopod_fossils.jpg"),
("晚奥陶世后一次灭绝", "远古海洋底栖生物", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Ordovician_benthic_fauna.jpg/1200px-Ordovician_benthic_fauna.jpg"),

#4 泥盆纪早期灭绝事件 C级
("泥盆纪早期灭绝事件", "泥盆纪浅海场景", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Early_devonian_sea.jpg/1200px-Early_devonian_sea.jpg"),
("泥盆纪早期灭绝事件", "原始鱼类化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Early_devonian_fish.jpg/1200px-Early_devonian_fish.jpg"),
("泥盆纪早期灭绝事件", "原始陆生植物", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Early_land_plants_reconstruction.jpg/1200px-Early_land_plants_reconstruction.jpg"),

#5 泥盆纪晚期（弗拉斯-法门）大灭绝 S级
("泥盆纪晚期（弗拉斯-法门）大灭绝", "泥盆纪远古海洋复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Devonian_sea.jpg/1200px-Devonian_sea.jpg"),
("泥盆纪晚期（弗拉斯-法门）大灭绝", "邓氏鱼复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Dunkleosteus_reconstruction.jpg/1200px-Dunkleosteus_reconstruction.jpg"),
("泥盆纪晚期（弗拉斯-法门）大灭绝", "泥盆纪鱼类化石石板", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Devonian_fish_fossil.jpg/1200px-Devonian_fish_fossil.jpg"),

#6 石炭纪雨林崩溃事件 C级
("石炭纪雨林崩溃事件", "石炭纪原始雨林复原", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Carboniferous_forest.jpg/1200px-Carboniferous_forest.jpg"),
("石炭纪雨林崩溃事件", "巨型节胸蜈蚣复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Arthropleura_reconstruction.jpg/1200px-Arthropleura_reconstruction.jpg"),
("石炭纪雨林崩溃事件", "石炭纪蕨类化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Carboniferous_fern_fossil.jpg/1200px-Carboniferous_fern_fossil.jpg"),

#7 中二叠世灭绝事件 B级
("中二叠世灭绝事件", "中二叠世陆地生态", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Mid_permian_scene.jpg/1200px-Mid_permian_scene.jpg"),
("中二叠世灭绝事件", "卡色龙复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Casea_reconstruction.jpg/1200px-Casea_reconstruction.jpg"),
("中二叠世灭绝事件", "中二叠世爬行动物化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Mid_permian_skull_fossil.jpg/1200px-Mid_permian_skull_fossil.jpg"),

#8 二叠纪末大灭绝（大死亡） S级
("二叠纪末大灭绝（大死亡）", "二叠纪末灭绝场景复原", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Permian_extinction.jpg/1200px-Permian_extinction.jpg"),
("二叠纪末大灭绝（大死亡）", "异齿龙复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Dimetrodon_life_restoration.jpg/1200px-Dimetrodon_life_restoration.jpg"),
("二叠纪末大灭绝（大死亡）", "西伯利亚暗色岩火山喷发", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Siberian_Traps_eruption.jpg/1200px-Siberian_Traps_eruption.jpg"),

#9 早三叠世灭绝事件 C级
("早三叠世灭绝事件", "早三叠世荒芜陆地", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Early_triassic_landscape.jpg/1200px-Early_triassic_landscape.jpg"),
("早三叠世灭绝事件", "水龙兽复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Lystrosaurus_reconstruction.jpg/1200px-Lystrosaurus_reconstruction.jpg"),
("早三叠世灭绝事件", "早三叠世海洋缺氧示意图", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Triassic_ocean_anoxia.jpg/1200px-Triassic_ocean_anoxia.jpg"),

#10 三叠纪末大灭绝 A级
("三叠纪末大灭绝", "三叠纪陆地生态复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Triassic_scene.jpg/1200px-Triassic_scene.jpg"),
("三叠纪末大灭绝", "三叠纪陆生生物群复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Triassic_terrestrial_fauna.jpg/1200px-Triassic_terrestrial_fauna.jpg"),
("三叠纪末大灭绝", "早期恐龙复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Early_dinosaur_reconstruction.jpg/1200px-Early_dinosaur_reconstruction.jpg"),

#11 侏罗-白垩灭绝事件 C级
("侏罗-白垩灭绝事件", "侏罗纪晚期生态复原", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Late_jurassic_scene.jpg/1200px-Late_jurassic_scene.jpg"),
("侏罗-白垩灭绝事件", "剑龙复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Stegosaurus_reconstruction.jpg/1200px-Stegosaurus_reconstruction.jpg"),
("侏罗-白垩灭绝事件", "侏罗纪菊石化石", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Ammonite_fossil.jpg/1200px-Ammonite_fossil.jpg"),

#12 白垩纪末大灭绝（恐龙灭绝） S级
("白垩纪末大灭绝（恐龙灭绝）", "白垩纪森林生态复原图", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Cretaceous_impact.jpg/1200px-Cretaceous_impact.jpg"),
("白垩纪末大灭绝（恐龙灭绝）", "小行星撞击想象图", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Chicxulub_impact_art.jpg/1200px-Chicxulub_impact_art.jpg"),
("白垩纪末大灭绝（恐龙灭绝）", "霸王龙三角龙复原", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Tyrannosaurus_Triceratops.jpg/1200px-Tyrannosaurus_Triceratops.jpg")
]

cur.executemany("INSERT INTO fossil_image (event_name, image_title, image_url) VALUES (?, ?, ?)", image_data)
conn.commit()

# 时间轴数据：名称、年代、等级、灭绝比例、颜色、标签文字
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
img_total = cur.execute("SELECT COUNT(*) FROM fossil_image").fetchone()[0]
conn.close()

print(f"✅ 图片表写入完成，图片总数：{img_total}")

# ========== 3. 新版Flask后端 server.py ==========
server_code = '''from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    event_info = None
    img_list = []
    total_img = 0
    badge_info = None

    conn = sqlite3.connect("extinction.db")
    total_img = conn.execute("SELECT COUNT(*) FROM fossil_image").fetchone()[0]
    conn.close()

    if request.method == "POST":
        event_name = request.form.get("event_name", "").strip()
        conn = sqlite3.connect("extinction.db")
        row = conn.execute("SELECT event_name, description, cause FROM extinction_event WHERE event_name = ?",(event_name,)).fetchone()
        images = conn.execute("SELECT image_title, image_url FROM fossil_image WHERE event_name = ?",(event_name,)).fetchall()
        conn.close()
        if row:
            event_info = {"name":row[0],"desc":row[1],"cause":row[2]}
            img_list = images
            # 匹配等级徽章
            for t in timeline_data:
                if t["name"] == event_name:
                    badge_info = t
                    break
    return render_template("index.html", data=event_info, images=img_list, all_events=all_events, total_img=total_img, timeline=timeline_data, badge=badge)

if __name__ == "__main__":
    app.run(debug=True)
'''
with open("server.py", "w", encoding="utf-8") as f:
    f.write(server_code)
print("✅ server.py 更新完成，支持徽章数据")

# ========== 4. 新版前端 index.html（增加详情页等级徽章） ==========
os.makedirs("templates", exist_ok=True)
html_text = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>史前12次灭绝事件数据库</title>
    <style>
        * {box-sizing: border-box;}
        body {font-family:Microsoft YaHei; margin:35px; background:#f4f6f8;}
        h1 {color:#2d3436; grid-column:1/-1;}
        /* 游戏风格图例 */
        .legend{background:#fff; padding:14px; border-radius:10px; box-shadow:0 2px 10px #00000010; margin-bottom:20px; display:flex; gap:20px; flex-wrap:wrap; align-items:center;}
        .legend-item{display:flex; align-items:center; gap:6px; font-weight:bold;}
        .legend-dot{width:14px;height:14px;border-radius:50%;}
        .timeline-wrap{overflow-x:auto; background:#fff; padding:20px; border-radius:12px; box-shadow:0 2px 10px #00000010; margin-bottom:30px;}
        .timeline{display:flex; gap:14px; min-width:1200px; align-items:center;}
        .timeline-item{flex-shrink:0; text-align:center; width:140px; position:relative;}
        .timeline-form{margin:0;}
        .timeline-btn{border:none; background:none; cursor:pointer; padding:0;}
        .timeline-btn:hover .timeline-dot{transform:scale(1.4); box-shadow:0 0 8px currentColor;}
        .timeline-btn:hover .timeline-name{color:#222;}
        .timeline-dot{width:14px;height:14px; border-radius:50%; margin:0 auto 8px; transition: all 0.2s;}
        .timeline-age{font-size:12px; color:#666;}
        .timeline-name{font-size:13px; font-weight:bold; transition: all 0.2s;}
        /* 悬浮提示框 */
        .tooltip{visibility:hidden; position:absolute; bottom:110%; left:50%; transform:translateX(-50%); background:#222; color:#fff; padding:6px 10px; border-radius:6px; white-space:nowrap; font-size:12px; z-index:99; opacity:0; transition:0.2s;}
        .timeline-item:hover .tooltip{visibility:visible; opacity:1;}

        .container {display: grid; grid-template-columns: 320px 1fr; gap:30px; max-width:1400px;}
        .sidebar{background:#fff; padding:20px; border-radius:12px; box-shadow:0 2px 10px #00000010;}
        .sidebar h3{margin-top:0; color:#2d3436;}
        .event-item{padding:8px 6px; cursor:pointer; border-bottom:1px solid #eee;}
        .stat-box{background:#edf7ff; padding:12px; border-radius:8px; margin-bottom:20px;}
        .main-area{}
        form {margin-bottom:25px;}
        input[type="text"] {padding:10px; width:420px; font-size:16px; border-radius:6px; border:1px solid #bdc3c7;}
        button {padding:10px 20px; background:#0984e3; color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer;}
        .result-card{background:white; padding:26px; border-radius:12px; box-shadow:0 2px 12px #00000012;}
        .img-grid {display:grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap:22px; margin-top:20px;}
        .img-card {background:#f8f9fa; padding:14px; border-radius:8px; text-align:center; overflow:hidden;}
        .img-card img {width:100%; border-radius:6px; transition: transform 0.3s ease;}
        .img-card img:hover{transform: scale(1.05);}
        .img-card p {font-weight:600; color:#2d3436; margin-top:8px;}
        .warn{color:#d63031; font-size:18px;}
        /* 灾难等级徽章 */
        .rank-badge{display:inline-block; margin-left:12px; padding:4px 10px; border-radius:20px; color:white; font-weight:bold; font-size:14px;}
    </style>
</head>
<body>
    <h1>史前12次灭绝事件查询系统</h1>
    <!-- 灾难等级图例（游戏UI） -->
    <div class="legend">
        <div class="legend-item"><span class="legend-dot" style="background:#e74c3c"></span>S级 顶级大灭绝</div>
        <div class="legend-item"><span class="legend-dot" style="background:#e67e22"></span>A级 重大灭绝</div>
        <div class="legend-item"><span class="legend-dot" style="background:#f1c40f"></span>B级 中度灭绝</div>
        <div class="legend-item"><span class="legend-dot" style="background:#27ae60"></span>C级 小型灭绝</div>
    </div>

    <!-- 地质时间轴，点击即可查询 -->
    <div class="timeline-wrap">
        <div class="timeline">
            {% for item in timeline %}
            <div class="timeline-item">
                <div class="tooltip">等级{{item.rank}}｜{{item.percent}}</div>
                <form class="timeline-form" method="post">
                    <input type="hidden" name="event_name" value="{{item.name}}">
                    <button class="timeline-btn" type="submit">
                        <div class="timeline-dot" style="background:{{item.color}}"></div>
                        <div class="timeline-age">{{item.age}}</div>
                        <div class="timeline-name">{{item.name}}</div>
                    </button>
                </form>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="container">
        <div class="sidebar">
            <div class="stat-box">
                <p><strong>事件总数：</strong>{{all_events|length}}</p>
                <p><strong>图片总数量：</strong>{{total_img}}</p>
            </div>
            <h3>灭绝事件列表（点击查询）</h3>
            {% for evt in all_events %}
            <form method="post" style="margin:0;">
                <input type="hidden" name="event_name" value="{{evt}}">
                <button class="event-item" type="submit" style="width:100%;text-align:left;border:none;background:none;">{{evt}}</button>
            </form>
            {% endfor %}
        </div>
        <div class="main-area">
            <form method="post">
                <input type="text" name="event_name" placeholder="输入灭绝事件全名，例如：石炭纪雨林崩溃事件" required>
                <button type="submit">查询资料</button>
            </form>
            {% if data %}
            <div class="result-card">
                <h2>
                    {{data.name}}
                    {% if badge %}
                    <span class="rank-badge" style="background:{{badge.color}}">{{badge.label}}</span>
                    {% endif %}
                </h2>
                <p><strong>灭绝诱因：</strong>{{data.cause}}</p>
                <p><strong>事件简述：</strong>{{data.desc}}</p>
                <h3>配套图像资料</h3>
                <div class="img-grid">
                    {% for title,url in images %}
                        <div class="img-card">
                            <img src="{{url}}" alt="{{title}}">
                            <p>{{title}}</p>
                        </div>
                    {% endfor %}
                </div>
            </div>
            {% elif request.method == "POST" %}
                <div class="result-card">
                    <p class="warn">未找到该灭绝事件，请核对名称。</p>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''
with open("templates/index.html","w",encoding="utf-8") as f:
    f.write(html_text)

print("✅ templates/index.html 详情页等级徽章完成")
print("\n🎉 项目全部功能完成！")
print("✅ 游戏S/A/B/C灾难分级")
print("✅ 时间轴彩色圆点，悬浮提示等级+灭绝比例")
print("✅ 点击时间轴圆点直接查询事件")
print("✅ 事件详情标题附带彩色等级徽章")
print("✅ 侧边栏点击查询、文本框查询")
print("✅ 图片网格展示，图片悬浮放大")
print("✅ 页面顶部游戏UI图例")
