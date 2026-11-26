## Why

目前的首頁混用粉、綠與紫色，並以「二次函數」等學校課程作為示意，與準備研究所入學考試的成年使用者期待不符。登入後直接進入課程列表，也沒有地方按日期安排每天要讀的內容，因此難以把整理課程與每日備考行動連起來。

## What Changes

- 將公開首頁改為莫蘭迪紫、灰紫與暖白的成熟視覺，移除粉色、綠色及校園手帳式的多色示意；文案與範例改為中性、適合備考者的科目、章節、錯題與複習計畫語境。
- 新增僅供登入使用者使用的備考首頁，作為登入成功後的預設入口，呈現今日讀書事項與行事曆入口。
- 新增個人行事曆與每日讀書事項：使用者可在指定日期建立、查看、編輯、完成及刪除自己的讀書安排，並可選擇關聯既有課程。
- 在登入後導覽中提供回到備考首頁與行事曆的明確入口，同時保留現有課程列表與登出操作。

## Capabilities

### New Capabilities

- `study-calendar`: 讓登入使用者以月曆檢視、建立與管理自己指定日期的讀書事項。
- `study-dashboard`: 提供登入後的備考首頁，彙整當日讀書事項並引導至行事曆與課程。

### Modified Capabilities

- `public-homepage`: 將首頁改為成熟的紫白備考視覺與符合目前功能的介紹內容。
- `shared-navigation`: 讓登入後的共用導覽能前往備考首頁、行事曆、課程列表與安全登出。

## Impact

- `apps/core/views.py`、`apps/core/urls.py`、`apps/core/templates/core/home.html`：區分公開首頁與登入後備考首頁的呈現及路由。
- `apps/core/templates/core/includes/navbar.html`、`apps/core/static/core/navbar.css`：加入登入後入口。
- `static/final-study/css/home.css` 與新的儀表板、行事曆樣式：統一為莫蘭迪紫白設計。
- `apps/learning/models.py`、`apps/learning/views.py`、`apps/learning/urls.py`、模板、遷移與測試：新增使用者私有的每日讀書事項及其行事曆操作。
- `config/settings/base.py`：登入成功後導向備考首頁。
