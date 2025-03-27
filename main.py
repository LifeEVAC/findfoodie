# app/main.py
from flask import Flask, request
from linebot import LineBotApi, WebhookParser
from linebot.models import TextMessage, MessageEvent
import os
import json

# Initialize Flask
app = Flask(__name__)

# Read credentials from environment
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

@app.route("/webhook", methods=["POST"])
def webhook():
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
