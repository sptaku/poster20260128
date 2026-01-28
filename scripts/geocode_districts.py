#!/usr/bin/env python3
"""
districts.json の各地区に Nominatim で緯度・経度を付け、マップでピン表示できるようにする。
使用: python3 scripts/geocode_districts.py
"""
import json
import os
import time
import urllib.request
import urllib.parse

DISTRICTS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "districts.json")
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "PosterMapApp/1.0 (local use)"

def geocode(query: str) -> tuple[float | None, float | None]:
    url = f"{NOMINATIM_URL}?{urllib.parse.urlencode({'q': query, 'format': 'json', 'limit': 1})}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data and len(data) > 0:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None, None

def main():
    import sys
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])

    with open(DISTRICTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    n = 0
    for area_key, city in [("ichikawa_4", "市川市"), ("funabashi_4", "船橋市")]:
        area = data.get(area_key, {})
        districts = area.get("districts", [])
        for i, d in enumerate(districts):
            if limit is not None and n >= limit:
                break
            if "lat" in d and "lng" in d:
                continue
            q = f"{d['name']} 千葉県{city}"
            lat, lon = geocode(q)
            if lat is not None and lon is not None:
                d["lat"] = round(lat, 6)
                d["lng"] = round(lon, 6)
                print(f"  {area_key} id={d['id']} {d['name']} -> {d['lat']},{d['lng']}")
            else:
                print(f"  skip (no result): {q}")
            n += 1
            time.sleep(1.1)
        if limit is not None and n >= limit:
            break

    with open(DISTRICTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved", DISTRICTS_PATH)

if __name__ == "__main__":
    main()
