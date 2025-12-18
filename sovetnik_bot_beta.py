import logging
import smtplib
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки
TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
EMAIL_TO = "ваша_почта@example.com"
EMAIL_FROM = "отправитель@example.com"
EMAIL_PASSWORD = "пароль_приложения"  # для Gmail используйте пароль приложения

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция отправки email
def send_email(user_data):
    subject = f"Новая заявка от {user_data['username']}"
    body = f"""
    Новая заявка:
    Имя: {user_data.get('name', 'Не указано')}
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

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Оставить заявку", callback_data='create_request')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы оставить заявку.",
        reply_markup=reply_markup
    )

# Обработка нажатия кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'create_request':
        user = query.from_user
        user_data = {
            'user_id': user.id,
            'username': user.username or user.first_name,
            'name': user.full_name,
            'time': query.message.date.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Отправка email
        if send_email(user_data):
            await query.edit_message_text(
                f"✅ Заявка успешно отправлена!\n"
                f"Ваши данные:\n"
                f"Имя: {user.full_name}\n"
                f"Username: @{user.username}\n"
                f"Время: {user_data['time']}"
            )
        else:
            await query.edit_message_text("❌ Ошибка при отправке заявки. Попробуйте позже.")

# Основная функция
def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()