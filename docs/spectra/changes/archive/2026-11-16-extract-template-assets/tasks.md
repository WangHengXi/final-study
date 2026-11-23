## 1. 以專案根目錄 `static/final-study/` 管理此次新資產

- [x] 1.1 在新增 static 設定前，加入 focused Django 測試來斷言 `STATICFILES_DIRS` 包含 `BASE_DIR / "static"`，且 staticfiles finder 可找到 `final-study/js/.gitkeep`；以該測試在目前程式碼上失敗作為 RED 證據。

- [x] 1.2 [after: 1.1] 在 `config/settings/base.py` 設定根目錄 `static/` 為 Django staticfiles 的額外搜尋路徑，並建立 `static/final-study/css/` 和 `static/final-study/js/.gitkeep`；以 1.1 的 focused 測試轉為 GREEN，並以 `python manage.py findstatic final-study/js/.gitkeep` 和 `python manage.py findstatic core/studytrack-theme.css` 確認新舊 static 來源都可解析。

## 2. 依重複度切分 CSS，而非建立單一大型樣式表

- [x] 2.1 [after: 1.2] 先新增首頁 CSS 載入的回歸測試並確認它在現況失敗，再將 `apps/core/templates/core/home.html` 的所有內嵌 CSS 搬至 `static/final-study/css/home.css`，讓模板以 `{% static %}` 在既有 `core/studytrack-theme.css` 前載入此檔；以測試轉為 GREEN、`findstatic final-study/css/home.css` 和既有首頁登入狀態連結測試確認外部資產與行為正確。

- [x] 2.2 [after: 1.2] 先為課程列表、課程詳情、錯題表單與課程設定表單的 stylesheet URL 與無內嵌 `<style>` 新增會失敗的回歸測試，再將各自 CSS 分別搬至 `static/final-study/css/course-list.css`、`course-detail.css`、`question-form.css` 與 `course-setting-form.css`，並在對應模板的主題 CSS 前載入；以測試轉為 GREEN、各檔案的 `findstatic` 結果與 Tailwind CDN 行不變完成驗證。

- [x] 2.3 [after: 1.2] 先為登入、註冊與登出頁共用 stylesheet URL、無內嵌 `<style>` 與保留 action／CSRF 欄位新增會失敗的回歸測試，再將三頁 CSS 整合至 `static/final-study/css/account.css` 並在既有主題 CSS 前載入；以三個 HTTP 回應的測試轉為 GREEN 與 `findstatic final-study/css/account.css` 完成驗證。

## 3. JavaScript 目錄只保留版本控制所需的空檔

- [x] 3.1 [after: 1.2] 保留 `static/final-study/js/.gitkeep`，不建立或載入空白 JavaScript，並保留所有模板既有的 Tailwind CDN `<script>` 行；以檔案內容檢查與 1.1 的 staticfiles 測試確認 JavaScript 目錄可被 Git 追蹤且沒有新增的應用程式 JavaScript 行為。

## 4. 以靜態資源解析與模板輸出作為完成檢查

- [x] 4.1 [after: 2.1, 2.2, 2.3, 3.1] 執行完整 Django 測試與六個新 CSS 檔的 `python manage.py findstatic` 檢查，確認回歸測試共同覆蓋所有受影響模板：每個模板均引用正確的 `/static/final-study/css/` 路徑、沒有內嵌 `<style>`，且現有主題 CSS 與 Tailwind CDN 載入行為不變。
