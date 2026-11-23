## 1. 首頁入口與內容

- [x] 1.1 實作 Honest feature narrative 與 Warm stationery composition：重寫 `apps/core/templates/core/home.html` 的首屏、功能內容與流程說明，使其只呈現課程、章節、錯題、錯誤原因、標籤與複習設定；以奶油紙張、粉紫／鼠尾草綠便條卡與學習桌面拼貼建立清楚的手帳風版面。移除或替換正確率、重做結果、題目狀態與進度分析的宣稱及示意，不加入外部圖片、圖示套件、字型服務或前端框架。以桌面寬度手動檢查文字對比、主要行動可辨識性，並逐項比對首頁敘述可對應 `Course`、`Chapter`、`Question`、`Tag` 或 `CourseSetting` 的既有行為。
- [x] 1.2 實作 Auth-aware primary action：公開首頁的「建立我的第一門課」在未登入時導向 `account_login`、已登入時導向 `learning:course-list`，不新增端點或資料欄位；在 `apps/core/tests.py` 建立首頁測試，使用未登入與已登入請求驗證兩種命名 URL。以 `python manage.py test apps.core` 驗證。[after: 1.1]

## 2. 響應式與可用性

- [x] 2.1 實作 Accessible responsive homepage 與 Accessible progressive enhancement：窄螢幕仍顯示首屏、主要行動與所有流程內容；在 JavaScript 停用時，導覽與內容仍可用；互動控制項具可見鍵盤焦點；減少動態效果偏好會停用裝飾性動畫與平滑捲動。以窄螢幕手動檢查、鍵盤 Tab、停用 JavaScript 與 `prefers-reduced-motion: reduce` 的瀏覽器模擬驗證。[after: 1.2]

## 3. 整合驗證

- [x] 3.1 執行首頁變更的整合驗證：確認完成後的首頁同時滿足 Accurate public learning workflow、Auth-aware first-course action 與 Accessible responsive homepage 三項規格，並確認既有課程列表、登入與註冊入口仍可到達。以 `python manage.py test`、登入／未登入的手動首頁導覽，以及桌面與窄螢幕檢查驗證。[after: 2.1]
