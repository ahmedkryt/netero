from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


# для отправки сообщений с картинкой
def send_photo_with_caption(update, context, caption, markup=None):
    photo_path = 'Image.jpg'
    chat_id = update.effective_chat.id
    if markup:
        context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'), caption=caption, reply_markup=markup)
    else:
        context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'), caption=caption)


# Первая сессия
def start(update, context):
    global grade
    grade = 11
    keyboard = [
        [
            InlineKeyboardButton('Учусь в 10 классе', callback_data="Учусь в 10 классе"),
            InlineKeyboardButton('Учусь в 11 классе', callback_data="Учусь в 11 классе"),
        ],
        [InlineKeyboardButton('У меня gap year', callback_data="У меня gap year"),
        InlineKeyboardButton('На разведке', callback_data="На разведке")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    name = update.message.chat.first_name
    caption = '''Здравствуй, {name}!

Мы — Ив и Ник — поможем тебе подготовиться к ЕГЭ по биологии. 
Для этого у нас есть:

🪼 конспекты по всем темам кодификатора
🪼 тренажёр для отработки заданий из банка ФИПИ

Расскажешь о себе?'''.format(name=name)
    global flag
    flag = False
    send_photo_with_caption(update, context, caption, markup)
    if flag:
        menu(update, context)


# обработчик кнопок
def button(update, context):
    global grade
    global flag
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == 'Учусь в 10 классе':
        update.effective_chat.send_message("Отлично! Будет больше времени, чтобы вникнуть в детали и разобраться со сложными случаями.")
        grade = 10
    if variant == 'Учусь в 11 классе':
        update.effective_chat.send_message('Самое время начать подготовку!')
        grade = 11
    if variant == 'У меня gap year':
        update.effective_chat.send_message('Уже знаком с форматом ЕГЭ, да? Тогда вперёд ботать, сотка сама себя не получит.')
        grade = 12
    if variant == 'На разведке':
        update.effective_chat.send_message('Исследуй, странник. Может, наткнёшься на что-нибудь интересное...')
    menu(update, context)


# основное окно
def menu(update, context):
    caption = 'Чем хочешь заняться?'
    keyboard = [
        [InlineKeyboardButton('Разобраться с теорией', callback_data="Разобраться с теорией")],
         [InlineKeyboardButton('Попрактиковаться', callback_data="Попрактиковаться")],
         [InlineKeyboardButton('Настроить получение напоминаний', callback_data="Настроить получение напоминаний")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_photo_with_caption(update, context, caption, markup)


# основная
def main():
    updater = Updater("7944892380:AAGKYP--CEiTaNtj4JAAlBWrw1MpX0sqOKs", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
