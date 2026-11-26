## Why

登入者需要一個可擴充為今日安排、行事曆、課程與複習分析的備考總覽；同時訪客仍需要一個清楚說明產品用途的公開首頁。現行根路徑會依登入狀態切換頁面，且測試站尚未套用讀書事項資料表遷移，導致行事曆失敗。

## What Changes

- 讓根路徑一律顯示公開首頁，說明 StudyTrack 的備考整理用途並引導登入或註冊。
- 新增獨立的登入後備考 Overview 路徑，保留今日事項摘要並為行事曆、課程與未來複習分析預留資訊架構。
- 將登入後導覽收斂為下拉式選單，選單包含備考 Overview、行事曆、我的課程、預留的複習分析位置與登出。
- 將登入成功後預設導向 Overview。
- 將讀書事項遷移納入測試站部署步驟，確保 `learning_studytask` 資料表存在後才啟用行事曆。

## Capabilities

### New Capabilities

- `study-overview`: 提供登入使用者的獨立備考總覽入口與今日摘要。

### Modified Capabilities

- `public-homepage`: 根路徑固定為公開產品介紹頁，不再對登入者改呈個人資料。
- `shared-navigation`: 登入後導覽改為可展開的選單，並提供 Overview 與既有工作區入口。

## Impact

- `apps/core/views.py`、`apps/core/urls.py`、`apps/core/templates/core/home.html` 與新的 Overview 模板。
- `apps/core/templates/core/includes/navbar.html`、`apps/core/static/core/navbar.css` 與首頁樣式。
- `config/settings/base.py` 的登入導向。
- 測試站部署使用的資料庫遷移命令與 `apps/learning/migrations/0007_studytask.py`。
