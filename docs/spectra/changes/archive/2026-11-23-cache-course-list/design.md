## Context

`config/settings/base.py` already configures Django's default cache with Redis, the project key prefix, and a 60-second default timeout. `CourseDataView` currently builds every owned-course JSON payload directly from the database, while `CourseCreateView` creates a course without coordinating with the list endpoint. Because course data is private to its owner and varies by search and page, a URL-only cache key would be unsafe and incomplete.

## Goals / Non-Goals

**Goals:**

- Reuse the existing default cache configuration for successful course-list API payloads.
- Prevent cached course data from crossing user, search, page, or invalidation boundaries.
- Ensure a newly created course is visible on the creator's next matching list request.
- Keep the course-list API available when Redis is unavailable.

**Non-Goals:**

- Change the `/learning/courses/data/` JSON schema, pagination size, sorting, authorization, or frontend request flow.
- Add a Redis dependency, a cache administration UI, cache warming, cache metrics, or caching for course details.
- Wire course rename or deletion flows, which do not currently exist, to invalidation; the reusable invalidation helper remains available for a later change.

## Decisions

### 使用每位使用者的版本化課程列表快取鍵

新增 learning-owned cache helper。它以使用者 ID、該使用者的課程列表版本、已修剪搜尋字串的雜湊與正整數頁碼組合出固定長度 payload key；使用者專屬版本值另存為不受預設 payload TTL 影響的 cache key。資料端點只快取成功的純 JSON-相容 payload，並沿用 default cache 的 60 秒 timeout。

此設計避免將原始搜尋文字放進快取鍵，也不需要列舉未知的搜尋或頁碼鍵。單純使用 URL 快取被排除，因為該 API 回傳資料依登入使用者而異。直接快取 QuerySet 或 HttpResponse 被排除，因為它們攜帶不必要的延遲求值或回應狀態。

### 建立課程後遞增課程列表快取版本

`CourseCreateView` 成功建立課程後，呼叫 helper 使建立者的版本值遞增；下一個列表請求因此使用新的 payload key。舊版本 payload 保留到其 60 秒 timeout，但不會再被讀取。版本遞增取代逐一刪除 payload key，因為既有快取鍵的搜尋條件和頁碼數量無法預先列舉。

這項失效只作用於建立者，不能影響其他使用者。建立失敗、驗證錯誤與重複課程代碼不得使快取失效。

### 快取故障時直接查詢資料庫

cache helper 將 cache get、set、版本讀取與版本遞增的故障視為最佳化失敗：讀取失敗時呼叫資料庫 payload builder，寫入或失效失敗不改變既有 HTTP 成功／錯誤語意。資料庫或授權例外不可被快取錯誤處理吞掉。

這保留課程列表的可用性，並避免 Redis 主機、帳號或網路細節進入 API 回應。把 cache 失敗回傳 5xx 的做法被排除，因為快取不是本 API 的資料來源。

## Implementation Contract

**Behavior:** 已驗證使用者重複讀取相同 `q`、`page` 的課程資料可取得快取中的成功 payload。建立者成功新增課程後，下一次符合條件的請求不得讀取建立前的 payload；另一名使用者的快取不受影響。

**Interface / data shape:** 在 `apps.learning` 提供 helper，負責取得或寫入課程 payload 與使指定使用者的版本失效。`CourseDataView` 將其現有 payload builder 作為 loader 提供給 helper；`CourseCreateView` 只在 `Course.objects.create` 成功後呼叫失效函式。HTTP JSON payload 與狀態碼維持不變。

**Failure modes:** cache backend 的讀寫或版本操作失敗時，讀取請求仍執行 loader 並回傳資料庫 payload；寫入或失效失敗不向使用者揭露內部 cache 錯誤。輸入驗證、匿名 401、資料庫失敗與 payload builder 程式錯誤不屬於快取備援範圍。

**Acceptance criteria:** 使用 LocMemCache 的 Django 測試驗證同鍵重複讀取避免第二次 payload builder 查詢、不同使用者或 query/page 使用不同 identity、建立後的下一次讀取含新課程、建立失敗不失效，以及 cache 操作拋出例外時 API 仍回傳正確 payload。執行 `uv run python manage.py test apps.learning`。

**In scope:** `apps/learning/views.py`、新的 learning cache helper 與 `apps/learning/tests.py`。

**Out of scope:** Redis 部署設定、資料庫 migration、前端 JavaScript、課程詳情快取，以及尚未存在的課程更新／刪除流程。

## Risks / Trade-offs

- [同一使用者有大量搜尋或頁碼組合] → 每個 payload 仍在設定的 60 秒 timeout 後過期，版本更新不需要掃描或刪除全部 key。
- [版本 key 在 payload 尚存時遺失] → 新版本 key 會以新的版本值建立，既有 payload 不再成為讀取目標。
- [cache 服務失效] → 直接執行資料庫 loader 並維持原有 JSON 契約。
- [將來加入課程更新或刪除] → 後續變更必須呼叫相同 invalidation helper，否則將在最多 60 秒內顯示舊資料。

## Migration Plan

1. 新增 cache helper 與以 LocMemCache 隔離的測試，先確認既有端點資料契約不變。
2. 將 `CourseDataView` 的 payload 建構包裝為 cache loader，並在 `CourseCreateView` 成功後使建立者版本失效。
3. 執行 learning 測試與完整 Django system check；若需復原，移除 helper 呼叫即可回到直接資料庫查詢，無資料遷移或持久化 payload 要清除。

## Open Questions

無。
