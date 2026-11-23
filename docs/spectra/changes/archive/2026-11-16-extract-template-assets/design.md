## Context

StudyTrack 的九個主要頁面都已使用 Django 的 `{% static %}`，且共用 `apps/core/static/core/studytrack-theme.css`。其中八個頁面仍在模板的 `<style>` 區塊保有頁面 CSS；六個學習頁與三個帳號頁也都保留 Tailwind CDN 的外部 `<script>`。專案設定目前只有 `STATIC_URL`，因此若將新資源放在專案根目錄 `static/`，必須明確加入 `STATICFILES_DIRS` 才能由 Django staticfiles 尋找。

這次雖不改變任何使用者功能，但涉及根目錄 static 搜尋設定、多個模板與資產載入順序，所以需要先固定資產位置和驗證方式。

## Goals / Non-Goals

目標：

- 讓 `static/final-study/css/` 成為此次拆出之頁面 CSS 的唯一位置，並建立 `static/final-study/js/` 作為未來自訂 JavaScript 的位置。
- 從模板移除既有的內嵌 CSS，改以 `{% static %}` 連結外部 CSS，同時保留現有渲染結果、頁面路由與 Tailwind class。
- 讓 Django 的 staticfiles 在開發與部署設定中都能找到新目錄，並以測試驗證輸出的資源 URL 與檔案可解析性。

非目標：

- 不改變頁面視覺設計、HTML 結構、登入／課程功能或表單行為。
- 不搬移既有 `apps/core/static/core/studytrack-theme.css`。
- 不調整 Tailwind CDN、導入 Node.js 或建立 CSS／JavaScript 的編譯流程。
- 不新增自訂 JavaScript；目前只有第三方 Tailwind CDN 載入，沒有可抽離的內嵌應用程式腳本。

## Decisions

### 以專案根目錄 `static/final-study/` 管理此次新資產

在 `config/settings/base.py` 加入 `STATICFILES_DIRS = [BASE_DIR / "static"]`，使所有設定環境都能發現 `static/final-study/`。這符合指定目錄名稱，也不會移動仍由 `apps.core` 管理的既有主題檔。

替代方案是在 `apps/core/static/` 下建立資產；雖能自動被 app staticfiles 尋找，但不符合指定的 `static/final-study/` 路徑，也會讓與 core app 無關的頁面資產被該 app 擁有。

### 依重複度切分 CSS，而非建立單一大型樣式表

建立下列外部樣式表：

- `static/final-study/css/home.css`：首頁的專屬版面與響應式規則。
- `static/final-study/css/course-list.css`：課程列表的專屬規則。
- `static/final-study/css/course-detail.css`：課程詳情的專屬規則。
- `static/final-study/css/question-form.css`：錯題表單的 Django 表單輸出規則。
- `static/final-study/css/course-setting-form.css`：學習設定表單的 Django 表單輸出規則。
- `static/final-study/css/account.css`：登入、註冊與登出的共用頁面與表單規則。

各模板先載入自己的頁面 CSS，再載入既有的 `core/studytrack-theme.css`，完全保留目前的 CSS 覆寫順序。`course_form.html` 沒有內嵌 CSS，故不強制新增空白頁面樣式表。

替代方案是為每個模板建檔；這會重複登入與註冊的相同表單規則。另一個替代方案是合併為單一 CSS；這會讓首頁的大量專屬規則與表單規則互相混雜。

### JavaScript 目錄只保留版本控制所需的空檔

於 `static/final-study/js/.gitkeep` 保留空目錄，並不把第三方 Tailwind CDN 腳本下載或重新封裝為專案檔案。這確保 Git 保存使用者要求的目錄，且不新增未使用的程式碼或維護第三方副本。

### 以靜態資源解析與模板輸出作為完成檢查

測試將驗證 staticfiles finder 可以找到新增的 CSS 及 JavaScript 目錄保留檔，並對每個受影響模板的 HTTP 回應檢查預期的 `/static/final-study/css/...` 連結。驗證時使用專案既有相依套件環境執行 `python manage.py test` 與 `python manage.py findstatic`；目前執行環境尚未安裝 Django，不能把該環境的失敗視為程式碼失敗。

## Implementation Contract

- `STATICFILES_DIRS` 必須包含專案根目錄的 `static`，而不覆蓋 Django app 既有 static 目錄的發現機制。
- 每份原本有內嵌 CSS 的受影響模板渲染後，必須多出正確的 stylesheet URL，且模板中不再有 `<style>` 標籤。
- CSS 的內容必須為原樣式規則的搬移；頁面專屬 CSS 必須位於上述 `static/final-study/css/` 對應檔案中。
- 所有受影響模板的 `core/studytrack-theme.css` 連結與 Tailwind CDN 腳本載入行為必須維持不變。
- `static/final-study/js/` 必須存在且由 Git 保留，但不應載入空白腳本，也不應增加 JavaScript 行為。
- 這項變更不改變能力層級可觀察行為：既有路由、登入狀態分流、課程資料與表單提交契約均不變。

範圍內：Django static 設定、受影響 HTML 模板、外部 CSS、目錄保留檔與對應測試。

範圍外：設計調整、第三方資產自託管、CSS 建置工具、JavaScript 功能與既有主題檔搬遷。

## Risks / Trade-offs

- [資產找不到] -> 以 `STATICFILES_DIRS` 設定根目錄 static，並以 `findstatic` 和模板回應測試確認 Django 可解析資產。
- [CSS 覆寫順序改變造成外觀差異] -> 維持每一模板原本內嵌 CSS 位於 `core/studytrack-theme.css` 之前的相對順序。
- [共用帳號樣式被過度合併] -> 僅合併登入、註冊與登出已經重複的基本規則；各頁特有內容仍由 Tailwind class 表達。
- [空 JavaScript 目錄被 Git 忽略] -> 以 `.gitkeep` 保留目錄，不加入會在瀏覽器載入的空腳本。

## Migration Plan

1. 新增 static 尋找設定與外部 CSS 檔，但先不改模板；確認 finder 可定位新檔案。
2. 逐一以外部 stylesheet 連結取代模板內嵌 CSS，並確保 `core/studytrack-theme.css` 仍在後方載入。
3. 新增或擴充回應測試，執行 Django 測試與 static finder 檢查。
4. 若需要回復，移除新 stylesheet 連結並還原各模板原本的內嵌 CSS，再移除 `STATICFILES_DIRS` 與新資產目錄；因不含資料遷移，無資料回復步驟。

## Open Questions

無；目前沒有內嵌的應用程式 JavaScript，因此 JavaScript 目錄保留但不加入可執行檔案。
