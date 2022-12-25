import logging
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    # InlineQueryHandler,
    PicklePersistence,
)
import requests
from json import JSONDecodeError
from models import Users
from datetime import datetime
from urllib.parse import urlparse

# @GoodsHunter_bot
TOKEN = '5625435958:AAHA-SUrnignJJHwlG7rwj8dHb0k7UBMnnw'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
(MAIN,) = range(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = await get_user(update, context)
    print('user', user.to_json())
    text = (
        '🦾 <b>Привет! Я - супер робот для WILDBERRIES</b>\n\n'
        'Сканирую этот маркетплейс каждый день и анализирую все данные.\n'
        'Если хочешь получить мои данные, то вот ссылка - http://wb.nio.design'
    )
    await update.message.reply_text(text, parse_mode='html')
    return MAIN


async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_chat.id
    user = Users.objects.filter(telegram_id=telegram_user_id).first()
    if user is None:
        user = Users(
            telegram_id=telegram_user_id,
            last_name=update.effective_chat.last_name,
            first_name=update.effective_chat.first_name,
            username=update.effective_chat.username,
            created_at=datetime.utcnow(),
        )
    user.save()
    return user


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    return await start(update, context)


def main() -> None:
    """Run the bot."""
    my_persistence = PicklePersistence(filepath='bot.pkl')
    application = Application.builder().token(TOKEN).persistence(
        persistence=my_persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN: [
                CommandHandler('cancel', cancel),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        persistent=True,
        name='bot'
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
