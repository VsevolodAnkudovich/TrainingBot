import os
import telebot
import time
from dotenv import load_dotenv

# Загружаем секреты
load_dotenv()
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))

bot = telebot.TeleBot(TOKEN)

# Загрузка тренировок
def load_workouts():
    workouts = {}
    current_program = ""
    with open('workouts.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_program = line[1:-1]
                workouts[current_program] = []
            elif current_program and line:
                workouts[current_program].append(line)
    return workouts

workouts = load_workouts()

# Проверка подписки
def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

# Старт бота
@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for program in workouts.keys():
            keyboard.add(program)
        bot.send_message(message.chat.id, "🏋️ Выберите программу тренировок:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "⛔ Для доступа подпишитесь на канал: [Путь Ханмы](https://t.me/hannasfollower)", parse_mode="Markdown")

# Отправка программы
@bot.message_handler(func=lambda message: message.text in workouts.keys())
def send_program(message):
    if not check_sub(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Требуется подписка на канал!")
        return
        
    program = message.text
    response = "\n".join(workouts[program])
    bot.send_message(message.chat.id, f"<b>{program}</b>\n{response}", parse_mode="HTML")

# Блокируем другие сообщения
@bot.message_handler(func=lambda message: True)
def block_other(message):
    bot.send_message(message.chat.id, "Используйте кнопки меню ⬇️")

# Автоперезапуск при ошибках
print("⚔️ Бот 'Путь Ханмы' запущен!")
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Перезапуск через 60 секунд...")
        time.sleep(60)
