## Summary

建立由 core app 擁有的共用頁面框架與導航列，讓首頁、學習頁與帳號頁能使用一致的品牌、登入狀態操作與靜態資產載入規則。

## Motivation

目前十個 Django 模板各自宣告文件 head、靜態檔與導覽相關標記。課程列表已包含登入／註冊／登出分支，其他頁則只有回上一頁連結或沒有全站導覽，造成共用 UI 重複且各頁導覽行為不一致。

## Proposed Solution

- 在 core app 建立可被專案模板載入的 base template 與 navbar partial，將品牌、首頁／我的課程入口與登入狀態操作集中維護。
- 讓學習頁與帳號頁繼承 core base template；每頁透過明確 block 提供 title、頁面 CSS 與內容。
- 讓首頁也繼承 base template，但覆寫導航區塊以保留目前的品牌與標語 header，並覆寫第三方資產區塊以維持首頁不載入 Tailwind CDN 的既有行為。
- 將 navbar 專屬 CSS 放入 `apps/core/static/core/`，並保留現有的 `core/studytrack-theme.css` 與各頁 `static/final-study/css/` 檔案的責任邊界。
- 以 Django 回應測試確認訪客與登入使用者都能看到正確導覽連結，且既有頁面 CSS、表單 action 與首頁登入狀態分流不變。

## Non-Goals (optional)

## Alternatives Considered (optional)

- 維持每頁各自複製導覽標記：短期變動小，但每次調整連結、登入狀態或樣式都要修改多個模板。
- 將 base template 放在專案根目錄 `templates/`：可以運作，但會讓全站 UI 的所有權脫離既有的 core app，與目前 `studytrack-theme.css` 的位置不一致。
- 以 JavaScript 動態插入導覽列：會增加載入與無 JavaScript 時的行為差異，Django template 繼承已能直接滿足需求。

## Impact

- Affected specs: shared-navigation (new)
- Affected code:
  - Modified: `apps/core/templates/core/home.html`, `apps/learning/templates/learning/course_list.html`, `apps/learning/templates/learning/course_detail.html`, `apps/learning/templates/learning/course_form.html`, `apps/learning/templates/learning/question_form.html`, `apps/learning/templates/learning/course_setting_form.html`, `templates/account/login.html`, `templates/account/signup.html`, `templates/account/logout.html`, `apps/core/tests.py`, `apps/core/test_static_assets.py`
  - New: `apps/core/templates/core/base.html`, `apps/core/templates/core/includes/navbar.html`, `apps/core/static/core/navbar.css`
  - Removed: duplicated document head、課程列表內重複的登入狀態導覽標記
