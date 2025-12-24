# LINE AI 聊天機器人使用指南

## 📋 **專案資訊**
- **版本**: v1.1.0
- **發佈日期**: 2025-12-24
- **功能**: 支援 @助教 與 @請查詢 兩種互動模式

## 🎯 **功能特色**

### 1. **雙重觸發模式**
本機器人支援兩種不同的互動模式：

#### 🧠 **@助教 模式** - AI 智慧對話
- **觸發方式**: `@助教 [您的問題]`
- **功能特點**:
  - AI 會判斷是否需要搜尋網路資訊
  - 提供智慧化的對話回覆
  - 支援多輪對話（記住對話歷史）
  - 自動決定是否執行 Perplexity 搜尋

#### 🔍 **@請查詢 模式** - 直接搜尋
- **觸發方式**: `@請查詢 [搜尋關鍵字]`
- **功能特點**:
  - 直接觸發 Perplexity AI 搜尋
  - 立即返回搜尋結果
  - 適合事實查詢、最新資訊等

## 🚀 **使用方法**

### 基本使用
1. **在 LINE 中加入機器人好友**
2. **發送訊息時以指定關鍵字開頭**

### 範例對話

#### 範例 1: 使用 @助教 模式
```
使用者: @助教 Python 的最新版本是什麼？
機器人: [AI 分析後決定搜尋]
       [顯示搜尋結果]
       [提供完整回覆]
```

#### 範例 2: 使用 @請查詢 模式
```
使用者: @請查詢 ChatGPT 最新功能
機器人: [直接顯示 Perplexity 搜尋結果]
```

#### 範例 3: 一般對話（無觸發）
```
使用者: 你好
機器人: [無回應 - 訊息被忽略]
```

## ⚙️ **部署指南**

### 環境需求
- Python 3.8+
- LINE Developer 帳號
- Gemini API 金鑰
- Perplexity API 金鑰

### 安裝步驟

#### 1. **下載專案**
```bash
git clone <repository-url>
cd line-bot-ai
```

#### 2. **安裝依賴**
```bash
pip install -r requirements.txt
```

#### 3. **環境變數配置**
建立 `.env` 檔案：
```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
GEMINI_API_KEY=your_gemini_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
```

#### 4. **啟動服務**
```bash
python main.py
```

### LINE Bot 設定
1. 前往 [LINE Developers](https://developers.line.biz/)
2. 建立新的 Channel
3. 設定 Webhook URL: `https://your-domain.com/callback`
4. 複製 Channel Access Token 和 Channel Secret

## 🔧 **API 配置**

### Gemini API
- 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
- 建立新的 API 金鑰
- 用於 AI 對話和搜尋決策

### Perplexity API
- 前往 [Perplexity AI](https://www.perplexity.ai/)
- 註冊並取得 API 金鑰
- 用於網路搜尋功能

## 📁 **專案結構**

```
line-bot-ai/
├── main.py                 # 主程式
├── requirements.txt        # Python 依賴
├── wsgi.py                # WSGI 入口
├── .env                   # 環境變數（需自行建立）
├── LINE_Bot_使用指南.md   # 本指南
├── 注意要點.md           # 開發注意事項
├── 虛擬環境指南.md        # 環境建置指南
└── git指南/              # Git 使用指南
```

## 🎮 **進階功能**

### 對話歷史管理
- 每個使用者最多保留 2 輪對話（4 條訊息）
- 自動清理舊的對話記錄

### 搜尋決策邏輯
- AI 會分析問題類型
- 判斷是否需要外部資訊
- 自動選擇適當的搜尋關鍵字

### 錯誤處理
- API 呼叫失敗時會顯示友好提示
- 網路問題自動重試
- 詳細的錯誤日誌記錄

## 🛠️ **開發與維護**

### 版本控制
```bash
# 切換到最新版本
git checkout main

# 查看舊版本
git checkout v1.0.0

# 建立功能分支
git checkout -b feature/new-feature
```

### 日誌查看
```bash
# 應用程式會自動記錄詳細日誌
# 查看啟動日誌
python main.py

# 日誌檔案位置：自動輸出到控制台
```

## ❓ **常見問題**

### Q: 機器人沒有回應？
A: 確保訊息以 `@助教` 或 `@請查詢` 開頭

### Q: 搜尋功能無效？
A: 檢查 Perplexity API 金鑰是否正確配置

### Q: AI 回覆品質不佳？
A: 確認 Gemini API 金鑰有效且有足夠額度

### Q: 如何重啟服務？
A: 終止程式後重新執行 `python main.py`

## 📞 **技術支援**

如遇技術問題，請檢查：
1. 環境變數配置
2. API 金鑰有效性
3. 網路連線狀態
4. Python 版本相容性

## 🔄 **更新日誌**

### v1.1.0 (2025-12-24)
- ✨ 新增 `@請查詢` 直接搜尋模式
- 🔧 重構觸發器系統支援多關鍵字
- 📈 優化搜尋決策邏輯
- 🐛 修復程式碼中的實例初始化問題

### v1.0.0 (2025-12-24)
- 🎉 初始版本發佈
- 🤖 實現 `@助教` AI 對話功能
- 🔍 整合 Perplexity 搜尋
- 💬 支援多輪對話歷史

---

**開發者**: LINE AI Bot Team
**最後更新**: 2025-12-24
