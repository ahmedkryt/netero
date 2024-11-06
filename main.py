from datetime import datetime
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import time
import datetime
import schedule
import logging
from threading import Thread


# включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# для отправки сообщений с картинкой
def send_photo_with_caption(update, context, caption, markup=None):
    photo_path = 'Image.jpg'
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'), caption=caption, reply_markup=markup)


# для отправки сообщений без картинки
def send_messages(update, context, text, markup=None):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


# диалог установка таймера напоминаний
def timer(update, context, notice):
    if notice:
        send_messages(update, context, 'Напиши, когда прислать напоминание в такой форме - 10:00')
    else:
        send_messages(update, context, 'Что ж, твой выбор. Как теперь перестать вспоминать о тебе?')
        schedule.clear()


# сообщение для отправки напоминания
def send_reminder(context, chat_id: int):
    context.bot.send_message(chat_id, text='Привет, пора позаниматься')


# установка таймера
def set_reminder(update, context: CallbackContext, time):
    chat_id = update.effective_chat.id
    # удаляем предыдущую задачу, если она была
    schedule.clear()
    # добавляем новую задачу в планировщик
    schedule.every().day.at(time).do(send_reminder, context=context, chat_id=chat_id)


# цикл для таймера
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# ввод пользователя для таймера
def handle_message(update, context):
    # время, которое ввел пользователь
    user_response = update.message.text
    # проверяем на валидность и отправляем на установку
    try:
        if datetime.datetime.strptime(user_response, '%H:%M').time():
            set_reminder(update, context, user_response)
    except(IndexError, ValueError):
        update.message.reply_text(f'Некорректный вид')


# диалог раздел с теорией
def conspect(update, context):
    keyboard = [
        [InlineKeyboardButton('Биология как наука', callback_data="Биология как наука")],
        [InlineKeyboardButton('Молекулярная и клеточная биология', callback_data="Молекулярная и клеточная биология")],
        [InlineKeyboardButton('Генетика', callback_data="Генетика")],
        [InlineKeyboardButton('Биотехнология', callback_data="Биотехнология")],
        [InlineKeyboardButton('Селекция', callback_data="Селекция")],
        [InlineKeyboardButton('Организм как биосистема', callback_data="Организм как биосистема")],
        [InlineKeyboardButton('Многообразие органического мира', callback_data="Многообразие органического мира")],
        [InlineKeyboardButton('Анатомия и физиология человека', callback_data="Анатомия и физиология человека")],
        [InlineKeyboardButton('Эволюция', callback_data="Эволюция")],
        [InlineKeyboardButton('Экология', callback_data="Экология")],
        [InlineKeyboardButton('Назад в меню', callback_data="Назад в меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, 'Выбери раздел', markup)


# диалог раздел напоминаний
def reminder(update, context):
    keyboard = [
        [InlineKeyboardButton('Настроить время получения напоминаний', callback_data="Время напоминаний")],
        [InlineKeyboardButton('Отказаться от напоминаний', callback_data="Отказаться от напоминаний")],
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, 'Настроить напоминания', markup)


# раздел практики
def practice(update, context):
    pass


# обработчик кнопок
def button(update, context):
    query = update.callback_query
    variant = query.data
    query.answer()
    if variant == 'Учусь в 10 классе':
        update.effective_chat.send_message("Отлично! Будет больше времени, чтобы вникнуть в детали и разобраться со сложными случаями.")
        grade = 10
        time.sleep(3)
        menu(update, context)
    if variant == 'Учусь в 11 классе':
        update.effective_chat.send_message('Самое время начать подготовку!')
        grade = 11
        time.sleep(3)
        menu(update, context)
    if variant == 'У меня gap year':
        update.effective_chat.send_message('Уже знаком с форматом ЕГЭ, да? Тогда вперёд ботать, сотка сама себя не получит.')
        grade = 12
        time.sleep(3)
        menu(update, context)
    if variant == 'На разведке':
        update.effective_chat.send_message('Исследуй, странник. Может, наткнёшься на что-нибудь интересное...')
        time.sleep(3)
        menu(update, context)
    if variant == 'Разобраться с теорией':
        conspect(update, context)
    if variant == 'Попрактиковаться':
        practice(update, context)
    if variant == 'Настроить получение напоминаний':
        reminder(update, context)
    if variant == 'Назад в меню':
        menu(update, context)
    if variant == 'Время напоминаний':
        timer(update, context, True)
    if variant == 'Отказаться от напоминаний':
        timer(update, context, False)


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


# Точка входа
def start(update, context):
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
    send_photo_with_caption(update, context, caption, markup)


# основная
def main():
    updater = Updater("7944892380:AAGKYP--CEiTaNtj4JAAlBWrw1MpX0sqOKs", use_context=True)
    dp = updater.dispatcher
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
