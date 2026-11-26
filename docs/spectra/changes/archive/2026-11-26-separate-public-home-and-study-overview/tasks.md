## 1. 公開首頁與 Overview 路由

- [x] 1.1 實作 **Keep the root route as a public landing page**、**Accurate public learning workflow** 與 **Any user sees the public product introduction**：根路徑不依登入狀態改變內容，且不顯示個人任務；以 `HomePageTests` 驗證訪客與登入使用者都看到公開首頁。
- [x] 1.2 [after: 1.1] 實作 **Authenticated study overview route**：新增受登入保護的 `/overview/`，讓登入成功預設導向此頁，並只摘要本人今日事項與空狀態；以 Django client 測試驗證導向與資料隔離。

## 2. 下拉式導覽與部署修復

- [x] 2.1 [after: 1.2] 實作 **Use one authenticated navigation dropdown** 與 **Authenticated user opens the navigation menu**：以具 `aria-expanded` 的選單取代登入後的分散按鈕，提供 Overview、行事曆、課程、不可導覽的複習分析提示與 CSRF 登出；以 `SharedNavigationTests` 驗證連結、可用狀態與登出表單。
- [x] 2.2 實作 **Apply the study-task migration before calendar traffic**：在測試站套用 `0007_studytask`，以 `.venv/bin/python manage.py showmigrations learning` 確認已套用，並對 `/learning/calendar/` 執行已登入的 smoke check，確認不再回傳缺表錯誤。

## 3. 整合驗收

- [x] 3.1 [after: 2.1, 2.2] 執行 `.venv/bin/python manage.py test`、`.venv/bin/python manage.py migrate --check` 與 `spectra validate separate-public-home-and-study-overview`；確認公開首頁、Overview、導覽與行事曆共同運作並記錄結果。
