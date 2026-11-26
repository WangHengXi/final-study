## Summary

將 StudyTrack 目前殘留的粉紅、鼠尾草綠與局部硬編碼樣式，統一為成熟、低飽和的莫蘭迪紫白視覺系統。

## Motivation

使用者已明確拒絕粉綠混色；目前首頁雖使用灰紫，但課程頁仍直接使用粉色 `#EAD1D7`，且主題樣式需靠覆蓋舊色彩才能維持一致。這會讓公開首頁、個人備考 Overview、行事曆與課程管理頁呈現不同的視覺語氣，削弱考研備考工具應有的沉穩感。

## Proposed Solution

- 建立唯一的紫白色彩角色：背景白、卡片白、淡灰紫、主要灰紫、深灰紫文字與對應邊框／焦點狀態。
- 移除使用者可見介面中的粉色、綠色與玫瑰色；課程、行事曆事項與重點區塊改以紫白層次，而非不同顏色區分。
- 將首頁、備考 Overview、行事曆、任務表單、課程清單、課程詳情與課程相關表單接至同一套主題語彙。
- 保持現有資訊架構、導覽、資料操作與可存取性行為，不新增或移除產品功能。

## Non-Goals (optional)

- 不重新設計資訊架構、頁面文案、資料模型、路由或行事曆操作流程。
- 不加入深色模式、使用者自訂主題、依課程分類上色或新的動畫效果。
- 不以截圖或影像資產取代可存取的 HTML／CSS 介面。

## Alternatives Considered (optional)

- 僅修改共用主題覆蓋規則：不採用，因課程模板仍會保留粉綠硬編碼，後續新增頁面也容易再次繞過主題。
- 保留多色課程分類、僅降低飽和度：不採用，仍違反使用者要求的單一紫白系統。

## Impact

- Affected specs: 新增 `morandi-purple-white-visual-system`
- Affected code:
  - Modified: `apps/core/static/core/studytrack-theme.css`
  - Modified: `static/final-study/css/home.css`
  - Modified: `static/final-study/css/study-calendar.css`
  - Modified: `apps/core/static/core/navbar.css`
  - Modified: `apps/learning/templates/learning/course_form.html`
  - Modified: `apps/learning/templates/learning/course_detail.html`
  - Modified: `apps/learning/templates/learning/course_list.html`
  - Modified: `apps/learning/templates/learning/course_setting_form.html`
  - Modified: `apps/learning/templates/learning/question_form.html`
  - Modified: `apps/core/templates/core/dashboard.html`
  - New: `apps/core/test_visual_theme.py`
  - Removed: none
