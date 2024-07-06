from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ButtonsTemplate)
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

    if event.message.text == "確認樣板":
        confirm_template = TemplateSendMessage(

            alt_text = "comfirm template",

            actions = [

                MessageAction(
                    label = 'yes',
                    text = 'yes'
                ),
                MessageAction(
                    label = 'no',
                    text = 'no'
                )

                ]

        )

        line_bot_api.reply_message(event.reply_token, confirm_template)

    if event.message.text == 'button':
        button_template = TemplateSendMessage(

            alt_text="buttons template",

            template = ButtonsTemplate(

                thumbnail_image_url = "",

                title = "Brown Cafe",
                text = "Enjoy",

                actions=[

                    MessageAction(

                        label="咖啡有神麼好處",
                        text="讓人有精神"
                    ),
                    URIAction(
                        label = "伯朗咖啡",
                        url="https://google.com"

                    )

                ]

            )

        )
        line_bot_api.reply_message(event.reply_token, button_template)


    if event.message.text == 'carousel':
        carousel_template = TemplateSendMessage(

            alt_text="carousel template",

            template= CarouselTemplate(

                columns = [

                    #第一個
                    CarouselColumn(

                        thumbnail_image_url = "",

                        title = "Brown Cafe",
                        text = "Enjoy",
                        actions = [

                            MessageAction(
                                label="咖啡有神麼好處",
                                text="讓人有精神"
                            ),
                            URIAction(
                                label = "伯朗咖啡",
                                url="https://google.com"

                            )
                        ]

                    ),

                    #第二個
                    CarouselColumn(

                        thumbnail_image_url = "",

                        title = "Brown Cafe",
                        text = "Enjoy",
                        actions = [

                            MessageAction(
                                label="咖啡有神麼好處",
                                text="讓人有精神"
                            ),
                            URIAction(
                                label = "伯朗咖啡",
                                url="https://google.com"

                            )
                        ]

                    )


                ]


            )


        )



if __name__ == "__main__":
    app.run()
