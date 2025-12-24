# LINE AI 網路搜尋聊天機器人

一個整合 LINE Bot、Google Gemini AI 和網路搜尋功能的智能聊天機器人。

## 功能特色

- 🤖 **LINE Bot 整合**：透過 LINE 訊息介面與使用者互動
- 🧠 **AI 智慧回覆**：使用 Google Gemini AI 生成自然對話
- 🔍 **網路搜尋**：自動判斷是否需要搜尋最新資訊
- 💬 **對話管理**：維持多輪對話脈絡
- 🚀 **WSGI 部署**：支援生產環境部署

## 系統需求

- Python 3.8+
- LINE Developers 帳號
- Google AI Studio API 金鑰

## 安裝步驟

### 1. 複製專案

```bash
git clone <repository-url>
cd linebot_search
```

### 2. 建立虛擬環境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 4. 環境變數設定

複製 `env.txt` 為 `.env` 並填入您的 API 金鑰：

```bash
cp env.txt .env
```

編輯 `.env` 檔案，填入以下資訊：

```env
# LINE Bot 設定（從 LINE Developers 控制台取得）
LINE_CHANNEL_ACCESS_TOKEN=您的_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=您的_CHANNEL_SECRET

# Google Gemini API 設定（從 Google AI Studio 取得）
GEMINI_API_KEY=您的_GEMINI_API_KEY
```

## 使用方法

### 本地測試

```bash
python main.py
```

應用程式將在 `http://localhost:5000` 啟動。

### 與機器人互動

1. 在 LINE 中新增您的 Bot 為好友
2. 傳送以 `@助教` 開頭的訊息
3. 機器人會根據內容判斷是否需要搜尋網路資訊
4. 獲得 AI 生成的智慧回覆

### 訊息格式

- **觸發關鍵字**：訊息必須以 `@助教` 開頭
- **搜尋功能**：機器人會自動判斷是否需要網路搜尋
- **對話限制**：每次交談限制為 30 個字，需說「繼續」獲取更多內容

## 專案結構

```
.
├── main.py              # Flask 應用程式主檔案
├── wsgi.py              # WSGI 部署配置
├── requirements.txt     # Python 相依套件
├── .env                 # 環境變數（需自行建立）
├── env.txt              # 環境變數範例
├── .gitignore          # Git 忽略檔案
└── README.md           # 專案說明
```

## 部署說明

### PythonAnywhere 部署

1. **上傳程式碼**：將專案檔案上傳到 PythonAnywhere
2. **設定環境變數**：在 PythonAnywhere 設定頁面配置環境變數
3. **WSGI 配置**：設定 WSGI 檔案路徑指向 `wsgi.py`
4. **安裝相依套件**：在 PythonAnywhere 的 console 中執行 `pip install -r requirements.txt`

### 環境變數配置

在生產環境中，確保以下環境變數已設定：

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`
- `GEMINI_API_KEY`

## API 說明

### LINE Bot Webhook

- **端點**：`/callback`
- **方法**：POST
- **功能**：接收 LINE 平台推送的訊息

### 健康檢查

- **端點**：`/`
- **方法**：GET
- **回應**：Welcome to LINE AI Search Bot!

## 開發說明

### 日誌系統

應用程式使用 Python logging 模組記錄重要事件：
- 訊息接收和處理
- API 呼叫結果
- 錯誤和警告

### 對話管理

- 每個使用者維持獨立的對話歷史
- 限制對話回合為 2 輪（4 條訊息）
- 自動清理舊對話

### 搜尋決策

使用 Gemini AI 判斷是否需要進行網路搜尋：
- 最新事件、時事內容 → 需要搜尋
- 一般知識、概念解釋 → 不需要搜尋

## 注意事項

1. **API 安全性**：務必將 `.env` 檔案加入 `.gitignore`，避免敏感資訊外洩
2. **搜尋限制**：網路搜尋功能依賴 Google 搜尋，建議控制使用頻率
3. **回覆長度**：AI 回覆限制在 30 個字內，用戶需主動要求繼續
4. **錯誤處理**：應用程式包含完善的錯誤處理機制

## 授權

本專案僅供學習和個人使用，請遵守相關服務條款。

## 聯絡資訊

如有問題或建議，請透過專案 Issue 頁面聯絡。
