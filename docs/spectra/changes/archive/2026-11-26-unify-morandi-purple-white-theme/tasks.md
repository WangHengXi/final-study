## 1. 建立共用紫白色彩系統

- [x] 1.1 A shared Morandi purple-and-white palette：在 `apps/core/static/core/studytrack-theme.css` 定義背景白、卡片白、淡灰紫、灰紫主色、深灰紫文字、輔助文字、邊框與焦點角色，並讓首頁、導覽與月曆可直接使用；以模板與樣式來源檢查確認色票值可用且未以頁面專屬粉綠色補足介面。
- [x] 1.2 [after: 1.1] Replace source colors instead of relying on CSS overrides，將 `static/final-study/css/home.css`、`apps/core/static/core/navbar.css` 與 `static/final-study/css/study-calendar.css` 的裝飾表面、按鈕、標籤與事項摘要改為共用紫白角色，並刪除僅為舊粉綠／玫瑰值服務的覆蓋規則；以首頁、Overview、導覽與行事曆的桌面及窄螢幕手動檢查確認只顯示紫白層次。

## 2. 遷移課程介面與互動回饋

- [x] 2.1 [after: 1.1] Decorative multicolor course styling is absent：將課程清單、課程詳情、課程建立／編輯、課程設定與題目表單中可見的粉紅、綠色、玫瑰色背景、課程圓點、按鈕、徽章與卡片改為共用紫白角色；以登入後逐頁人工檢查確認課程與任務透過文字、位置、白／淡紫表面和灰紫互動狀態區分。
- [x] 2.2 [after: 2.1] Preserve semantic feedback without decorative multicolor surfaces：調整受影響欄位、連結與按鈕的 hover、focus、disabled 與驗證錯誤呈現，使 Interactive and validation feedback remain distinguishable，且錯誤僅以可讀文字回饋而非粉綠／玫瑰裝飾底色；以鍵盤焦點巡覽及空白必填欄位提交手動驗證。

## 3. 防止舊色回歸並驗證

- [x] 3.1 [after: 1.2, 2.2] Verify rendered pages and source-level palette boundaries，同時滿足 Deprecated decorative palette sources do not return：新增或擴充 `apps/core/test_visual_theme.py`，確認首頁、Overview、行事曆與課程頁載入共用主題，並檢查受影響模板與 CSS 不含 `#EAD1D7`、`#DFBEC7`、`#DFBCC6`、`#F0F3F0`、`#F0E7EB`、`#E7ECE9`；以 `.venv/bin/python manage.py test` 與上述目標頁的手動紫白檢查驗證。
