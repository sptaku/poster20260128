# ポスター貼り 地区割り振り

千葉県第4区（衆院選）のポスター掲示マップに基づき、**ポスター貼りの人数**を入力すると、対応する地区が自動で割り振られるWebアプリです。  
市川市4区・船橋市4区のポス掲略図（PDF）から投票区データを抽出し、設置箇所数がなるべく均等になるように A・B・C… に振り分けます。

## 使い方

1. **対象地域**で「市川市4区」「船橋市4区」「両方まとめて」のいずれかを選ぶ
2. **ポスター貼りの人数**に、割り振りたい人数（1～50）を入力する
3. 表示された「A」「B」「C」…ごとの地区一覧を確認する  
   （各人の「○箇所」「有権者およそ○人」も表示）
4. 地区名をクリックし、「Googleマップで見る」を選ぶと、座標が登録された地区ではその場所にピンが立った状態で開きます（未登録の地区は検索結果で開きます）。

## ローカルで動かす

`data/districts.json` を読み込むため、ブラウザで `index.html` を直接開く（`file://`）とエラーになります。  
次のいずれかで起動してください。

```bash
# 方法1: Python（標準搭載でそのまま使えます）
python3 -m http.server 8000
# → ブラウザで http://localhost:8000 を開く

# 方法2: Node.js がある場合
npx serve .
```

## GitHub で公開する

### 1. リポジトリを作成してpush

```bash
# Gitリポジトリを初期化（まだの場合）
git init
git add .
git commit -m "Initial commit: ポスター貼り地区割り振りアプリ"

# GitHubでリポジトリを作成後、以下を実行
git remote add origin https://github.com/<ユーザー名>/<リポジトリ名>.git
git branch -M main
git push -u origin main
```

**注意**: PDFファイル（約70MB×2）が含まれます。pushに時間がかかる場合があります。  
PDFをGitHubに含めない場合は、`.gitignore` に `*.pdf` を追加し、PDFは別途配置してください（その場合、リンク先を変更する必要があります）。

### 2. GitHub Pagesを有効化

1. GitHubリポジトリの **Settings** → **Pages** を開く
2. **Source** を「Deploy from a branch」に設定
3. **Branch** を `main`、**Folder** を `/ (root)` に設定して保存
4. 数分待つと、公開URLが表示されます: `https://<ユーザー名>.github.io/<リポジトリ名>/`

### 3. 動作確認

公開URLにアクセスして、以下を確認してください：
- 対象地域の選択ができる
- 人数を入力すると地区が割り振られる
- 地区名をクリックして「マップ（○ページ目）で見る」「Googleマップで見る」が開ける
- 「両方まとめて」で市川と船橋が分かれて割り振られる

## データについて

- **市川市4区**: ポスター掲示場設置場所総数 229 箇所（31 投票区）  
- **船橋市4区**: 同上 235 箇所（30 投票区）※ PDF から抽出した範囲

元データは市川市・船橋市選挙管理委員会の「ポスター掲示場設置場所略図」です。  
地区名・設置数などは公式PDFを前提にしています。最新の設置状況は各市選管にご確認ください。

## ファイル構成

```
.
├── index.html        # アプリ本体（HTML+CSS+JS）
├── data/
│   └── districts.json   # 投票区データ（設置数・有権者数など）
├── scripts/
│   ├── extract_districts.py   # JSON 生成用（PDF テキストから手動で入力したデータを変換）
│   ├── geocode_districts.py   # 地区の緯度・経度を取得して districts.json に追記（Googleマップのピン用）
│   └── clean_coords.py        # 千葉県外の誤った座標を削除
└── README.md
```

`districts.json` を更新する場合は、`scripts/extract_districts.py` 内の `ICHIKAWA_RAW` / `FUNABASHI_RAW` を編集したうえで `python3 scripts/extract_districts.py` を実行すると、`data/districts.json` が再生成されます。

地区の緯度・経度（Googleマップでピン表示するため）は、`python3 scripts/geocode_districts.py` で OpenStreetMap Nominatim を使って取得できます。約1秒に1件のため全件で約2分かかります。誤って他県の施設が入った座標は `python3 scripts/clean_coords.py` で削除できます。
