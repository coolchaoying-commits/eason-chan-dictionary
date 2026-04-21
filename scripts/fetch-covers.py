#!/usr/bin/env python3
"""
精准版：按 (歌名, 原专辑名) 搜索 iTunes，必须命中原专辑才接受。
"""
import urllib.request, urllib.parse, json, ssl, os

# (id, 歌名关键字, 原专辑关键字 [可多个 alias])
SONGS = [
    ("fu-si-saan-haa",     "富士山下",   ["What's Going On"]),
    ("lok-faa-lau-seoi",   "落花流水",   ["Life Continues"]),
    ("pou-tou-sing-suk-si","葡萄成熟",   ["U-87", "U 87", "U87"]),
    ("ming-nin-gam-jat",   "明年今日",   ["The Line-Up", "Line-Up", "Line Up"]),
    ("saa-lung",           "沙龍",       ["H3M"]),
    ("jam-ngo-hang",       "任我行",     ["The Key"]),
    ("fu-gwaa",            "苦瓜",       ["Stranger Under My Skin", "?"]),
    ("daan-ce",            "單車",       ["Shall We Dance", "Shall We Talk"]),
    ("jyu-ngo-soeng-zoi",  "與我常在",   ["與我常在", "与我常在"]),
    ("k-go-zi-wong",       "K歌之王",    ["打得火熱", "打得火热"]),
]

CTX = ssl.create_default_context()

def search(term, entity="song", country="hk", limit=15):
    url = ("https://itunes.apple.com/search?"
           + urllib.parse.urlencode({
               "term": term, "entity": entity,
               "country": country, "limit": limit, "lang": "zh_cn",
           }))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as r:
            return json.loads(r.read())
    except Exception:
        return {"results": []}

def is_eason(artist):
    a = artist.lower()
    return ("eason" in a) or ("陳奕迅" in artist) or ("陈奕迅" in artist)

def album_match(name, aliases):
    n = name.lower().replace(" ", "").replace("-", "")
    for a in aliases:
        if a.lower().replace(" ", "").replace("-", "") in n:
            return True
    return False

def hi_res(url):
    return url.replace("100x100bb.jpg", "1500x1500bb.jpg") \
              .replace("100x100", "1500x1500")

def find_song(song_kw, aliases):
    """跨 hk/tw/us 找一个：歌名匹配 + 艺人是 Eason + 专辑名匹配 alias"""
    for country in ("hk", "tw", "us"):
        for term in (f"陳奕迅 {song_kw}", f"Eason Chan {song_kw}", song_kw):
            data = search(term, "song", country, 25)
            for r in data.get("results", []):
                if not is_eason(r.get("artistName", "")):
                    continue
                if song_kw not in r.get("trackName", "") and \
                   song_kw not in r.get("trackCensoredName", ""):
                    continue
                if album_match(r.get("collectionName", ""), aliases):
                    return r
    return None

def find_album(aliases):
    """退一步：直接按 album alias 找；取第一张"""
    for country in ("hk", "tw", "us"):
        for a in aliases:
            data = search(f"陳奕迅 {a}", "album", country, 10)
            for r in data.get("results", []):
                if not is_eason(r.get("artistName", "")):
                    continue
                if album_match(r.get("collectionName", ""), aliases):
                    return r
    return None

def fetch():
    out_dir = "covers"
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    previews = {}
    for sid, song_kw, aliases in SONGS:
        r = find_song(song_kw, aliases) or find_album(aliases)
        if not r:
            rows.append((sid, "MISS", "", "", "")); continue
        art_url = hi_res(r["artworkUrl100"])
        preview = r.get("previewUrl", "")
        if preview:
            previews[sid] = preview
        out = os.path.join(out_dir, f"{sid}.jpg")
        try:
            req = urllib.request.Request(art_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
                with open(out, "wb") as f:
                    f.write(resp.read())
            size = os.path.getsize(out)
            rows.append((sid, f"OK {size//1024}KB",
                         r.get("collectionName", ""),
                         r.get("trackName", r.get("collectionName", "")),
                         "✓" if preview else "—"))
        except Exception as e:
            rows.append((sid, f"ERR {e}", "", "", ""))

    print(f"\n{'id':<22} {'cover':<14} {'album':<40} {'track':<22} {'preview'}")
    print("-" * 120)
    for row in rows:
        print(f"{row[0]:<22} {row[1]:<14} {row[2]:<40} {row[3]:<22} {row[4]}")

    # 写 audio-previews.js
    with open("audio-previews.js", "w", encoding="utf-8") as f:
        f.write("// 自动生成：由 scripts/fetch-covers.py 写入\n")
        f.write("// 来源：Apple Music / iTunes 官方 30 秒试听片段\n")
        f.write("const PREVIEWS = {\n")
        for sid in previews:
            f.write(f'  "{sid}": "{previews[sid]}",\n')
        f.write("};\n")
    print(f"\n✓ 已写入 audio-previews.js（{len(previews)} 首）")

if __name__ == "__main__":
    fetch()
