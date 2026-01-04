#########################################################################
# Python x AI Agent
# Flask, Linebot, deployment - 網站伺服器串聯LINE服務
#
# Version: v1.2.0
# Release Date: 2025-12-24
# Description: LINE AI 聊天機器人 - 支援 @助教 與 @請查詢 雙重互動模式，JSON 解析已修復
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

# 應用程式版本資訊
__version__ = "1.2.0"
__author__ = "LINE AI Bot Developer"
__description__ = "LINE AI 聊天機器人 - 支援雙重互動模式"

# 從環境變數取得配置（使用 os.environ 直接存取）
try:
    LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']
    GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
    PERPLEXITY_API_KEY = os.environ['PERPLEXITY_API_KEY']  # 新增這行
except KeyError as e:
    logger.error(f"缺少環境變數: {e}")
    raise

# 初始化 LINE Bot API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始化 Gemini API
gemini_client = genai.Client(api_key=GEMINI_API_KEY)



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


class PerplexitySearchModule:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def search(self, query, num_results=5):
        """使用 Perplexity AI 進行搜尋"""
        try:
            import requests
            
            payload = {
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "user", 
                        "content": f"Search for: {query}. Provide {num_results} key results with brief descriptions."
                    }
                ],
                "max_tokens": 1000
            }
            
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # 格式化結果
            result = f"Perplexity 搜尋結果:\n{query}\n\n{content}"
            return result
            
        except Exception as e:
            return f"Perplexity 搜尋失敗: {str(e)}"


# 觸發過濾器
class TriggerFilter:
    """檢測訊息是否以支援的關鍵字開頭，決定是否觸發 AI 回應"""

    TRIGGER_KEYWORDS = ["@助教"]

    @staticmethod
    def is_triggered(message):
        """檢查訊息是否以任何支援的關鍵字開頭"""
        return any(message.strip().startswith(keyword) for keyword in TriggerFilter.TRIGGER_KEYWORDS)

    @staticmethod
    def get_trigger_type(message):
        """取得觸發的關鍵字類型"""
        for keyword in TriggerFilter.TRIGGER_KEYWORDS:
            if message.strip().startswith(keyword):
                return keyword
        return None

    @staticmethod
    def extract_content(message):
        """提取關鍵字之後的內容"""
        trigger_type = TriggerFilter.get_trigger_type(message)
        if trigger_type:
            content = message[len(trigger_type):].strip()
            return content
        return None


# 初始化 Perplexity 搜尋模組
search_module = PerplexitySearchModule(PERPLEXITY_API_KEY)

# 搜尋決策提示模板
SEARCH_DECISION_TEMPLATE = """
你是一個AI助手，需要判斷用戶的問題是否需要進行網路搜尋。

分析以下對話歷史和用戶訊息，決定是否需要搜尋網路來提供準確答案。

回覆格式：必須是有效的JSON格式，格式如下：
{{"search": "Y", "keyword": "搜尋關鍵字"}}

或者

{{"search": "N", "keyword": ""}}

規則：
- 如果問題涉及最新資訊、事實查詢、時事新聞、統計數據、或需要外部知識，設定 search: "Y"
- 如果是個人意見、一般閒聊、情感問題、或已有足夠資訊，設定 search: "N"
- keyword 應為簡潔的搜尋關鍵字，不要超過10個字
- 必須嚴格按照JSON格式回覆，不要添加任何額外文字

對話歷史:
{history}

使用者訊息: {message}

請只回覆JSON，不要有任何其他內容。
"""



# 建立 Flask 應用程式
def create_app():
    """建立 Flask 應用程式"""
    app = Flask(__name__)

    @app.route('/')
    def index():
        return f'Welcome to LINE AI Search Bot v{__version__}!'

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

        # 檢查訊息是否以支援的關鍵字開頭
        if not TriggerFilter.is_triggered(user_message):
            logger.info("訊息未觸發支援的關鍵字，忽略")
            return

        # 取得觸發類型和內容
        trigger_type = TriggerFilter.get_trigger_type(user_message)
        triggered_content = TriggerFilter.extract_content(user_message)

        if not triggered_content:
            logger.info("觸發關鍵字後沒有內容，忽略")
            return

        try:
            

            if trigger_type == "@助教":
                # AI 對話模式
                logger.info(f"AI 對話模式: {triggered_content}")

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

                    # 嘗試解析 JSON 回應
                    response_text = search_response.text.strip()
                    logger.info(f"Gemini 回應: {response_text}")

                    # 嘗試直接解析 JSON
                    try:
                        search_decision = json.loads(response_text)
                    except json.JSONDecodeError:
                        # 如果直接解析失敗，嘗試從文字中提取 JSON
                        import re
                        json_match = re.search(r'\{.*\}', response_text)
                        if json_match:
                            try:
                                search_decision = json.loads(json_match.group())
                            except json.JSONDecodeError:
                                logger.warning(f"無法解析 Gemini JSON 回應: {response_text}")
                                search_decision = {"search": "N", "keyword": ""}
                        else:
                            logger.warning(f"Gemini 回應中沒有找到 JSON: {response_text}")
                            search_decision = {"search": "N", "keyword": ""}

                    # 驗證 JSON 結構
                    if not isinstance(search_decision, dict) or "search" not in search_decision:
                        logger.warning(f"無效的搜尋決策格式: {search_decision}")
                        search_decision = {"search": "N", "keyword": ""}

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
                system_prompt = """
                                你是一個有幫助的 LINE 聊天機器人助手。請用繁體中文回覆。每次交談盡量簡短。
                                並在重要的資訊的部分：截斷。目的是增加緊急程度。
                                並加上請說{繼續}。如果使用者說：繼讀。你就說：繼續要加錢!
                                這樣做的目的是讓使用者覺得好笑，因為這個部分讓人類覺得好笑。

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

            logger.info(f"已回覆 {user_id}: {trigger_type}")
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
