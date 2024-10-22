import logging

from select import select

from api  import  gpt, image
from  enum import  Enum
import requests
from config import API_KEY
import shelve
from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from config import BOT_KEY

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class ModelEnum(Enum):
    gpt_text = 1
    gpt_image =2

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    user_name = user.full_name
    pandora = shelve.open("pandora")
    if str(user_id) not in pandora.keys():
        user_data = {
            "user_name": user_name,
            "subs": "Free",
            "tokens": 0,
            "model": ModelEnum.gpt_text.value
        }
        pandora[str(user_id)] = user_data
    await update.message.reply_html (f" Привет {pandora[str(user_id)]['user_name']}!")
    pandora.close()

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    pandora = shelve.open("pandora")
    subscription_type = pandora[str(user_id)]["subs"]
    tokens = pandora[str(user_id)]["tokens"]
    profile_text = (
        f"Это ваш профиль. \n"
        f"ID: {user_id}\n"
        f"Подписка: {subscription_type}\n\n"
        f"Лимиты: {tokens} token"
    )
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     help_text = (
        "Чтобы начать, пиши /start \n"
        "Чтобы пополнить токены /store \n"
    )
    await update.message.reply_text(help_text)


async def process_message (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    pandora = shelve.open("pandora")
    user_id = str(user.id)
    tokens =pandora[str(user_id)]['tokens']
    gpt_model = pandora[user_id]["model"]
    if tokens > 0:
     if gpt_model == ModelEnum.gpt_text.value:
      message = update.message.text
      answer = gpt(message)
      await update.message.reply_text(answer)
     if gpt_model == ModelEnum.gpt_image.value:
         message = update.message.text
         answer = image(message)
         await update.message.reply_photo(
             photo=answer[0],
             caption=answer[1]

         )
    else:
     mess = "Пополните баланс в store"
     await update.message.reply_text(mess)
    pandora.close()
async def store(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    await update.message.reply_text("Добро пожаловать в магазин! Сколько токенов хочешь купить?")
    pandora = shelve.open('pandora')
    pandora[user_id]['tokens'] = 20
    pandora[user_id]['subs'] = 'VIP'
async def mode(update: Update, context: CallbackContext) -> None:
    keyboard = [
      [InlineKeyboardButton("GPT 3.5", callback_data="1")],
      [InlineKeyboardButton("Stable Diffusion", callback_data="2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await  update.message.reply_text("Тут вы можете сменить модель нейросетей",reply_markup = reply_markup)

async  def button(update: Update, context: CallbackContext):
    pandora = shelve.open("pandora")
    query = update.callback_query
    mode_gpt = query.data
    user_model =pandora[user_id_chat]
    user_model["model"] = int(mode_gpt)
    pandora[user_id_chat] = user_model

    pandora.close()

    new_keyboard = [
        [InlineKeyboardButton("GPT 3.5", callback_data="1")],
        [InlineKeyboardButton("Stable Diffusion", callback_data="2")]
    ]

    for row in new_keyboard:
        for button in row:
            if button.callback_data == mode_gpt:
                new_button =InlineKeyboardButton(f"✅{button.text}",callback_data = button.callback_data)
                row[row.index(button)] = new_button
    reply_markup =InlineKeyboardMarkup(new_keyboard)
    await query.edit_message_text(
        text ="Тут вы можете сменить модель нейросетей",
        reply_markup = reply_markup
    )
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7014697331:AAGu24mW78fWbSofq4kZo9-8VgfqhbwSmm4").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("store", store))
    application.add_handler(CommandHandler("mode", mode))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()