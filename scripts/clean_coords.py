#!/usr/bin/env python3
"""千葉県外の誤った座標を districts.json から削除する。"""
import json, os

path = os.path.join(os.path.dirname(__file__), "..", "data", "districts.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 市川市: おおよそ 35.70-35.80, 139.88-140.00
# 船橋市: おおよそ 35.65-35.75, 139.92-140.05
def in_chiba_ichikawa(lat, lng):
    return 35.70 <= lat <= 35.80 and 139.88 <= lng <= 140.00

def in_chiba_funabashi(lat, lng):
    return 35.65 <= lat <= 35.75 and 139.92 <= lng <= 140.05

for area_key, in_area in [("ichikawa_4", in_chiba_ichikawa), ("funabashi_4", in_chiba_funabashi)]:
    for d in data.get(area_key, {}).get("districts", []):
        if "lat" in d and "lng" in d:
            if not in_area(d["lat"], d["lng"]):
                del d["lat"]
                del d["lng"]
                print(f"removed wrong coords: {area_key} id={d['id']} {d['name']}")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved", path)
