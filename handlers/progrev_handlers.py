
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import FIRST_MASSAGE, GET_NAME, GET_NUMBER, GET_MAIL, GET_AGREE, GET_INFO, GET_INLINE_BUTTON



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update -  это полная информация о том что произошло в чате(сообщении)
    # update.effective_user - это информация о пользователе, который отправил сообщение
    # update.effective_chat - это информация о чате в котром произошло событие(информация о диологе:диалг напр с ботом,
    #  группой и т)
    # update.effective_message - это информация о сообщении , которое отправил пользователь
    # context - это контекст, в котором происходит событие(побочные действия котрые наш бот будет уметь делать(в контексте
    # будем данные между разными функциями передавать, будем что-то запоминать, будем вызывать отложенные действия,
    # вспомогательные действия которые он будет делать))

    keyboard = [["Да", "Нет"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}! Пройди опрос и  получи в подарок пробное занятие! Хочешь консультацию о тренировках в клубе  IFIT?",
        reply_markup=markup,
    )

    return FIRST_MASSAGE


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if answer == "Да":
        keyboard = [[update.effective_user.first_name]]
        markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Чтобы получить консультацию, напиши свое имя.",
            reply_markup=markup,
        )
        return GET_NAME
    elif answer == "Нет":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Очень жаль, может быть в другой  раз...",
            reply_markup=ReplyKeyboardRemove(),
        )
        return GET_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    context.user_data["name"] = name
    print(name)
    keyboard = [[KeyboardButton("Поделиться моим контактом", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Напишите свой номер телефона в формате (375)-код оператора(3 цифры) номер (7 цифр).",
        reply_markup=markup,
    )
    return GET_NUMBER


async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.effective_message.contact.phone_number
    context.user_data["number"] = number
    print(number)
    if number[:4] != "+375" or number[:4] != "3750" or number[:4] != "3750":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Напишите свой e-mail."
        )
        return GET_MAIL


async def get_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mail = update.effective_message.text
    context.user_data["mail"] = mail
    print(mail)
    keyboard = [["Да", "Нет"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы согласны на обработку персональных данных? Мы не передаем ваши данные третьим лицам.",
        reply_markup=markup,
    )
    return GET_AGREE


async def get_agree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if answer == "Да":
        keyboard = [["FIT"]]
        markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ваш промокод на пробное бесплатное занятие 'MI FIRST IFIT'. Добро пожаловать в клуб! Жми FIT и получай гайд по тренировкам",
            reply_markup=markup,
        )
        return GET_INFO
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Тогда все!("
        )
        return GET_INFO
    print(context.user_data)
         

