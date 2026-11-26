## Context

根路徑目前會對登入者呈現個人備考內容，造成公開產品介紹頁消失。讀書事項模型與遷移已在程式庫中，但測試站資料庫未套用遷移，讀取行事曆時缺少資料表。

## Goals / Non-Goals

**Goals:**

- 將公開首頁與個人備考總覽分成不同路徑。
- 讓導覽以單一下拉式選單提供登入後功能。
- 將缺少資料表的部署步驟變成可驗證的修復流程。

**Non-Goals:**

- 不在本次實作複習分析功能；僅預留選單位置。
- 不更改讀書事項的欄位、行事曆互動或課程資料。

## Decisions

### Keep the root route as a public landing page

`/` 一律渲染公開產品介紹，已登入使用者也能回到此頁。獨立的 `/overview/` 僅供登入者使用，登入成功後導向該路徑。此做法保留可分享的產品入口，避免私人摘要取代公開說明。

### Use one authenticated navigation dropdown

登入後導覽以單一「選單」控制項收納備考 Overview、行事曆、我的課程、複習分析（顯示即將推出）與登出。選單外僅保留品牌連結。這取代分散的膠囊按鈕，亦可容納後續功能。

### Apply the study-task migration before calendar traffic

部署程序必須在新版本啟用前執行 `.venv/bin/python manage.py migrate`，並以 `showmigrations learning` 確認 `0007_studytask` 已套用。缺少資料表是部署狀態，不以執行期吞錯隱藏。

## Implementation Contract

- 訪客與已登入使用者請求 `/` 都得到公開首頁，且不含個人任務。
- `/overview/` 需要登入，顯示現有今日任務摘要；成功登入預設抵達此路徑。
- 已登入導覽有可鍵盤操作的下拉選單；選單的可用項目能前往 Overview、行事曆、課程，登出維持 POST 與 CSRF。複習分析為不可導覽的「即將推出」標示。
- 測試站執行遷移後，`/learning/calendar/` 不再因 `learning_studytask` 缺表而回傳 500。
- 驗收包含 Django 路由／導覽測試、`python manage.py migrate` 與行事曆回應檢查。

## Risks / Trade-offs

- [已登入者預期根路徑是個人頁] → 登入後導向 Overview，導覽明確標示其位置。
- [下拉選單的鍵盤操作不足] → 使用語意 button、`aria-expanded` 與焦點可見樣式。
- [遷移漏跑再次造成 500] → 部署清單加入遷移與 `showmigrations` 檢查。

## Migration Plan

1. 部署程式與遷移檔。
2. 在測試站執行 `.venv/bin/python manage.py migrate`。
3. 執行 `.venv/bin/python manage.py showmigrations learning`，確認 `0007_studytask` 有 `[X]`。
4. 登入後開啟 Overview 與行事曆驗證。
