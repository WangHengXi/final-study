## Context

目前 core、learning 與 account 的模板沒有使用 `{% extends %}`。每個完整頁面各自宣告 HTML head、`{% load static %}`、主題 CSS，且多數頁面各自放置品牌或返回連結。課程列表另有唯一一份依登入狀態顯示登入／註冊／登出的標記。Django 已啟用 app template discovery，專案層模板目錄 `templates/` 也可解析 app template，因此 core 可以安全提供給其他 app 繼承的版型。

這是一個跨 core、learning 與 account 的結構調整。core 是共同 UI 的擁有者；learning 與 account 分別是兩個實際使用該模板契約的接入端。

## Goals / Non-Goals

**Goals:**

- 以 core app 提供一份可重用的 base template、navbar partial 與 navbar CSS。
- 讓首頁、學習頁與帳號頁共用 head、靜態資產載入與導航規則，同時允許頁面內容與 CSS 保持獨立。
- 讓訪客取得首頁、登入與註冊入口；登入使用者取得首頁、我的課程與安全的 POST 登出入口。
- 保留首頁既有的品牌＋標語 header，以及各表單／詳情頁目前的情境式返回連結。

**Non-Goals:**

- 不改變路由、登入流程、課程權限、表單資料或頁面文案。
- 不重寫既有 `static/final-study/css/` 的頁面專屬樣式，也不新增 JavaScript 或前端建置工具。
- 不讓共用導航存取 `user.profile`；沒有 UserProfile 的使用者仍必須能渲染導航。
- 不遷移 `core/greeting.html` 的極簡回應頁。

## Decisions

### Core owns the reusable base template and navbar partial

建立 `core/base.html` 與 `core/includes/navbar.html`，並將 navbar CSS 放在 `apps/core/static/core/navbar.css`。core 已持有 `studytrack-theme.css`，因此將共同 UI 放在同一 app 可避免讓 learning 或 account 擁有全站框架。

替代方案是放在根目錄 `templates/`；雖能工作，但使 UI 所有權分散。以 JavaScript 注入則會增加載入依賴並不利於無 JavaScript 的導覽。

### Base template exposes explicit blocks and preserves asset order

`core/base.html` 提供 `title`、`vendor_assets`、`page_css`、`navbar`、`content` 與 `body_class` block。預設 `vendor_assets` 載入既有 Tailwind CDN；`page_css` 由各子模板載入自己的 CSS，接著 base 載入 `core/studytrack-theme.css` 與 `core/navbar.css`。這保留目前頁面 CSS 先於主題覆寫的相對順序。

首頁覆寫空的 `vendor_assets`，避免引入原本不存在的 Tailwind reset；首頁也覆寫 `navbar`，保留現有 header。其他使用者面對的 learning 與 account 頁使用預設 navbar。

### Default navbar covers authenticated and guest navigation without profile dependence

navbar 的品牌連結導向首頁。訪客看到登入與註冊連結；登入使用者看到我的課程連結與含 CSRF 的 POST 登出表單。使用者識別只可使用 `user.username` 或不顯示名稱，不能存取可缺少的 `user.profile`。

替代方案是繼續保留課程列表中的導航分支；這會讓其他頁沒有一致入口且重複登入狀態判斷。

### Page-local back links remain in page content

「回到課程」和「回到課程列表」帶有章節、課程或表單的情境，因此保留在子模板內容中。navbar 只提供跨頁導覽，避免把動態物件 URL 變成共用模板的必要 context。

## Implementation Contract

- 使用預設 navbar 的 account 與 learning 頁，渲染後必須包含品牌首頁連結；訪客還必須看到登入與註冊連結，登入使用者還必須看到我的課程連結及含 CSRF 的 POST 登出表單。
- 所有遷移至 base 的頁面必須透過 block 供應其 title、頁面內容與需要的頁面 CSS，且每頁既有的 `static/final-study/css/` 連結仍會出現在回應中。
- 除首頁外，既有使用 Tailwind 的頁面每次回應只保留原本的一個 Tailwind CDN script；首頁不新增該 script。
- 首頁必須保留現有品牌＋標語 header，不能同時渲染預設 navbar；detail／form 頁的情境式返回連結必須保留。
- 導航列不可因缺少 UserProfile 而產生 template rendering error；導覽不以 `user.profile` 作必要資料。
- 範圍內：core base/partial/CSS、九個使用者面對模板的繼承調整與回歸測試。
- 範圍外：`core/greeting.html`、路由／視圖／模型調整、頁面內容重設計、第三方資產自託管。

## Risks / Trade-offs

- [base 中的資產順序改變外觀] → 以 page CSS、theme、navbar CSS 的固定順序載入，並以回應測試確認各頁資產仍存在。
- [預設 navbar 與首頁現有 header 重複] → 首頁明確覆寫 `navbar` block。
- [登出頁的 navbar 與確認登出表單重複操作] → navbar 提供全站入口，確認頁保留原有明確操作；兩者皆使用 POST 和 CSRF。
- [缺少 UserProfile 的帳號無法渲染] → navbar 不存取 profile，測試以只建立 Django user 的登入狀態驗證。

## Migration Plan

1. 先加入 base template、navbar partial、navbar CSS 與回歸測試。
2. 逐組遷移 home、learning、account 模板；每組保持可渲染並跑測試。
3. 移除已由 base 提供的重複 head 與課程列表登入狀態導航。
4. 若需回復，將子模板還原為完整文件，並移除 base、partial 與 navbar CSS；不涉及資料庫或資料遷移。

## Open Questions

無。
