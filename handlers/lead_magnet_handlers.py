from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import GET_INLINE_BUTTON


async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Петли TRX", callback_data="Петли")],
        [InlineKeyboardButton("Пилатес", callback_data="Пилатес")],
        [InlineKeyboardButton("Soft fitness", callback_data="Soft fitness")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="получай гайд",
        reply_markup=markup,
    )
    return GET_INLINE_BUTTON


async def get_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "Петли":
        # /-начиная от корня ./ - текущая папка ../ - на папку назад
        photo = open("./static/foto1.jpg", "rb")
        await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo, caption="это фотка"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="получай гайд",
        )
        photo.close()
