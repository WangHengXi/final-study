## 1. 建立可驗證的共用導覽框架

- [x] 1.1 先為「Shared application shell」、「Guest navigation」與「Authenticated navigation」加入 Django 回應測試：驗證 core base 的資產與 block 契約、訪客的首頁／登入／註冊入口，以及沒有 UserProfile 的登入使用者仍能看到首頁／我的課程／含 CSRF 的 POST 登出；以 focused test 在尚未建立 navbar 前失敗作為 RED 證據。

- [x] 1.2 [after: 1.1] 依「Core owns the reusable base template and navbar partial」建立 `core/base.html`、`core/includes/navbar.html` 與 `core/navbar.css`，並依「Default navbar covers authenticated and guest navigation without profile dependence」完成 core 的可重用導覽契約；以 `findstatic core/navbar.css` 和 base template 載入檢查確認 core 資產可使用，跨頁回應測試保留到各模板遷移任務轉為 GREEN。

## 2. 將頁面接入共用框架

- [x] 2.1 [after: 1.2] 依「Base template exposes explicit blocks and preserves asset order」將首頁改為繼承 core base，提供 title、page CSS 與內容 block，並覆寫 navbar 與 vendor assets 以保留原本品牌＋標語 header 和不載入 Tailwind CDN 的行為；以首頁回應測試確認沒有預設 navbar 重複、既有首頁 CSS／theme 連結與訪客／登入分流均保持正確。

- [x] 2.2 [after: 1.2] 依「Base template exposes explicit blocks and preserves asset order」將五個 learning 模板改為繼承 core base，讓預設 navbar 與每頁既有 CSS／Tailwind 資產各只渲染一次；以登入使用者的課程列表、詳情、建立課程、錯題與設定頁回應測試確認「Shared application shell」及「Authenticated navigation」均成立並轉為 GREEN。

- [x] 2.3 [after: 1.2] 依「Base template exposes explicit blocks and preserves asset order」將登入、註冊與登出模板改為繼承 core base，保留原本表單 action、CSRF 欄位與 account CSS；以訪客／登入使用者回應測試確認「Guest navigation」與「Authenticated navigation」及資產載入順序正確並轉為 GREEN。

## 3. 保留情境式頁面導覽並完成驗證

- [x] 3.1 [after: 2.1, 2.2, 2.3] 依「Page-local back links remain in page content」驗證「Page-specific navigation remains available」：課程詳情與表單頁仍有原本的返回連結，首頁仍只保留其自訂 header；執行 `python manage.py test`、`python manage.py findstatic core/navbar.css` 與模板靜態掃描，確認不遺留重複完整 HTML head 或重複 navbar。
