# 陳奕迅詞典 · Eason Chan Dictionary

> 一本把陳奕迅的歌名當作「詞條」來正經訓詁的私人詞典。
> 注音用粵拼（jyutping），釋義分「原義 / 歌詞義 / 人話版」三層，配金句、出處、何以入心。

🌐 **線上瀏覽**：<https://coolchaoying-commits.github.io/eason-chan-dictionary/>

🎧 **特別功能**：首頁鼠標懸停黑膠封面，自動播放該曲 30 秒副歌片段。

---

## 截圖

> 米白紙頁、暖橙印章、旋轉黑膠、官方專輯封面 —— 像翻一本紙質詞典，又像在唱片店試聽。

---

## 收錄歌曲（首版 10 首）

| 歌名 | 詞 | 曲 | 專輯 / 年份 |
|------|----|----|-----------|
| 富士山下 | 林夕 | 澤日生 | What's Going On…? / 2006 |
| 葡萄成熟時 | 黃偉文 | Vincent Chow | What's Going On…? / 2006 |
| 落花流水 | 黃偉文 | Eric Kwok / 陳奕迅 | What's Going On…? / 2006 |
| 任我行 | 林夕 | Christopher Chak | The Key / 2013 |
| 浮誇 | 黃偉文 | C. Y. Kong | U-87 / 2005 |
| K 歌之王 | 林夕 | 陳輝陽 | 打得火熱 / 2000 |
| 明年今日 | 林夕 | 陳小霞 | The Line-Up / 2002 |
| 單車 | 黃偉文 | 柳重言 | Shall We Dance? Shall We Talk! / 2001 |
| 苦瓜 | 黃偉文 | Kenix Cheang | Stranger Under My Skin / 2011 |
| 沙龍 | 黃偉文 | 陳奕迅 | H3M / 2009 |

---

## 本地運行

```bash
git clone https://github.com/coolchaoying-commits/eason-chan-dictionary.git
cd eason-chan-dictionary
python3 -m http.server 8766
# 瀏覽器打開 http://localhost:8766
```

或直接雙擊 `index.html` 也能看（首頁懸停試聽功能需要 http server）。

---

## 加歌

只改一個文件：`data.js`。複製任意一首詞條，改字段：

```js
{
  id: "fu-si-saan-haa",                 // 粵拼 id，唯一
  song: "富士山下",
  jyutping: "fu3 si6 saan1 haa6",       // 數字聲調
  definitions: [
    { layer: "原義",   gloss: "..." },
    { layer: "歌詞義", gloss: "..." },
    { layer: "人話版", gloss: "..." }
  ],
  lyrics: [
    { line: "金句歌詞", why: "為什麼戳" }
  ],
  credits: { lyricist: "林夕", composer: "澤日生", album: "...", year: 2006 }
}
```

> ⚠️ 文案內加引用 / 強調，請用 `「」` 或 `『』`，不要用 `""` —— 否則會與 JS 字符串引號衝突，整個 `data.js` 會報錯。

加完歌後，跑一次 `python3 scripts/fetch-covers.py` 自動抓官方專輯封面 + 30 秒試聽片段（來自 iTunes Search API）。

---

## 項目結構

```
eason-chan-dictionary/
├── index.html             # 首頁 · 黑膠詞條卡片，懸停試聽
├── word.html              # 詳情頁 · 單首歌完整釋義
├── data.js                # 詞條數據（核心）
├── audio-previews.js      # 30 秒試聽 URL（自動生成）
├── style.css              # Claude 主題 · 米白 / 暖橙 / 石墨
├── favicon.svg
├── covers/                # 專輯封面（自動生成）
└── scripts/
    └── fetch-covers.py    # 從 iTunes 抓封面 + 試聽
```

---

## 設計決策

- **為什麼用粵拼數字聲調？** 標準、專業，且製造「裝作漢語詞典」的反差感最強。普通話拼音版會失去港樂魂。
- **為什麼釋義分三層？** 「原義」奠定字典正經感，「歌詞義」是真正的二創，「人話版」一句話戳到淚點。少一層都不完整。
- **為什麼首頁放金句而不是釋義？** 金句是鈎子，釋義是揭示。先勾住人，進詳情頁再揭示。
- **為什麼是黑膠 + 官方封面？** 粉絲對唱片實體的熱愛是任何 emoji 都替代不了的；旋轉動畫只在懸停時觸發，剋制、不喧賓奪主。
- **為什麼用 Claude 米白 + 暖橙？** 簡潔、溫暖、有呼吸感，比黑底舒服，更貼近紙質詞典的氣質。

---

## 致敬

靈感來自 [cm-dictionary.site](https://cm-dictionary.site/)（陳奕迅迷因詞典 by Cybermiao），向那位匿名作者致敬。本項目是對其概念的個人致敬與重新解讀，並非分支或抄襲。

---

## 版權聲明

- 本項目代碼以 [MIT License](#) 開源，歡迎 fork 並添加你心中的歌單。
- **專輯封面圖**版權歸唱片公司及原作者所有，由 [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/) 公開接口獲取，僅作個人學習與愛好用途。
- **30 秒試聽片段**為 Apple Music 公開預覽 URL，從 Apple CDN 即時加載，本項目不託管任何音頻文件。
- **歌詞**版權歸詞作者及版權方所有，本項目僅引用具有評論性質的金句（fair use），完整歌詞請至各正版音樂平臺收聽。
- 如版權方認為本項目內容不妥，請開 issue 聯繫，將立即下架。

---

編纂：Edison × AI Edison · MMXXVI 春

「我已經 / 給你一切 / 不能比這多」
