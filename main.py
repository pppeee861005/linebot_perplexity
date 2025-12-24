#########################################################################
# Python x AI Agent
# Flask, Linebot, deployment - 網站伺服器串聯LINE服務
#
# [作業]
# LINE AI Bot 自主網搜聊天機器人
##########################################################################

import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 載入環境變數
load_dotenv()

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 從環境變數取得配置（使用 os.environ 直接存取）
try:
    LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
except KeyError as e:
    logger.error(f"缺少環境變數: {e}")
    raise

# 初始化 LINE Bot API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始化 Gemini API
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# 搜尋決策樣板
SEARCH_DECISION_TEMPLATE = '''
根據以下對話歷史和使用者的最新訊息，判斷是否需要進行網路搜尋才能提供準確的回覆。

對話歷史:
{history}

使用者訊息: {message}

請以以下 JSON 格式回覆（只回覆 JSON，不要其他文字）:
{{
    "search": "Y" 或 "N",
    "keyword": "如果需要搜尋，提供搜尋關鍵字；否則留空"
}}

判斷標準:
- 如果訊息涉及最新事件、時事、產品發布等需要最新資訊的內容，回覆 "Y"
- 如果訊息是一般知識、概念解釋或不需要最新資訊的內容，回覆 "N"
'''

# 對話管理器
class ConversationManager:
    """管理每個使用者的對話歷史，限制為 2 個回合（4 條訊息）"""

    def __init__(self, max_exchanges=2):
        self.conversations = {}
        self.max_messages = max_exchanges * 2

    def add_message(self, user_id, content):
        """新增訊息到使用者的對話歷史"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []

        self.conversations[user_id].append(content)

        if len(self.conversations[user_id]) > self.max_messages:
            self.conversations[user_id] = self.conversations[user_id][-self.max_messages:]

    def get_history(self, user_id):
        """取得使用者的對話歷史"""
        return self.conversations.get(user_id, [])

    def clear_history(self, user_id):
        """清除使用者的對話歷史"""
        if user_id in self.conversations:
            del self.conversations[user_id]

# 全域對話管理器實例
conversation_manager = ConversationManager()

# 觸發過濾器
class TriggerFilter:
    """檢測訊息是否以 @助教 開頭，決定是否觸發 AI 回應"""

    TRIGGER_KEYWORD = "@助教"

    @staticmethod
    def is_triggered(message):
        """檢查訊息是否以 @助教 開頭"""
        return message.strip().startswith(TriggerFilter.TRIGGER_KEYWORD)

    @staticmethod
    def extract_content(message):
        """提取 @助教 之後的內容"""
        if TriggerFilter.is_triggered(message):
            content = message[len(TriggerFilter.TRIGGER_KEYWORD):].strip()
            return content
        return None

# Google 搜尋模組
class GoogleSearchModule:
    """執行 Google 網路搜尋"""

    def search(self, keyword, num_results=5):
        """執行 Google 搜尋"""
        try:
            from googlesearch import search
            results = []
            for url in search(keyword, num_results=num_results, lang="zh-TW"):
                results.append(url)

            if not results:
                return "未找到相關搜尋結果。"

            result_text = f"搜尋關鍵字: {keyword}\n搜尋結果:\n"
            for i, url in enumerate(results, 1):
                result_text += f"{i}. {url}\n"

            return result_text
        except Exception as e:
            logger.error(f"Google 搜尋錯誤: {e}")
            return f"搜尋失敗: {str(e)}"

# 全域搜尋模組實例
search_module = GoogleSearchModule()

# 建立 Flask 應用程式
def create_app():
    """建立 Flask 應用程式"""
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Welcome to LINE AI Search Bot!'

    @app.route('/callback', methods=['POST'])
    def callback():
        """LINE webhook 回調端點"""
        signature = request.headers.get('X-Line-Signature', '')
        body = request.get_data(as_text=True)

        logger.info(f"Request body: {body}")

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            logger.warning("無效的 LINE 簽名")
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        """處理 LINE 文字訊息"""
        user_id = event.source.user_id
        user_message = event.message.text

        logger.info(f"收到來自 {user_id} 的訊息: {user_message}")

        # 檢查訊息是否以 @助教 開頭
        if not TriggerFilter.is_triggered(user_message):
            logger.info(f"訊息未觸發 @助教，忽略")
            return

        # 提取 @助教 之後的內容
        triggered_content = TriggerFilter.extract_content(user_message)

        try:
            # 新增使用者訊息到歷史
            conversation_manager.add_message(user_id, triggered_content)

            # 取得對話歷史
            history = conversation_manager.get_history(user_id)

            # 構建歷史字符串
            history_str = "\n".join(history[:-1]) if len(history) > 1 else "（無歷史）"

            # 判斷是否需要搜尋
            search_prompt = SEARCH_DECISION_TEMPLATE.format(
                history=history_str,
                message=triggered_content
            )

            try:
                search_response = gemini_client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=[search_prompt]
                )
                search_decision = json.loads(search_response.text)
            except Exception as e:
                logger.warning(f"搜尋決策失敗: {e}")
                search_decision = {"search": "N", "keyword": ""}

            # 準備回覆內容
            reply_content = ""
            if search_decision.get("search") == "Y" and search_decision.get("keyword"):
                keyword = search_decision["keyword"]
                logger.info(f"執行搜尋: {keyword}")
                search_results = search_module.search(keyword)
                reply_content = f"搜尋結果:\n{search_results}\n\n"

            # 生成最終回覆
            system_prompt = """你是一個有幫助的 LINE 聊天機器人助手。請用繁體中文回覆。每次交談只顯示30個字，超過的部分，顯示請說繼續，如果使用者說繼續的話，你要說繼續要加錢。
            例如：從前有一隻小豬，住在山上然後 ....請說{繼續}。使用者說：繼讀。你說：繼續要加錢!

            """

            # 構建完整訊息
            full_prompt = f"{system_prompt}\n\n對話歷史:\n{history_str}\n\n使用者訊息: {triggered_content}"

            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=[full_prompt]
            )

            reply_content += response.text

            # 新增 AI 回覆到歷史
            conversation_manager.add_message(user_id, response.text)

            # 發送回覆
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_content)
            )

            logger.info(f"已回覆 {user_id}")
        except Exception as e:
            logger.error(f"處理訊息時出錯: {e}")
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="抱歉，處理您的訊息時出現錯誤。請稍後再試。")
                )
            except Exception as send_error:
                logger.error(f"發送錯誤訊息失敗: {send_error}")

    return app

# 建立應用程式實例
app = create_app()

def main():
    """主函數 - 啟動 Flask 應用程式"""
    app.run(debug=False, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
