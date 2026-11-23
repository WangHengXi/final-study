## Why

課程 AJAX API 已可依使用者、搜尋條件及頁碼回傳資料，但每次請求都重新查詢資料庫，尚未使用既有 Redis 設定。課程建立後也需要立即使該使用者的既有列表快取失效，避免新課程暫時看不見。

## What Changes

- 將課程 JSON 列表的成功回應快取於既有 Redis 快取後端，沿用目前設定的 60 秒預設存活時間。
- 以使用者、已修剪搜尋字串、頁碼及使用者專屬列表版本隔離快取鍵，避免跨帳號或跨查詢共用資料。
- 建立課程成功後遞增該使用者的課程列表版本，使任何既有列表快取立即失效；快取服務不可用時改由資料庫正常回應。
- 為快取命中、隔離、建立後失效及快取故障備援加入測試。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `ajax-data-lists`: 課程資料端點增加使用者隔離的快取與建立課程後的即時失效行為，且維持既有 JSON 契約。

## Impact

- `apps/learning/views.py`：課程資料端點讀取快取，以及建立課程成功後使列表快取失效。
- `apps/learning/`：新增可由端點與建立流程共用的課程列表快取 helper。
- `apps/learning/tests.py`：快取命中、使用者隔離、建立後失效與故障備援測試。
- `config/settings/base.py`：沿用既有 Redis 預設快取設定，不新增快取後端或外部依賴。
