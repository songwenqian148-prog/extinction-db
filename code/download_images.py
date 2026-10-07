"""Fetch real, freely-licensed images from Wikimedia Commons and store them in
the local `static/` folder, then point `extinction.db` -> `fossil_image` at them.

Run:  python code/download_images.py
"""

import os
import re
import sqlite3
import time
from urllib.parse import urlparse

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "extinction.db")
API = "https://commons.wikimedia.org/w/api.php"

HEADERS = {"User-Agent": "extinction-db-coursework/1.0 (educational use)"}

# event display name -> candidate search queries (extra queries are fallbacks so
# transient network failures never leave an event without its images)
EVENT_QUERIES = {
    "寒武纪末灭绝事件": [
        "Anomalocaris canadensis reconstruction",
        "Cambrian trilobite fossil",
        "Burgess Shale reconstruction",
        "Cambrian fossil",
        "Hallucigenia",
    ],
    "奥陶纪末大灭绝": [
        "Ordovician trilobite fossil",
        "Orthoceras fossil",
        "Ordovician brachiopod fossil",
        "Ordovician nautiloid fossil",
        "Ordovician fossil",
    ],
    "晚奥陶世后一次灭绝": [
        "Ordovician graptolite fossil",
        "Ordovician glaciation",
        "Ordovician echinoderm fossil",
        "Ordovician fossil",
        "graptolite fossil",
    ],
    "泥盆纪早期灭绝事件": [
        "Devonian coral fossil",
        "early Devonian fossil fish",
        "Devonian brachiopod fossil",
        "Devonian fossil",
        "Devonian fish fossil",
    ],
    "泥盆纪晚期（弗拉斯-法门）大灭绝": [
        "Dunkleosteus",
        "placoderm fossil",
        "Late Devonian fossil",
        "Devonian ammonite fossil",
        "Devonian fossil",
    ],
    "石炭纪雨林崩溃事件": [
        "Arthropleura reconstruction",
        "Lepidodendron fossil",
        "Carboniferous fossil plant",
        "Carboniferous fossil",
        "Meganeura",
    ],
    "中二叠世灭绝事件": [
        "Dimetrodon",
        "Middle Permian fossil",
        "Permian fusulinid",
        "Permian brachiopod fossil",
        "Permian fossil",
    ],
    "二叠纪末大灭绝（大死亡）": [
        "Siberian Traps",
        "Lystrosaurus fossil",
        "Permian Triassic boundary",
        "Permian extinction",
        "Permian fossil",
    ],
    "早三叠世灭绝事件": [
        "Early Triassic fossil",
        "Lystrosaurus skeleton",
        "Triassic marine reptile",
        "Triassic fossil",
        "Triassic recovery",
    ],
    "三叠纪末大灭绝": [
        "Plateosaurus skeleton",
        "Late Triassic fossil",
        "Triassic extinction",
        "Coelophysis",
        "Triassic fossil",
    ],
    "侏罗-白垩灭绝事件": [
        "Jurassic ammonite fossil",
        "ichthyosaur fossil",
        "Jurassic fossil",
        "Jurassic marine",
        "ammonite fossil",
    ],
    "白垩纪末大灭绝（恐龙灭绝）": [
        "Tyrannosaurus rex skeleton",
        "Chicxulub crater",
        "Cretaceous Paleogene boundary",
        "Triceratops fossil",
        "K-Pg boundary",
    ],
}

# curated Wikimedia Commons files (tried first; search queries are the fallback)
PINNED = {
    "寒武纪末灭绝事件": [
        "File:Anomalocaris life restoration by Sebastian Brandt (Reco-Brandt).jpg",
        "File:Cambrian Trilobite Olenoides Mt. Stephen.jpg",
        "File:Burgess Shale reconstruction.jpg",
    ],
    "奥陶纪末大灭绝": [
        "File:Ceraurus sp. (fossil trilobite) (Ordovician; Picton, Ontario, Canada).jpg",
        "File:Orthoceras, Erfoud, Marruecos, 2021-01-14, DD 001-040 FS.jpg",
        "File:Fossil Brachiopod (Strophomena filitexta).jpg",
    ],
    "晚奥陶世后一次灭绝": [
        "File:Ordovician Sea Life by Knight.jpg",
        "File:The late Ordovician sea floor of southwest Wisconsin.jpg",
        "File:Carneyella ulrichi fossil edrioasteroid Upper Ordovician KY.jpg",
    ],
    "泥盆纪早期灭绝事件": [
        "File:Hexagonaria sp. (fossil coral) (Devonian; near Fulton, Missouri, USA) 2 - 53317525186.jpg",
        "File:Cardipeltis bryanti fossil fish, Bighorn Mountains WY.jpg",
        "File:Devonian Brachiopod reef.jpg",
    ],
    "泥盆纪晚期（弗拉斯-法门）大灭绝": [
        "File:Dunkleosteus spp.jpg",
        "File:Alienacanthus malkowskii.jpg",
        "File:Discoclymenia cucullata Late Devonian Morocco.jpg",
    ],
    "石炭纪雨林崩溃事件": [
        "File:Arthropleura Reconstruction.jpg",
        "File:Lepidodendron fossil.jpg",
        "File:Carboniferous fossil plant Neuropteris.jpg",
    ],
    "中二叠世灭绝事件": [
        "File:Dimetrodon incisivum 01.jpg",
        "File:Rhynchonellid crura Permian Texas.jpg",
        "File:Kaibab Formation - fossil brachiopod and crinoid columnals.jpg",
    ],
    "二叠纪末大灭绝（大死亡）": [
        "File:Extent of Siberian traps german.png",
        "File:Lystrosaurus skeleton, from Abel, O. (1919). Die Stämme der Wirbeltiere.jpg",
        "File:Native iron in basalt (Siberian Traps Flood Basalt, Permian-Triassic boundary"
        " times, 251 Ma; Putoran Plateau, Siberia, Russia) 1 (17151514269).jpg",
    ],
    "早三叠世灭绝事件": [
        "File:Triassic fossils.png",
        "File:Lystrosaurus georgi mounted skeleton.jpg",
        "File:Triassic marine reptile diversity.jpg",
    ],
    "三叠纪末大灭绝": [
        "File:Plateosaurus panorama.jpg",
        "File:Coelophysis bauri mount.jpg",
        "File:Fossil fern with galls, from Late Triassic, Alborz, Iran 01.jpg",
    ],
    "侏罗-白垩灭绝事件": [
        "File:Ichthyosaur fossil NCMNS.jpg",
        "File:Calcretes et ammonites.jpg",
        "File:Araucaria mirabilis (fossil cone) (Jurassic; Argentina) (49021443726).jpg",
    ],
    "白垩纪末大灭绝（恐龙灭绝）": [
        "File:Tyrannosaurus Rex (Zhengzhou).jpg",
        "File:Chicxulub Impact Crater, Gulf of Mexico (33789560443).jpg",
        "File:Cretaceous paleogene boundary calcium carbonate curve 1.png",
    ],
}

TARGET_PER_EVENT = 3
BAD_EXT = {".svg", ".tif", ".tiff", ".xcf", ".pdf", ".webm", ".ogv", ".ogg", ".djvu"}


def log(msg):
    print(msg, flush=True)


def search_commons(session, query, limit=8):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size",
        "iiurlwidth": "1100",
    }
    last_err = None
    for attempt in range(5):
        try:
            resp = session.get(API, params=params, timeout=30)
            if resp.status_code != 200 or not resp.text.strip():
                raise ValueError(f"HTTP {resp.status_code} empty body")
            return resp.json().get("query", {}).get("pages", {}) or {}
        except Exception as err:  # noqa: BLE001
            last_err = err
            time.sleep(2.5 * (attempt + 1))
    log(f"   search failed for '{query}': {last_err}")
    return {}


def imageinfo_for_titles(session, titles):
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles),
        "prop": "imageinfo",
        "iiprop": "url|size",
        "iiurlwidth": "1100",
    }
    for attempt in range(5):
        try:
            resp = session.post(API, data=params, timeout=30)
            if resp.status_code != 200 or not resp.text.strip():
                raise ValueError(f"HTTP {resp.status_code} empty body")
            pages = resp.json().get("query", {}).get("pages", {}) or {}
            return {p.get("title"): (p.get("imageinfo") or [{}])[0] for p in pages.values()}
        except Exception:  # noqa: BLE001
            time.sleep(2.5 * (attempt + 1))
    return {}


def acceptable(title, info):
    ext = os.path.splitext(title)[1].lower()
    if ext in BAD_EXT:
        return False
    w = info.get("width") or 0
    h = info.get("height") or 0
    if w < 640 or h < 400:
        return False
    ratio = w / h if h else 0
    if ratio < 0.35 or ratio > 4:
        return False
    return bool(info.get("thumburl") or info.get("url"))


def download(session, url, path):
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=45)
            if resp.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            resp.raise_for_status()
            if len(resp.content) < 2048:
                raise ValueError("suspiciously small file")
            with open(path, "wb") as fh:
                fh.write(resp.content)
            return len(resp.content)
        except Exception as err:  # noqa: BLE001
            if attempt == 2:
                log(f"   download failed: {err}")
                return 0
            time.sleep(2)
    return 0


def clean_title(title):
    name = title.replace("File:", "")
    name = os.path.splitext(name)[0]
    name = name.replace("_", " ")
    return re.sub(r"\s+", " ", name).strip()


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    for name in os.listdir(STATIC_DIR):
        if name.startswith("event"):
            os.remove(os.path.join(STATIC_DIR, name))
    session = requests.Session()
    session.headers.update(HEADERS)

    result = {}
    for event_name, queries in EVENT_QUERIES.items():
        log(f"[{event_name}]")
        saved = []
        used_remote = set()

        pinned = PINNED.get(event_name, [])
        if pinned:
            infos = imageinfo_for_titles(session, pinned)
            for title in pinned:
                if len(saved) >= TARGET_PER_EVENT:
                    break
                info = infos.get(title)
                if not info or not acceptable(title, info):
                    continue
                url = (info.get("thumburl") or info.get("url") or "").split("?")[0]
                ext = os.path.splitext(urlparse(url).path)[1].lower() or ".jpg"
                idx = len(saved) + 1
                fname = f"{_slug(event_name)}_{idx}{ext}"
                size = download(session, url, os.path.join(STATIC_DIR, fname))
                if size:
                    used_remote.add(title)
                    saved.append((fname, clean_title(title)))
                    log(f"   OK {fname} ({size} bytes) <- {clean_title(title)}")
            time.sleep(0.8)

        for query in queries:
            if len(saved) >= TARGET_PER_EVENT:
                break
            pages = search_commons(session, query)
            for _, page in sorted(
                pages.items(), key=lambda kv: kv[1].get("index", 99)
            ):
                if len(saved) >= TARGET_PER_EVENT:
                    break
                title = page.get("title", "")
                info = (page.get("imageinfo") or [{}])[0]
                if title in used_remote or not acceptable(title, info):
                    continue
                url = (info.get("thumburl") or info.get("url") or "").split("?")[0]
                if not url:
                    continue
                ext = os.path.splitext(urlparse(url).path)[1].lower() or ".jpg"
                idx = len(saved) + 1
                fname = f"{_slug(event_name)}_{idx}{ext}"
                path = os.path.join(STATIC_DIR, fname)
                size = download(session, url, path)
                if size:
                    used_remote.add(title)
                    saved.append((fname, clean_title(title)))
                    log(f"   OK {fname} ({size} bytes) <- {clean_title(title)}")
                break
            time.sleep(1.2)
        result[event_name] = saved
        time.sleep(0.4)

    update_db(result)


def _slug(event_name):
    # stable ASCII-ish key from the event order instead of the Chinese name
    order = list(EVENT_QUERIES.keys()).index(event_name) + 1
    return f"event{order:02d}"


def update_db(result):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS fossil_image ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, "
        "image_title TEXT, image_url TEXT)"
    )
    removed = 0
    updated = 0
    inserted = 0
    for event_name, images in result.items():
        rows = cur.execute(
            "SELECT id FROM fossil_image WHERE event_name = ? ORDER BY id",
            (event_name,),
        ).fetchall()
        for i, (fname, title) in enumerate(images):
            if i < len(rows):
                cur.execute(
                    "UPDATE fossil_image SET image_title = ?, image_url = ? WHERE id = ?",
                    (title, f"/static/{fname}", rows[i][0]),
                )
                updated += 1
            else:
                cur.execute(
                    "INSERT INTO fossil_image(event_name, image_title, image_url) "
                    "VALUES (?, ?, ?)",
                    (event_name, title, f"/static/{fname}"),
                )
                inserted += 1
        for rid, in rows[len(images):]:
            cur.execute("DELETE FROM fossil_image WHERE id = ?", (rid,))
            removed += 1
    conn.commit()
    total = cur.execute("SELECT COUNT(*) FROM fossil_image").fetchone()[0]
    conn.close()
    log(f"\nupdated={updated} inserted={inserted} removed={removed} total_images={total}")


if __name__ == "__main__":
    main()
