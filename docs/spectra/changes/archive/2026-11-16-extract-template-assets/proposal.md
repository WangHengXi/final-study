## Why

目前首頁、學習頁與帳號頁各自把頁面專屬 CSS 寫在 HTML 的 `<style>` 區塊中，讓版面標記與樣式規則難以分別閱讀及維護。將樣式移到統一的 `static/final-study/css/`，並建立對應的 JavaScript 目錄，可讓日後新增前端互動時有固定位置，同時保持現有頁面功能與外觀不變。

## What Changes

- 在專案根目錄建立 `static/final-study/css/` 與 `static/final-study/js/`，並設定 Django 尋找此專案層級 static 目錄。
- 將目前內嵌於首頁、課程列表、課程詳情、錯題表單、課程設定表單，以及帳號登入／註冊／登出頁面的 CSS 拆成外部樣式表；帳號頁共用相同的表單樣式表。
- 讓每個受影響模板透過 `{% static %}` 載入自己的外部樣式表，且維持現有 `core/studytrack-theme.css` 的載入順序與 Tailwind CDN 載入方式。
- 保留 JavaScript 目錄供未來自訂腳本使用；此次不新增、搬移或打包 JavaScript，因為目前模板沒有內嵌的應用程式 JavaScript。
- 加入可在已安裝專案相依套件的環境執行的檢查，確認 Django 可以解析新靜態資源，且各模板渲染後均引用正確的外部樣式表。

## Non-Goals (optional)

- 不調整任何頁面的文字、DOM 結構、互動、配色或 Tailwind class。
- 不移除或重新設計既有的 `apps/core/static/core/studytrack-theme.css` 主題覆寫。
- 不將 Tailwind CDN 改為本機編譯或新增 Node.js 前端建置流程。
- 不為空的 JavaScript 目錄加入占位執行程式碼或新的前端功能。

## Impact

- Affected specs: none
- Affected code:
  - New: `static/final-study/css/` 下的頁面樣式表、`static/final-study/js/` 的目錄保留檔，以及用來驗證 static 資源引用的測試。
  - Modified: `config/settings/base.py`、受影響的 Django HTML 模板。
  - Removed: 模板內嵌的頁面專屬 CSS 區塊。
- Compatibility: no capability-level observable behavior changes
