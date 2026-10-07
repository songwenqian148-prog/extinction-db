import sqlite3

DB_PATH = "data.db"

events = [
    ("寒武纪末灭绝事件", 485, 484, "海洋环境扰动，古杯动物、奥尔登三叶虫等早期动物群大量消失", "The Geologic Time Scale 2012"),
    ("晚奥陶世后一次灭绝", 440, 439, "冰川融化海平面快速上升，底栖群落崩溃", "Earth-Science Reviews 2021"),
    ("泥盆纪早期灭绝事件", 407, 406, "气候冷暖波动，珊瑚礁生态受损", "Palaeontology 2019"),
    ("泥盆纪晚期（弗拉斯-法门）大灭绝", 372, 371, "多次缺氧脉冲，珊瑚、层孔虫彻底衰落", "Nature Communications 2020"),
    ("石炭纪雨林崩溃事件", 307, 306, "冈瓦纳冰盖扩张，海平面震荡，森林生态系统崩溃", "Palaeogeography 2022"),
    ("中二叠世灭绝事件", 260, 259, "峨眉山大火成岩省喷发，海洋缺氧", "Science 2019"),
    ("二叠纪末大灭绝（大死亡）", 252, 251.9, "史上最严重灭绝事件，火山喷发导致温室效应，约96%海洋生物灭绝", "Nature 2018"),
    ("早三叠世灭绝事件", 247, 246, "二叠纪末灭绝后海洋持续缺氧高温，生态系统复苏受阻", "Nature 2018"),
    ("侏罗-白垩灭绝事件", 145, 144, "侏罗-白垩之交小型灭绝，海生爬行动物与双壳类大量消失", "Journal of the Geological Society 2022"),
    ("白垩纪末大灭绝（恐龙灭绝）", 66, 66, "小行星撞击+火山活动，非鸟恐龙、菊石灭绝", "Science 2010"),
]

causes = {
    "寒武纪末灭绝事件": ("海平面波动", "寒武纪海侵海退反复，底栖生物栖息地不稳定", "The Geologic Time Scale 2012"),
    "晚奥陶世后一次灭绝": ("快速海侵", "冰川消融，海水快速淹没大陆架，底栖群落无法适应", "Earth-Science Reviews 2021"),
    "泥盆纪早期灭绝事件": ("气候波动", "冷暖交替，珊瑚礁生态系统持续压力", "Palaeontology 2019"),
    "泥盆纪晚期（弗拉斯-法门）大灭绝": ("多次缺氧脉冲", "多轮海水缺氧事件叠加，礁生物连续灭绝", "Nature Communications 2020"),
    "石炭纪雨林崩溃事件": ("冰盖扩张", "全球降温，海平面下降，热带雨林大面积退缩", "Palaeogeography 2022"),
    "中二叠世灭绝事件": ("大型火山喷发", "峨眉山火山释放巨量温室气体，海洋缺氧酸化", "Science 2019"),
    "二叠纪末大灭绝（大死亡）": ("大型火山喷发", "西伯利亚暗色岩喷发，大量CO₂释放，海洋酸化", "Nature 2018"),
    "早三叠世灭绝事件": ("海洋缺氧", "早三叠世海水持续缺氧与高温，底栖生态复苏延迟", "Nature 2018"),
    "侏罗-白垩灭绝事件": ("海平面与气候波动", "海平面升降与气候波动，浅海生态系统更替", "Journal of the Geological Society 2022"),
    "白垩纪末大灭绝（恐龙灭绝）": ("天体撞击", "希克苏鲁伯小行星撞击，尘埃遮蔽阳光，食物链崩溃", "Science 2010"),
}

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

inserted = 0
skipped = 0
for name, start_ma, end_ma, brief, source in events:
    exists = cur.execute(
        "SELECT event_id FROM extinction_events WHERE event_name = ?", (name,)
    ).fetchone()
    if exists:
        skipped += 1
        continue
    cur.execute(
        "INSERT INTO extinction_events(event_name, start_ma, end_ma, brief_desc, source) "
        "VALUES (?, ?, ?, ?, ?)",
        (name, start_ma, end_ma, brief, source),
    )
    event_id = cur.lastrowid
    cause_type, desc, csource = causes[name]
    cur.execute(
        "INSERT INTO extinction_causes(event_id, cause_type, description, source) "
        "VALUES (?, ?, ?, ?)",
        (event_id, cause_type, desc, csource),
    )
    inserted += 1

conn.commit()
total = cur.execute("SELECT COUNT(*) FROM extinction_events").fetchone()[0]
conn.close()

print(f"inserted={inserted} skipped(existing)={skipped} total_events={total}")
