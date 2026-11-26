## 1. 每日讀書事項資料與輸入規則

- [x] 1.1 實作 **Store daily study tasks with user-owned dates**：在 `apps/learning/models.py` 與遷移中加入 `StudyTask`，包含使用者擁有權、日期、120 字以內標題、可選課程、備註與完成狀態；驗證以模型測試確認同日可有多筆、資料依擁有者隔離，並執行 `python manage.py makemigrations --check`。
- [x] 1.2 實作 **Create and edit a dated study task** 的表單資料契約：只列出目前使用者的課程、拒絕空白或過長標題與他人課程，並保留無效提交的欄位值；以 `StudyTaskFormTests` 覆蓋有效與無效輸入。

## 2. 私人月曆與事項操作

- [x] 2.1 [after: 1.1, 1.2] 實作 **Server-render a monthly calendar with accessible task controls** 與 **Private monthly study calendar**：新增受登入保護的 `/learning/calendar/` 月曆、前後月導覽、無效 month 回退當月、按日顯示本人事項與可讀的新增入口；以 `StudyCalendarViewTests` 驗證月份切換、當月回退與跨使用者資料不外洩。
- [x] 2.2 [after: 2.1] 完成 **Create and edit a dated study task** 的新增與編輯頁面：有效提交後回到該事項所在月份，錯誤表單不寫入資料並顯示欄位錯誤；以 Django client 測試驗證本人課程可關聯、他人課程遭拒絕與日期月份導向。
- [x] 2.3 [after: 2.2] 完成 **Manage completion and removal of personal tasks**：以 CSRF 保護的 POST 切換完成與刪除，成功後回到來源月份，其他使用者對讀取、編輯、切換及刪除皆得到 404；以 `StudyTaskOwnershipTests` 驗證狀態轉換與所有權保護。

## 3. 登入後備考首頁與導覽

- [x] 3.1 [after: 1.1] 實作 **Separate public landing page from authenticated study dashboard** 與 **Authenticated users reach a personal study dashboard**：讓根路徑依登入狀態呈現公開首頁或新備考首頁，並將無 return URL 的登入成功導向備考首頁；以 `HomePageTests` 驗證訪客不見私人資料、登入使用者到達備考首頁。
- [x] 3.2 [after: 3.1] 完成 **Dashboard summarizes only today's personal tasks**：備考首頁依當前日期只列出目前使用者的未完成與已完成事項，無事項時顯示明確空狀態，且含新增今日安排、行事曆及課程入口；以固定日期的 Django 測試驗證資料隔離與空狀態。
- [x] 3.3 [after: 2.1, 3.1] 完成 **Authenticated navigation**：登入後共用導覽可前往備考首頁、行事曆、我的課程及使用 POST 的安全登出，訪客導覽維持首頁、登入、註冊；以 `apps/core/test_navigation.py` 驗證含 CSRF 的登出表單與所有連結。

## 4. 公開首頁與一致視覺

- [x] 4.1 實作 **Use a single Morandi purple and white visual system**：在首頁、備考首頁與行事曆使用暖白、灰紫、深紫與淡紫的共同視覺 token，移除粉紅、綠色、多色手帳卡片與便條紙效果；以桌面及窄螢幕手動檢查確認配色、鍵盤焦點、可讀文字與版面未溢出。
- [x] 4.2 [after: 4.1] 完成 **Accurate public learning workflow**：將公開首頁文案與示意換成中性備考的課程、章節、錯題、複習設定與個人安排語境，且不宣稱統計、提醒、重複排程或同步功能；以首頁回應內容測試與人工文案檢查確認。

## 5. 整合驗收

- [x] 5.1 [after: 2.3, 3.2, 3.3, 4.2] 執行 `python manage.py test` 與 `spectra validate refresh-landing-and-add-study-calendar`，確認既有課程流程、導覽、公開首頁、備考首頁及行事曆規格皆通過；修正測試或規格落差後重新執行兩項驗證。
