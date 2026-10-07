import base64
import os
import sqlite3

STATIC_DIR = "static"

# Minimal valid 1x1 JPEG placeholder
PLACEHOLDER_JPEG = base64.b64decode(
    "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a"
    "HBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAABAAEBAREA/8QAFAABAAAAAAAA"
    "AAAAAAAAAAAACf/EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAD8AKp//2Q=="
)

# event display name -> list of static filenames (one per image row)
event_images = {
    "寒武纪末灭绝事件": ["cambrian_1.jpg", "cambrian_2.jpg", "cambrian_3.jpg"],
    "奥陶纪末大灭绝": ["ordovician_1.jpg", "ordovician_2.jpg", "ordovician_3.jpg"],
    "晚奥陶世后一次灭绝": ["ordovician_4.jpg", "ordovician_5.jpg", "ordovician_6.jpg"],
    "泥盆纪早期灭绝事件": ["devonian_1.jpg", "devonian_2.jpg", "devonian_3.jpg"],
    "泥盆纪晚期（弗拉斯-法门）大灭绝": ["devonian_4.jpg", "devonian_5.jpg", "devonian_6.jpg"],
    "石炭纪雨林崩溃事件": ["carboniferous_1.jpg", "carboniferous_2.jpg", "carboniferous_3.jpg"],
    "中二叠世灭绝事件": ["permian_1.jpg", "permian_2.jpg", "permian_3.jpg"],
    "二叠纪末大灭绝（大死亡）": ["permian_4.jpg", "permian_5.jpg", "permian_6.jpg"],
    "早三叠世灭绝事件": ["triassic_1.jpg", "triassic_2.jpg", "triassic_3.jpg"],
    "三叠纪末大灭绝": ["triassic_4.jpg", "triassic_5.jpg", "triassic_6.jpg"],
    "侏罗-白垩灭绝事件": ["jurassic_1.jpg", "jurassic_2.jpg", "jurassic_3.jpg"],
    "白垩纪末大灭绝（恐龙灭绝）": ["cretaceous_1.jpg", "cretaceous_2.jpg", "cretaceous_3.jpg"],
}

os.makedirs(STATIC_DIR, exist_ok=True)

created = 0
kept = 0
for names in event_images.values():
    for name in names:
        path = os.path.join(STATIC_DIR, name)
        if os.path.exists(path):
            kept += 1
        else:
            with open(path, "wb") as f:
                f.write(PLACEHOLDER_JPEG)
            created += 1

conn = sqlite3.connect("extinction.db")
cur = conn.cursor()
updated = 0
for event_name, names in event_images.items():
    rows = cur.execute(
        "SELECT id FROM fossil_image WHERE event_name = ? ORDER BY id", (event_name,)
    ).fetchall()
    for (row_id,), filename in zip(rows, names):
        cur.execute(
            "UPDATE fossil_image SET image_url = ? WHERE id = ?",
            (f"/static/{filename}", row_id),
        )
        updated += 1
conn.commit()
total = cur.execute("SELECT COUNT(*) FROM fossil_image").fetchone()[0]
conn.close()

print(f"placeholders created={created} kept={kept} updated_rows={updated} total_images={total}")
