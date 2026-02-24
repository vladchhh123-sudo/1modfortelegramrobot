import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import threading
import time
import signal
import sys

TOKEN = '8792682877:AAHKRz4CJ05KfmdrKfVBcEIS9a2vKzr2swo'
bot = telebot.TeleBot(TOKEN)

CHANNELS = [
    '@+LReJflzWOR00MDU6',
    '@+brkwd5YZY8tiNWVi',
    '@+wm0r3qnxLcA4M2U6',
    '@+nvM6U9acy7g4ZDUy',
    '@+hbceh-QB_HE1MjAy'
]

CHANNEL_LINKS = [
    'https://t.me/+LReJflzWOR00MDU6',
    'https://t.me/+brkwd5YZY8tiNWVi',
    'https://t.me/+wm0r3qnxLcA4M2U6',
    'https://t.me/+nvM6U9acy7g4ZDUy',
    'https://t.me/+hbceh-QB_HE1MjAy'
]

CHANNEL_NAMES = [
    'КАНАЛ #1', 'КАНАЛ #2', 'КАНАЛ #3', 'КАНАЛ #4', 'КАНАЛ #5'
]

pending_users = {}
failed_once = {}
running = True


def signal_handler(sig, frame):
    global running
    print("\n🛑 Остановка...")
    running = False
    bot.stop_polling()
    sys.exit(0)


def get_user_first_name(user):
    if user.first_name:
        return user.first_name
    if user.username:
        return user.username
    return "Друг(а)"


def is_subscribed(user_id):
    for i, channel in enumerate(CHANNELS):
        try:
            time.sleep(0.3)
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                print(f"❌ Не подписан на {CHANNEL_NAMES[i]}")
                return False
        except Exception as e:
            print(f"⚠️ Ошибка проверки {CHANNEL_NAMES[i]}: {e}")
            return None
    print(f"✅ Пользователь {user_id} подписан на все 5 каналов")
    return True


def send_delayed_mod(chat_id, user_id):
    if not running:
        return
    delay = 56 * 3600  # 56 часов
    print(f"⏳ Мод для {user_id} через {delay} секунд...")
    time.sleep(delay)
    if not running or user_id not in pending_users:
        return

    del pending_users[user_id]

    text = (
        f"🕵️‍♂️ Теперь ты точно установил(а) Telegram Mod!\n\n"
        f"🎀 Если не появилась новая функция в твоем аккаунте, скинь бота 15-ти своим друзьям и подожди 30 минут!\n"
        f"p.s. они тоже должны установить себе этот мод!"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📱 Поделиться ULTIMATE модом", callback_data="share"))
    try:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"⚠️ Ошибка отправки мода: {e}")


@bot.message_handler(commands=['start'])
def start(message):
    if not running:
        return

    user_id = message.from_user.id
    failed_once.pop(user_id, None)
    pending_users.pop(user_id, None)

    first_name = get_user_first_name(message.from_user)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔥 ПОЛУЧИТЬ МОД", callback_data="get_ultimate"))

    text = (
        f"🕵️‍♂️ {first_name}, привет!\n\n"
        f"🔥 Это бот для получения Telegram Mod, в котором ты:\n"
        f"👁️ Сможешь читать что пишет собеседник, еще до отправки сообщения\n"
        f"💬 Востанавливать удалённые сообщения и чаты за последние 5 лет\n"
        f"⚡ Видить с кем общается собеседник\n"
        f"📍 Следить по геолокации где находиться собеседник\n"
        f"👤 Просматривать всю активность профилья других пользователей\n\n"
        f"💎 Только 0.1% имеют доступ к этом моду!\n\n"
        f"⚠️ ЕСЛИ ТЫ ХОЧЕШЬ ЗНАТЬ ВСЁ о тех, с кем общаешься жми кнопку ниже!👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if not running:
        return

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    first_name = get_user_first_name(call.from_user)

    bot.answer_callback_query(call.id)

    if call.data == "get_ultimate":
        markup = InlineKeyboardMarkup()
        for name, link in zip(CHANNEL_NAMES, CHANNEL_LINKS):
            markup.row(InlineKeyboardButton(name, url=link))
        markup.add(InlineKeyboardButton("✅ ГОТОВО", callback_data="check_ready"))

        text = (
            f"🚀 {first_name}, ты в одном шаге до получения мода!\n\n"
            f"🔥 Осталось пару секунд до суперсилы!\n\n"
            f"Поддержи наших партнёров — благодаря ним работает мод и мы можем выдавать его бесплатно!\n\n"
            f"📢 Вот ссылки на каналы (кнопки ниже ведут туда же):\n\n"
            f"🔗 КАНАЛ #1: https://t.me/+LReJflzWOR00MDU6\n"
            f"🔗 КАНАЛ #2: https://t.me/+brkwd5YZY8tiNWVi\n"
            f"🔗 КАНАЛ #3: https://t.me/+wm0r3qnxLcA4M2U6\n"
            f"🔗 КАНАЛ #4: https://t.me/+nvM6U9acy7g4ZDUy\n"
            f"🔗 КАНАЛ #5: https://t.me/+hbceh-QB_HE1MjAy\n\n"
            f"⚠️ Если Телеграм выдал ошибку при переходе, подожди 3–5 секунд и попробуй снова.\n\n"
            f"✅ После этого нажми на кнопку «ГОТОВО» ниже 👇"
        )

        bot.edit_message_text(
            text,
            chat_id,
            call.message.message_id,
            reply_markup=markup,
            disable_web_page_preview=True
        )

    elif call.data == "check_ready":
        if failed_once.get(user_id):
            text = (
                f"Отлично, видим твою подписку на каналы.\n\n"
                f"⏳ Ожидай 56 часов — за это время мы разработаем мод специально под твой аккаунт!\n\n"
                f"Такое время ожидания, потому что сейчас очень много запросов."
            )
            bot.edit_message_text(
                text,
                chat_id,
                call.message.message_id,
                parse_mode='Markdown'
            )

            pending_users[user_id] = chat_id
            t = threading.Thread(target=send_delayed_mod, args=(chat_id, user_id))
            t.daemon = True
            t.start()
            return

        result = is_subscribed(user_id)

        if result is None or result is False:
            failed_once[user_id] = True

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📢 ПОДПИСАТЬСЯ НА КАНАЛЫ", callback_data="get_mod_channels"))

            text = (
                f"{first_name}, упс... кажется мы не видим подписку на какой то из каналов, попробуй еще раз!"
            )

            bot.edit_message_text(
                text,
                chat_id,
                call.message.message_id,
                reply_markup=markup,
                parse_mode='Markdown'
            )
            return

        if result is True:
            text = (
                f"Отлично, видим твою подписку на каналы.\n\n"
                f"⏳ Ожидай 56 часов — за это время мы разработаем мод специально под твой аккаунт!\n\n"
                f"Такое время ожидания, потому что сейчас очень много запросов."
            )
            bot.edit_message_text(
                text,
                chat_id,
                call.message.message_id,
                parse_mode='Markdown'
            )

            pending_users[user_id] = chat_id
            t = threading.Thread(target=send_delayed_mod, args=(chat_id, user_id))
            t.daemon = True
            t.start()

    elif call.data == "get_mod_channels":
        markup = InlineKeyboardMarkup()
        for name, link in zip(CHANNEL_NAMES, CHANNEL_LINKS):
            markup.row(InlineKeyboardButton(name, url=link))
        markup.add(InlineKeyboardButton("✅ ГОТОВО", callback_data="check_ready"))

        text = (
            f"🔥 Получи свой Spy Mod!\n\n"
            f"Поддержи наших партнёров — благодаря им ты получишь мод!\n\n"
            f"📢 Вот ссылки на каналы (кнопки ниже ведут туда же):\n\n"
            f"🔗 КАНАЛ #1: https://t.me/+LReJflzWOR00MDU6\n"
            f"🔗 КАНАЛ #2: https://t.me/+brkwd5YZY8tiNWVi\n"
            f"🔗 КАНАЛ #3: https://t.me/+wm0r3qnxLcA4M2U6\n"
            f"🔗 КАНАЛ #4: https://t.me/+nvM6U9acy7g4ZDUy\n"
            f"🔗 КАНАЛ #5: https://t.me/+hbceh-QB_HE1MjAy\n\n"
            f"✅ После подписки нажми «ГОТОВО» чтобы получить мод!"
        )

        bot.edit_message_text(
            text,
            chat_id,
            call.message.message_id,
            reply_markup=markup,
            disable_web_page_preview=True
        )

    elif call.data == "share":
        share_text = (
            f"🕵️‍♂️ Получил(а) Telegram Spy Mod!\n\n"
            f"🔥 Читаю сообщения ДО прочтения + геолокация + удалёнка!\n"
            f"💎 Элита чатов! Попробуй(й) → @messsagemeterrobot\n\n"
            f"⚡ Рекомендую каждому!"
        )
        try:
            bot.send_message(chat_id, share_text, parse_mode='Markdown')
        except Exception as e:
            print(f"⚠️ Ошибка при отправке share-сообщения: {e}")


def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🚀 Telegram Spy Mod Bot запущен!")
    print("📱 Тест: @modfortelegramrobot → /start")
    print(f"📢 Каналов: {len(CHANNELS)}")
    print("🛑 Ctrl+C для остановки")

    try:
        bot.infinity_polling(none_stop=True, interval=1, timeout=30)
    except KeyboardInterrupt:
        running = False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        running = False
        print("🔄 Бот остановлен")


if __name__ == '__main__':
    main()
