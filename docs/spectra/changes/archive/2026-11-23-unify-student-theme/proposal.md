## Why

目前首頁、帳號頁與學習頁各自直接寫入不同的粉紫、粉紅與綠色值；使用者在頁面之間切換時，無法感受到一致的 StudyTrack 品牌。現在需要以使用者已確認的明亮莫蘭迪紫白色票，讓學生與訪客的所有頁面形成同一套輕盈、專注的視覺體驗。

## What Changes

- 將公開首頁、帳號頁與學習頁的背景、卡片、邊框、主要按鈕、懸停狀態、文字與鍵盤焦點統一為明亮莫蘭迪紫白色票。
- 以霧白 `#FCFBFF`、卡片白 `#FFFFFF`、淺霧紫 `#F4F0F8`、柔亮紫 `#E7DCEF`、按鈕懸停色 `#DCCCE8`、淡紫邊框 `#E8E0EE`、墨紫文字 `#453C4D`、次要文字 `#746B7C` 與焦點色 `#A98DBC` 作為實作依據。
- 移除首頁與其他學生介面中的粉紅、鼠尾草綠及不屬於此色票的硬編碼裝飾色；錯誤訊息維持可辨識的低飽和暗紅例外。
- 保留既有頁面結構、文字、表單流程、登入狀態分流、連結目的地與無障礙焦點行為。

## Non-Goals

- 不改變 Django `/admin/` 管理後台。
- 不新增或變更資料模型、URL、API、表單欄位、登入流程或 AI 功能。
- 不重設首頁版面與文案，僅將既有外觀轉換至統一色票。

## Impact

- Affected specs: none
- Affected code:
  - New: (none)
  - Modified: `apps/core/templates/core/home.html`, `templates/account/login.html`, `templates/account/signup.html`, `templates/account/logout.html`, `apps/learning/templates/learning/course_list.html`, `apps/learning/templates/learning/course_detail.html`, `apps/learning/templates/learning/course_form.html`, `apps/learning/templates/learning/question_form.html`, `apps/learning/templates/learning/course_setting_form.html`
  - Removed: (none)
- Compatibility: no capability-level observable behavior changes
