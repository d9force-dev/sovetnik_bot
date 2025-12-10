import logging
import smtplib
from email.mime.text import MIMEText
from telegram import Updatem InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

#Настройки
TOKEN = 8591104317:AAFR1kDtLHp4CySEn1gm_Mz0RHhcgqdrO1o
EMAIL_TO = sanya.martynenko.99@gmail.com
EMAIL_FROM = mav@telecombg.ru
EMAIL_PASSWORD = c3P-WkM-uQS-C6Z

#Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#Функции отправки email
def send_email(user_data):
    subject = f"Новая заявка от {user_data['username']}"
    body = f"""
    Новая заявка:
    Имя: {user_data.get('name', 'не указано')}
    Username: @{user_data['username']}
    ID: {user_data['user_id']}
    Время: {user_data['time']}
    """


    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO


    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки email: {e}")
        return False
    

#Команда /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Оставить заявку", callback_data='create_reauest')]
    ]