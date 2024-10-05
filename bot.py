import requests
import telebot
from app.setting import TELEBOT_BOT_TOKEN
from app.agent import agent_with_chat_history
token_tg = TELEBOT_BOT_TOKEN
url = "https://web.telegram.org/k/#@MC_VN_bot"
bot = telebot.TeleBot(token_tg)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, my name is MC_VN_bot. Can I help u?")

@bot.message_handler(func=lambda message: True)
def get_answer(message):
    user_input = message.text
    # Tạo embedding cho input của người dùng
    print(user_input)
    res = agent_with_chat_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "<foo>"}}, )
    # Gửi phản hồi về người dùng
    if res not in ["ok", "error"]:
        bot.reply_to(message, res['output'])
    else:
        bot.reply_to("Sorry, I didn't understand")

@bot.message_handler(commands=['end'])
def end_message(message):
    bot.reply_to(message, "Thanks you. Have u a good day.")


bot.infinity_polling()