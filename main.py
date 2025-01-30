from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler
from threading import Thread
import telegram
import datetime
import schedule
import logging
import time

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
    keyboard = [
        [InlineKeyboardButton('Назад в меню', callback_data="В меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    if notice:
        send_messages(update, context, '''Напиши, когда прислать уведомление, в такой форме: __:__
Например, 09:00''')
    else:
        send_messages(update, context, 'Что ж, твой выбор.', markup)
        schedule.clear()


# сообщение для отправки напоминания
def send_reminder(context, chat_id: int):
    keyboard = [
        [InlineKeyboardButton('В меню', callback_data="В меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    context.bot.send_message(chat_id, text='Привет, пора позаниматься', reply_markup=markup)


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
    keyboard = [
        [InlineKeyboardButton('Назад в меню', callback_data="В меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    # время, которое ввел пользователь
    user_response = update.message.text
    # проверяем на валидность и отправляем на установку
    try:
        if datetime.datetime.strptime(user_response, '%H:%M').time():
            # если время записано без предшествующего нуля, корректируем данные
            if len(user_response.split(':')[0]) == 1:
                user_response = '0' + user_response
            if len(user_response.split(':')[1]) == 1:
                user_response = user_response[:-1] + '0' + user_response[-1]
            # устанавливаем
            set_reminder(update, context, user_response)
            # отвечаем пользователю
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Будем напоминать каждый день в {user_response} — точно не забудешь!', reply_markup=markup)
    except(IndexError, ValueError):
        update.message.reply_text(f'Не понимаю, попробуй еще раз', reply_markup=markup)


# диалог Напоминания
def reminder(update, context):
    keyboard = [
        [InlineKeyboardButton('Настроить время уведомлений', callback_data="Время уведомлений")],
        [InlineKeyboardButton('Отказаться от уведомлений', callback_data="Отказаться от уведомлений")],
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, 'Настроить уведомления', markup)


# Диалог Практика
def practice(update, context):
    keyboard = [
        [InlineKeyboardButton('Биология как наука', callback_data="Биология как наука практика")],
        [InlineKeyboardButton('Молекулярная и клеточная биология', callback_data="Молекулярная биология практика")],
        [InlineKeyboardButton('Генетика', callback_data="Генетика практика")],
        [InlineKeyboardButton('Биотехнология', callback_data="Биотехнология практика")],
        [InlineKeyboardButton('Селекция', callback_data="Селекция практика")],
        # [InlineKeyboardButton('Организм как биосистема', callback_data="Организм как биосистема практика")],
        # [InlineKeyboardButton('Многообразие органического мира', callback_data="Многообразие органического мира практика")],
        # [InlineKeyboardButton('Анатомия и физиология человека', callback_data="Анатомия и физиология человека практика")],
        # [InlineKeyboardButton('Эволюция', callback_data="Эволюция практика")],
        # [InlineKeyboardButton('Экология', callback_data="Экология практика")],
        [InlineKeyboardButton('В меню', callback_data="В меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, 'Выбери раздел', markup)

# Раздел Биология как наука Практика
def biology_as_science_prac(update, context):
    pass


# Раздел молекулярная и клеточная биология Практика
def molecular_and_cellular_biology_main_prac(update, context):
    keyboard = [
        [InlineKeyboardButton('История и методы цитологии. Клеточная теория', callback_data="История цитологии практика")],
        [InlineKeyboardButton('Биохимия', callback_data="Биохимия практика")],
        [InlineKeyboardButton('Строение клетки', callback_data="Строение клетки практика")],
        [InlineKeyboardButton('Метаболизм', callback_data="Метаболизм практика")],
        [InlineKeyboardButton('Матричные реакции', callback_data="Матричные реакции практика")],
        [InlineKeyboardButton('Клеточный цикл', callback_data="Клеточный цикл практика")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, text='Выбери тему', markup=markup)


# Раздел Генетика Практика
def genetics_prac(update, context):
    pass


# Раздел Биотехнология Практика
def biotechnology_prac(update, context):
    pass


# Раздел Селекция Практика
def breeding_prac(update, context):
    pass


# Тема История и методы цитологии Раздела Молекулярная и клеточная биология Практика
def history_and_methods_citology_prac(update, context):
    pass


# Тема Биохимия Раздела Молекулярная и клеточная биология Практика
def biochemistry_prac(update, context):
    pass


# Тема Строение клетки Раздела Молекулярная и клеточная биология Практика
def cell_structure_prac(update, context):
    pass


# Тема Метаболизм Раздела Молекулярная и клеточная биология Практика
def metabolism_prac(update, context):
    pass


# Тема Матричные реакции Раздела Молекулярная и клеточная биология Практика
def matrix_reactions_prac(update, context):
    pass


# Тема Клеточный цикл Раздела Молекулярная и клеточная биология Практика
def cell_cycle_prac(update, context):
    pass


# диалог Теория
def conspect(update, context):
    keyboard = [
        [InlineKeyboardButton('Биология как наука', callback_data="Биология как наука теория")],
        [InlineKeyboardButton('Молекулярная и клеточная биология', callback_data="Молекулярная биология теория")],
        [InlineKeyboardButton('Генетика', callback_data="Генетика теория")],
        [InlineKeyboardButton('Биотехнология', callback_data="Биотехнология теория")],
        [InlineKeyboardButton('Селекция', callback_data="Селекция теория")],
        # [InlineKeyboardButton('Организм как биосистема', callback_data="Организм как биосистема теория")],
        # [InlineKeyboardButton('Многообразие органического мира', callback_data="Многообразие органического мира теория")],
        # [InlineKeyboardButton('Анатомия и физиология человека', callback_data="Анатомия и физиология человека теория")],
        # [InlineKeyboardButton('Эволюция', callback_data="Эволюция теория")],
        # [InlineKeyboardButton('Экология', callback_data="Экология теория")],
        [InlineKeyboardButton('В меню', callback_data="В меню")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, 'Выбери раздел', markup)


# Раздел Биология как наука Теория
def biology_as_science_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1V8CRBD_NWHVGB5RVxbSXKdhwsmAe_irgcWOD-T3M7_Q/edit?usp=drive_link'>📑 Свойства и уровни организации биосистем. Разделы и методы биологии</a>

<a href='https://docs.google.com/document/d/17gU7Co2qcBKVhptiXlLvfKTOoh_zsnWFx-De6lYIdiQ/edit?usp=drive_link'>📑 Исследование</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview = True)


# Раздел молекулярная и клеточная биология Теория
def molecular_and_cellular_biology_main_con(update, context):
    keyboard = [
        [InlineKeyboardButton('История и методы цитологии. Клеточная теория', callback_data="История цитологии теория")],
        [InlineKeyboardButton('Биохимия', callback_data="Биохимия теория")],
        [InlineKeyboardButton('Строение клетки', callback_data="Строение клетки теория")],
        [InlineKeyboardButton('Метаболизм', callback_data="Метаболизм теория")],
        [InlineKeyboardButton('Матричные реакции', callback_data="Матричные реакции теория")],
        [InlineKeyboardButton('Клеточный цикл', callback_data="Клеточный цикл теория")]
    ]
    markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=False)
    send_messages(update, context, text='Выбери тему', markup=markup)


# Раздел Генетика Теория
def genetics_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/15lipZln844hOfzfO5ZQfXJwZ_E1cjO3ciOAKEukInj0/edit?usp=sharing'>📑 Основные генетические понятия и символы. Методы генетики</a>

<a href='https://docs.google.com/document/d/1I6EyUTvBh4OW5s_Kfw4Cflx8gQmi9J_-DgDInYyf9vo/edit?usp=sharing'>📑 Генетика Менделя</a>

<a href = 'https://docs.google.com/document/d/1C4Wk499yuDfAhM4welcv_TCRn_-Q255GwP7CRCnnCQw/edit?usp=sharing'>📑 Генетика Моргана. Хромосомная теория наследственности</a>

<a href = 'https://docs.google.com/document/d/19FIgIge7H-xlA1a8S-98keyqapXTaNXin-B0MZgdCK0/edit?usp=sharing'>📑 Изменчивость. Генетические болезни</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Раздел Биотехнология Теория
def biotechnology_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1ipgZOoMw1KO1PKInvnStYFLgU7xI2F5ASkWpXyx1Tdo/edit?usp=sharing'>📑 Биотехнология</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Раздел Селекция Теория
def breeding_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/16cYkwZXNVub2ylcaCYR5E1m4F8Pdx8BAQ7YR7-1KTlA/edit?usp=drive_link'>📑 Селекция</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема История и методы цитологии Раздела Молекулярная и клеточная биология Теория
def history_and_methods_citology_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1kA8Ue_5iLpen2GmOEIAfJByZfJxufh6R_xhY5Wavk10/edit?usp=sharing'>📑 История и методы цитологии. Клеточная теория</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема Биохимия Раздела Молекулярная и клеточная биология Теория
def biochemistry_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1v1nQ7noVqfkrt0gAp0QU8-9aafwNaK4zZbj2Y2OW5a4/edit?usp=sharing'>📑 Химический состав клетки. Вода. Минеральные вещества</a>

<a href='https://docs.google.com/document/d/1AuySgB2dddxSIPCRsaFn2S014y8v1jSBP1KJJ_iAvsA/edit?usp=sharing'>📑 Липиды</a>

<a href = 'https://docs.google.com/document/d/143tRQQUbF-QWQdfDAvV3ny2GL6JLM3yD6fQaaR3b3Ks/edit?usp=sharing'>📑 Углеводы</a>

<a href = 'https://docs.google.com/document/d/16WXZRksgYRACQrLb70Ok_4wXdOtfqlaKWXGAWnMqJUk/edit?usp=sharing'>📑 Нуклеиновые кислоты. АТФ</a>

<a href = 'https://docs.google.com/document/d/1CMBsKh9_PdMzpeK5WvObAXNKlDtqqh3mYM6_nQA6ul0/edit?usp=sharing'>📑 Белки. Ферменты</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема Строение клетки Раздела Молекулярная и клеточная биология Теория
def cell_structure_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1NGdosXt8mkpFgRpK7Bf0Ry5XVdGeHiH1-6WWTBSgh_I/edit?usp=sharing'>📑 Прокариоты и эукариоты</a>

<a href='https://docs.google.com/document/d/1nON2sdHiu0wL7JLZtvbXkRmwb53eqMAavBYgAK3YjoI/edit?usp=sharing'>📑 Строение прокариотической клетки. Бактерии и археи</a>

<a href = 'https://docs.google.com/document/d/15x990_dywHVmcpIQncvdmKLLCV8saOZFSNHLBZGOUeA/edit?usp=sharing'>📑 Строение эукариотической клетки</a>'''

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема Метаболизм Раздела Молекулярная и клеточная биология Теория
def metabolism_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1JHqaKDWGyHykpTrSjzcrBHqUV4ClDk031kj0CLTvtqU/edit?usp=sharing'>📑 Метаболизм</a>

<a href='https://docs.google.com/document/d/14wt_qHqAuedkzwGs2znmR43QKeUKQIVH7aNPyLhG1-M/edit?usp=sharing'>📑 Анаболизм: хемосинтез и фотосинтез</a>

<a href='https://docs.google.com/document/d/1bZeJRZv4es3vVe7DQuVOJUY2FcAuxVLz7Ob1ruNXIdg/edit?usp=sharing'>📑 Катаболизм: брожение и клеточное дыхание</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема Матричные реакции Раздела Молекулярная и клеточная биология Теория
def matrix_reactions_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/1_O0of-Q1Ngw-BuosM-SVtHt09Cp7EyzMhyeWA07dOTc/edit?usp=sharing'>📑 Репликация ДНК</a>

<a href='https://docs.google.com/document/d/19ki2hZ7bfwCil6pzt58jxPuSPQKzqKxj1EtZ-GKNOvw/edit?usp=sharing'>📑 Транскрипция и трансляция</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# Тема Клеточный цикл Раздела Молекулярная и клеточная биология Теория
def cell_cycle_con(update, context):
    text = '''<a href='https://docs.google.com/document/d/18DfCOdE0V7TmNSV3pYbMLxmkFgQknoLauC6du38_5HM/edit?usp=sharing'>📑 Клеточный цикл</a>'''
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML,
                             disable_web_page_preview=True)


# обработчик кнопок
def button(update, context):
    query = update.callback_query
    variant = query.data
    query.answer()

    if variant == 'Учусь в 10 классе':
        update.effective_chat.send_message("Хвалю за решение начать готовиться уже сейчас!")
        grade = 10
        time.sleep(2)
        menu(update, context)
    if variant == 'Учусь в 11 классе':
        update.effective_chat.send_message('Самое время начать подготовку!')
        grade = 11
        time.sleep(2)
        menu(update, context)
    if variant == 'У меня gap year':
        update.effective_chat.send_message('Уже знаком с форматом ЕГЭ, да? Тогда вперёд ботать, сотка сама себя не получит.')
        grade = 12
        time.sleep(2)
        menu(update, context)
    if variant == 'На разведке':
        update.effective_chat.send_message('Исследуй, странник. Может, наткнёшься на что-нибудь интересное...')
        time.sleep(2)
        menu(update, context)

    if variant == 'Разобраться с теорией':
        conspect(update, context)
    if variant == 'Попрактиковаться':
        practice(update, context)
    if variant == 'Настроить уведомления':
        reminder(update, context)

    if variant == 'В меню':
        menu(update, context)

    if variant == 'Время уведомлений':
        timer(update, context, True)
    if variant == 'Отказаться от уведомлений':
        timer(update, context, False)
    # теория
    if variant == 'Биология как наука теория':
        biology_as_science_con(update, context)
    if variant == 'Молекулярная биология теория':
        molecular_and_cellular_biology_main_con(update, context)
    if variant == 'История цитологии теория':
        history_and_methods_citology_con(update, context)
    if variant == 'Биохимия теория':
        biochemistry_con(update, context)
    if variant == 'Строение клетки теория':
        cell_structure_con(update, context)
    if variant == 'Метаболизм теория':
        metabolism_con(update, context)
    if variant == 'Матричные реакции теория':
        matrix_reactions_con(update, context)
    if variant == 'Клеточный цикл теория':
        cell_cycle_con(update, context)
    if variant == 'Генетика теория':
        genetics_con(update, context)
    if variant == 'Биотехнология теория':
        biotechnology_con(update, context)
    if variant == 'Селекция теория':
        breeding_con(update, context)
    # практика
    if variant == 'Биология как наука практика':
        biology_as_science_prac(update, context)
    if variant == 'Молекулярная биология практика':
        molecular_and_cellular_biology_main_prac(update, context)
    if variant == 'История цитологии практика':
        history_and_methods_citology_prac(update, context)
    if variant == 'Биохимия практика':
        biochemistry_prac(update, context)
    if variant == 'Строение клетки практика':
        cell_structure_prac(update, context)
    if variant == 'Метаболизм практика':
        metabolism_prac(update, context)
    if variant == 'Матричные реакции практика':
        matrix_reactions_prac(update, context)
    if variant == 'Клеточный цикл практика':
        cell_cycle_prac(update, context)
    if variant == 'Генетика практика':
        genetics_prac(update, context)
    if variant == 'Биотехнология практика':
        biotechnology_prac(update, context)
    if variant == 'Селекция практика':
        breeding_prac(update, context)


# основное окно
def menu(update, context):
    caption = 'Чем хочешь заняться?'
    keyboard = [
        [InlineKeyboardButton('Разобраться с теорией', callback_data="Разобраться с теорией")],
         [InlineKeyboardButton('Попрактиковаться', callback_data="Попрактиковаться")],
         [InlineKeyboardButton('Настроить уведомления', callback_data="Настроить уведомления")]
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
