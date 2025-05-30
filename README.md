# Threads 帖文爬蟲工具

這是一個用於抓取 Threads 用戶帖文的 Python 工具。該工具可以自動獲取指定用戶的 Threads 頁面內容，解析帖文數據，並將結果保存為結構化的 JSON 格式。

## 功能特點

- 自動抓取指定用戶的 Threads 頁面
- 解析帖文內容和相關信息
- 將結果保存為 JSON 格式
- 模塊化設計，便於維護和擴展
- 內置錯誤處理機制

## 項目結構

```
.
├── main.py              # 主程序入口
├── scarch_html.py       # 網頁內容獲取模塊
├── scarch_parser.py     # HTML 解析模塊
├── requirements.txt     # 項目依賴
├── output/             # 輸出目錄
│   └── posts_*.json    # 解析結果
└── README.md           # 項目說明
```

### 模塊說明

- `main.py`: 程序主入口，協調各模塊工作
- `scarch_html.py`: 負責訪問並下載目標頁面的 HTML 內容
- `scarch_parser.py`: 解析 HTML 內容，提取所需的帖文數據

## 環境要求

- Python 3.10
- FastAPI 0.110.0
- Playwright 1.42.0
- BeautifulSoup4 4.12.2
- Uvicorn 0.27.1
- 其他依賴見 requirements.txt

## 安裝

1. 克隆此倉庫：
```bash
git clone [你的倉庫URL]
cd [倉庫名稱]
```

2. 創建並激活虛擬環境：

Windows:
```bash
# 創建虛擬環境
python -m venv .venv

# 激活虛擬環境
.\.venv\Scripts\Activate.ps1  # PowerShell
# 或
.\.venv\Scripts\activate.bat  # CMD
```

Linux/macOS:
```bash
# 創建虛擬環境
python -m venv .venv

# 激活虛擬環境
source .venv/bin/activate
```

3. 安裝依賴：
```bash
# 安裝所有 Python 包
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
playwright install
```

4. 如果安裝過程中遇到 greenlet 包的問題，可以嘗試：
```bash
# 安裝最新版本的 greenlet
pip install greenlet==3.2.0
```

## 運行服務

啟動 FastAPI 服務器：
```bash
# 開發模式（自動重載）
python app.py

# 或使用 uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

服務啟動後，可以通過以下地址訪問：
- API 文檔：http://localhost:8000/docs
- 交互式 API 文檔：http://localhost:8000/redoc
- API 根路徑：http://localhost:8000/

## 使用方法

運行程序並指定要爬取的用戶名：
```bash
python main.py -u <用戶名>
```

例如：
```bash
python main.py -u ray.realms
```

您也可以使用完整的參數名：
```bash
python main.py --username ray.realms
```

## 輸出格式

程序會在 `output` 目錄下生成 JSON 文件，格式如下：

```json
{
  "user": "用戶名",
  "posts": [
    {
      "content": "帖文內容",
      "timestamp": "發布時間",
      "likes": "點贊數",
      "replies": "評論數"
    },
    // ... 更多帖文
  ]
}
```

## 注意事項

- 請確保遵守 Threads 的使用條款和政策
- 建議適當控制爬取頻率，避免對服務器造成過大負擔
- 首次運行時會自動創建 `output` 目錄
- 確保系統有足夠的磁盤空間存儲輸出文件

## 常見問題

1. 如果遇到網絡錯誤，程序會自動重試
2. 輸出文件使用 UTF-8 編碼，確保正確處理中文內容
3. 如需修改輸出目錄，可以在 `main.py` 中設置

## 貢獻指南

歡迎提交 Issue 和 Pull Request 來改進這個項目。在提交之前，請確保：

1. 代碼符合 PEP 8 規範
2. 添加了適當的註釋和文檔
3. 通過了所有測試

## 授權

本項目採用 MIT 授權協議。詳見 [LICENSE](LICENSE) 文件。

## 作者

kuo6

## 更新日誌

- v1.0.3 (2024-03-21)
  - 代碼優化和穩定性改進
  - 更新依賴包版本
  - 完善錯誤處理機制

- v1.0.1 (2025-04-21)
  - 添加命令行參數支持
  - 保持互動數據為原始字符串格式
  - 優化錯誤處理

- v1.0.0 (2025-04-21)
  - 初始版本發布
  - 實現基本的爬取功能
  - 添加錯誤處理機制 