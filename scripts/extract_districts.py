#!/usr/bin/env python3
"""PDFから投票区（ポスター掲示地区）データを抽出しJSON出力する。"""
import re, json, os

# 市川市4区: 抽出済みテキストから得た投票区データ（id, name, spots, voters）
ICHIKAWA_RAW = """
1 大町第二団地集会所 7 0.10 1257
2 大町会館 7 3.03 1773
3 大野地域ふれあい館 9 2.49 6493
4 柏井小学校 7 2.80 7805
5 大柏出張所 8 0.70 5250
6 迎米公民館 7 0.88 3070
7 大野小学校 6 1.05 7137
8 下貝塚中学校 6 0.58 4073
9 曽谷春日神社 7 0.47 3149
10 国分高校 7 0.66 4016
11 曽谷小学校 9 0.75 5941
12 国分小学校 9 0.83 3735
13 チャレンジ国分 4 0.67 2675
14 中国分小学校 9 1.23 5079
15 歴史博物館 8 0.90 4353
16 いきいきセンター北国分 9 0.56 3033
17 国府台小学校 8 0.76 4625
18 第一中学校 9 1.12 1651
19 真間小学校 6 0.31 2417
20 第二中学校 7 0.37 2927
21 須和田自治会館 4 0.25 2721
22 第三中学校 6 0.56 5660
23 宮久保小学校 9 1.09 9051
24 東部公民館 9 1.51 7473
25 若宮小学校 9 0.63 4497
26 中山清華園管理棟 7 0.27 2582
27 第四中学校 7 0.49 3444
28 いきいきセンター北方 9 0.51 5274
29 中山小学校 6 0.45 4806
30 鬼高小学校 7 0.54 6121
31 第六中学校 7 0.51 6066
"""

# 船橋市4区: 抽出テキストから得た投票区データ
FUNABASHI_RAW = """
1 船橋市立峰台小学校 10 0.93 10874
2 船橋市立市場小学校 4 0.40 2223
3 船橋市立宮本小学校 7 0.39 4464
4 船橋市立宮本中学校 9 0.86 7349
5 船橋市立船橋高等学校 8 1.08 6555
6 船橋市青少年会館 10 2.71 7071
7 船橋市浜町公民館 8 0.86 6169
8 緑台町会会館 7 0.20 2728
9 フェイス５階 7 0.70 11500
10 船橋市立湊町小学校 10 0.42 7179
11 船橋市立湊中学校 7 0.70 1768
12 船橋市立南本町小学校 9 3.31 6069
13 海神中央町会会館 4 0.22 3623
14 船橋市立海神小学校 9 0.69 7711
15 船橋市立海神中学校 10 1.15 13106
17 船橋市立海神南小学校 8 1.32 11402
18 船橋市立葛飾中学校 10 1.80 12770
19 船橋市立葛飾小学校 6 0.56 5842
20 船橋市西部公民館 6 0.62 8746
21 船橋市立小栗原小学校 8 0.65 11441
22 本中山6・7丁目集会所 7 0.13 2620
23 船橋市西船児童ホーム 5 0.42 6660
24 船橋市立法典西小学校 10 1.07 9137
25 船橋市立法典小学校 8 1.41 8290
26 船橋市立法田中学校 8 0.80 4418
27 船橋市法典公民館 6 1.33 8229
28 船橋市立法典東小学校 9 1.43 5663
29 船橋市立丸山小学校 9 0.71 6537
30 船橋市立塚田小学校 10 1.62 9691
31 船橋市立塚田小学校（体育館） 6 0.64 9157
"""

def parse_raw(s):
    rows = []
    for line in s.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("（") or "欠番" in line:
            continue
        m = re.match(r"^(\d+)\s+(.+?)\s+(\d+)\s+[\d.]+\s+(\d+)\s*$", line)
        if m:
            rows.append({
                "id": int(m.group(1)),
                "name": m.group(2).strip(),
                "spots": int(m.group(3)),
                "voters": int(m.group(4)),
            })
    return rows

def main():
    ichikawa = [d for d in parse_raw(ICHIKAWA_RAW) if d["id"] <= 31]
    funabashi_fixed = [d for d in parse_raw(FUNABASHI_RAW) if d["id"] <= 31]
    out = {
        "ichikawa_4": {
            "label": "市川市4区",
            "total_spots": sum(d["spots"] for d in ichikawa),
            "total_voters": sum(d["voters"] for d in ichikawa),
            "districts": ichikawa,
        },
        "funabashi_4": {
            "label": "船橋市4区",
            "total_spots": sum(d["spots"] for d in funabashi_fixed),
            "total_voters": sum(d["voters"] for d in funabashi_fixed),
            "districts": funabashi_fixed,
        },
    }
    path = os.path.join(os.path.dirname(__file__), "..", "data", "districts.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Wrote", path)
    print("市川市4区:", len(ichikawa), "区,", out["ichikawa_4"]["total_spots"], "箇所")
    print("船橋市4区:", len(funabashi_fixed), "区,", out["funabashi_4"]["total_spots"], "箇所")

if __name__ == "__main__":
    main()
