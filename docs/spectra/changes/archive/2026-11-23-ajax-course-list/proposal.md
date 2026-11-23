## Why

目前的課程列表由伺服器一次渲染所有課程，搜尋時也必須重新載入整頁；課程數增加後，等待感受、分頁與讀取失敗的處理都不足。此變更先把課程列表建立為可重用的 AJAX 資料列表範例，並明定之後含後端資料的列表都必須採用相同模式。

## What Changes

- 為登入使用者提供可分頁、可搜尋的課程 JSON 資料端點，且只回傳其自己的課程。
- 將課程列表頁改為以 AJAX 載入、搜尋與換頁，並讓 URL 保留目前關鍵字與頁碼。
- 設計首次讀取、後續讀取、空結果與讀取錯誤的不同可存取畫面狀態，以及可重試操作。
- 建立「後端資料列表」的共通規範：未來新增的此類列表必須以 AJAX 取得資料，並提供分頁、載入、空結果及錯誤處理。

## Capabilities

### New Capabilities

- `ajax-data-lists`: 規範課程及後續後端資料列表的 AJAX 資料契約、分頁與可存取的載入、空結果、錯誤狀態。

### Modified Capabilities

- None.

## Impact

- `apps/learning/views.py`：課程資料 API 與頁面回應分工。
- `apps/learning/urls.py`：課程資料 API 路由。
- `apps/learning/templates/learning/course_list.html`：AJAX 列表容器、狀態區與客戶端行為。
- `static/final-study/css/course-list.css`：載入與錯誤畫面樣式。
- `apps/learning/tests.py`：資料端點、分頁、所有權與畫面狀態測試。
