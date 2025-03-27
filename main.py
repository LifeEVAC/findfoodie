# app/main.py

from flask import Flask, request
import os

app = Flask(__name__)

# Try to import LINE Bot API (optional until credentials are ready)
try:
    from linebot import LineBotApi, WebhookParser
    from linebot.models import TextMessage, MessageEvent

    CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
    CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

    if CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        parser = WebhookParser(CHANNEL_SECRET)
    else:
        line_bot_api = None
        parser = None

except Exception as e:
    print("LINE SDK not fully initialized:", e)
    line_bot_api = None
    parser = None

@app.route("/webhook", methods=["POST"])
def webhook():
    if not parser or not line_bot_api:
        return "LINE Bot not initialized (no credentials)", 200

    body = request.get_data(as_text=True)
    signature = request.headers.get("X-Line-Signature")

    try:
        events = parser.parse(body, signature)
    except Exception as e:
        return str(e), 400

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            reply = f"You said: {event.message.text}"
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text=reply)
            )

    return "OK", 200

