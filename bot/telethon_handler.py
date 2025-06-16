from telethon import TelegramClient, events
from config import api_id, api_hash, chat_id, blacklist, eta_limit, frequency_limit
from utils.logger import write_log
from bot.aiogram_handler import bot
from utils.market import mexc_check
import re
import datetime

client = TelegramClient("DCA", api_id, api_hash)
mesid = 0


@client.on(events.NewMessage(chats=-1002599723862))
async def handler(event):
    global mesid
    side = None
    ticker_match = None

    if event.message.reply_to_msg_id == mesid:
        await bot.send_message(chat_id, f"Зміна Статусу!")
        await event.message.forward_to("@FineDcaFilter")
        return

    text = event.message.message.lower()
    frequency = (lambda m: int(float(m[0]) * (1000 if m[1] == "k" else 1)))(re.search(r"frequency: \$([\d.]+)(k?)", text).groups())
    eta_match = re.search(r"eta:\s*(?:(\d+)h)?\s*,?\s*(?:(\d+)m)?", text)
    ehours = int(eta_match.group(1)) if eta_match and eta_match.group(1) else 0
    eminutes = int(eta_match.group(2)) if eta_match and eta_match.group(2) else 0
    eta = ehours + eminutes / 60

    if "🟩" in text:
        side = "🟩 Long"
        ticker_match = re.search(r"buying \s*([^\s-]+)", text)
    elif "🟥" in text:
        side = "🟥 Short"
        ticker_match = re.search(r"selling \s*([^\s-]+)", text)
    ticker = ticker_match.group(1).upper()

    write_log(ticker, "\nОтримано новий сигнал")
    write_log(ticker, "Розпочато перевірку")

    if frequency > frequency_limit:
        write_log(ticker, f"✅ Пройдено перевірку на Частоту {frequency}")

        if eta < eta_limit:
            write_log(ticker, f"✅ Пройдено перевірку на Довжину DCA {eta}")

            if "range: ❌" not in text:
                write_log(ticker, "✅ Пройдено перевірку на range")

                if not any(word in ticker for word in blacklist):
                    write_log(ticker, "✅ Пройдено перевірку на blacklist")

                    if await mexc_check(ticker):
                        write_log(ticker, "✅ Токен є на MEXC")

                        now = datetime.datetime.now()
                        delta = datetime.timedelta(hours=eta)
                        close_time_form = now + delta
                        close_time = close_time_form.strftime("%H:%M")

                        await event.message.forward_to("@FineDcaFilter")
                        await bot.send_message(chat_id, f"{side}\nТікер: <b>{ticker}</b>\n🕒 Закриття о {close_time}",
                                         parse_mode="HTML")
                        mesid = event.message.id
                        write_log(ticker, "✅ Успішно відправлено")

                    else: write_log(ticker, "❌ Немає токена на MEXC")
                else: write_log(ticker, "❌ Заблоковано через blacklist")
            else: write_log(ticker, "❌ Є Range: повідомлення відхилено")
        else: write_log(ticker, f"❌Сильно довга DCA: {eta}")
    else: write_log(ticker, f"❌ Дуже маленька частота купівлі: {frequency}")
