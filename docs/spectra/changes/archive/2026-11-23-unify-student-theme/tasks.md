## 1. 建立統一主題

- [x] 1.1 實作 Shared semantic color tokens：新增共用靜態主題樣式檔，定義 `--page-bg`、`--surface`、`--surface-subtle`、`--primary-surface`、`--primary-surface-hover`、`--border`、`--text`、`--text-muted` 與 `--focus`，並讓所有目標模板能透過 Django static 載入；權杖須對應 Bright Morandi purple-white palette 的確認色碼。以模板渲染檢查與靜態檔內容檢查驗證權杖存在且不依賴外部資產。
- [x] 1.2 實作 Scoped student-facing templates 的帳號頁部分：登入、註冊與登出頁載入共用主題並以語意權杖統一背景、卡片、輸入框、主要／次要按鈕、文字、焦點與錯誤狀態，且保留所有帳號表單的提交與導向行為。以未登入瀏覽器檢查及 `uv run python manage.py test` 驗證。[after: 1.1]
- [x] 1.3 實作 Scoped student-facing templates 的學習頁部分：課程列表、詳情、建立課程、建立錯題與課程設定頁載入共用主題，並以相同語意權杖呈現背景、卡片、輸入、標籤、按鈕、文字與鍵盤焦點；保留 URL、欄位、擁有者限制與表單行為。以登入使用者的瀏覽器檢查及 `uv run python manage.py test` 驗證。[after: 1.2]
- [x] 1.4 實作 Bright Morandi purple-white palette 的首頁部分：將首頁現有粉紅與鼠尾草綠品牌色替換為共用霧白、淺霧紫與柔亮紫權杖，保留現有版面、登入狀態分流、連結目的地與減少動態效果行為。以桌面及窄螢幕手動檢查，並執行 `uv run python manage.py test apps.core.tests.HomePageTests` 驗證。[after: 1.3]

## 2. 跨頁驗證

- [x] 2.1 驗證所有納入頁面的 Shared semantic color tokens：確認九個目標模板皆載入共用主題，舊的粉紅與鼠尾草綠品牌色未殘留於學生／訪客介面，深文字與焦點狀態在明亮表面上仍清楚可辨；Django `/admin/` 未被修改。以模板搜尋、桌面與窄螢幕瀏覽器檢查、鍵盤 Tab 檢查及 `uv run python manage.py test` 驗證。[after: 1.4]
