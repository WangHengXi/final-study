## 1. 使用者隔離的列表快取

- [x] 1.1 實作「User-isolated cached course data」與「使用每位使用者的版本化課程列表快取鍵」：在 `apps/learning/course_list_cache.py` 提供只快取成功 JSON-相容 payload 的 helper，key 納入使用者、已修剪搜尋值雜湊、頁碼與使用者版本，payload 使用 default cache timeout，版本 key 不隨 payload timeout 過期。以 `apps/learning/tests.py` 的 LocMemCache 測試驗證相同 request 命中快取、使用者與 query/page 隔離，並執行 `uv run python manage.py test apps.learning`。
- [x] 1.2 [after: 1.1] 將 `CourseDataView` 的既有 payload builder 接到 cache helper，讓成功 JSON schema、排序、授權、無效頁碼 400 與匿名 401 維持不變；當 cache 讀寫失敗時依「快取故障時直接查詢資料庫」改由 loader 回傳資料，且不公開 backend 細節。以模擬 cache 操作例外的端點測試與 `uv run python manage.py test apps.learning` 驗證。

## 2. 建立後失效

- [x] 2.1 [after: 1.2] 實作「Course creation invalidates cached course lists」與「建立課程後遞增課程列表快取版本」：僅在 `CourseCreateView` 成功建立課程後使建立者的列表版本失效；驗證失敗或重複代碼不失效，且其他使用者版本不變。以先快取空列表、建立 `Calculus`／`MATH101`、再讀取列表的 Django 測試驗證新課程立即可見，並執行 `uv run python manage.py test apps.learning`。

## 3. 變更驗證

- [x] 3.1 [after: 2.1] 檢查課程列表的快取實作符合「User-isolated cached course data」與「Course creation invalidates cached course lists」：確認快取只包裝成功資料 payload、版本化失效沒有掃描未知 key，且 API 契約未變；以 `uv run python manage.py check`、`uv run python manage.py test apps.learning` 與 `spectra validate cache-course-list` 驗證。
