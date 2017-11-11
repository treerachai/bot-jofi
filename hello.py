from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_access_token = 'xz/JtdLRqBocv4PpYboi0a0RnXv3vpurJW9ElUuaHPpT8DFAflJK1Fpwc4cy0Unl94BXTdCmVaWYB9g8v8G8hNeci/Kr45J3a9m7kHsbeXYGbmiDQltRp5dsLJj7aNr34uhp/iWf+B+fI4SUvFcd+AdB04t89/1O/w1cDnyilFU='
channel_secret = 'd0aa00b32ee8cb491e52dd801b86e041'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='hello,'+event.message.text))

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Msg'))
    pass


if __name__ == "__main__":
    app.run()
