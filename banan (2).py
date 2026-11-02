import asyncio
from datetime import datetime, timezone
from telethon import TelegramClient, events

api_id = 33549426
api_hash = 'd21b3b3404d354e94a30927741022c3e'

# Текст автоответа
AUTO_REPLY_TEXT = "Привіт! Я зараз зайнятий чи відійшов від ПК. Мій AI-агент прийняв твоє повідомлення, я відповім тобі одразу, як повернуся! 🤖"

client = TelegramClient('my_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Реагируем только на личные сообщения (ЛС)
    if event.is_private:
        # Получаем информацию о вашем собственном аккаунте
        me = await client.get_me()
        
        # Запрашиваем актуальный статус пользователя (себя) через API
        user_status = (await client.get_entity(me.id)).status
        
        # Проверяем, онлайн вы сейчас или нет
        try:
            # Если в объекте статуса есть время последнего выхода (UserStatusOffline)
            was_online = user_status.was_online
            now = datetime.now(timezone.utc)
            
            # Считаем, сколько минут вы уже оффлайн
            minutes_offline = (now - was_online).total_seconds() / 60
            
            print(f"Вы оффлайн уже {minutes_offline:.1f} минут.")
            
            # Если прошло меньше 5 минут, то автоответ НЕ отправляем
            if minutes_offline < 5:
                print("Вы вышли недавно (меньше 5 минут назад). Автоответ отменен.")
                return
                
        except AttributeError:
            # Если свойства was_online нет, значит вы прямо сейчас ОНЛАЙН
            print("Вы сейчас в сети (Онлайн). Автоответ отменен.")
            return

        # Если проверки пройшли и вы оффлайн более 5 минут — отправляем ответ
        sender = await event.get_sender()
        print(f"Получено сообщение от {sender.first_name}. Отправляю автоответ...")
        await asyncio.sleep(1)  # Пауза для реалистичности
        await event.reply(AUTO_REPLY_TEXT)

print("🤖 Умный автоответчик запущен. Он сработает, только если вас нет в сети более 5 минут...")
with client:
    client.run_until_disconnected()
