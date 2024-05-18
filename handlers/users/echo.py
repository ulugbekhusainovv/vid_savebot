from loader import dp,bot
from aiogram import types,html,F
import sqlite3,re
from datetime import datetime
from aiogram.types import  InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.filters import CommandStart,Command
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
import random
from .vid_down import Downloads
import json
import speedtest
import asyncio



async def speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    ping = st.results.ping
    return ping

# async def measure_speed():
#     st = speedtest.Speedtest()
#     st.get_best_server()

#     download_speed = await asyncio.to_thread(st.download) / 1_000_000  # MB/s
#     upload_speed = await asyncio.to_thread(st.upload) / 1_000_000  # MB/s
#     ping = st.results.ping

#     return download_speed, upload_speed, ping



@dp.message(Command('speed'))
async def speed_msg(message:types.Message):
    reaction_list = [ "⚡","👨‍💻","🗿","🔥"]
    try:
        await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
        is_big=False
    )
    except: 
        pass
    await bot.send_chat_action(message.chat.id, "typing")
    data = await message.answer("🚀...")
    ping = await speed()
    await data.edit_text(f"""
🚀Bot tezligi: {ping:.2f} ms""")



conn = sqlite3.connect('bot.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR(30) NULL,
        full_name TEXT,
        telegram_id INTEGER,
        lang_code VARCHAR(10) NULL,
        registration_date TEXT
    )
''')
conn.commit()

msg_text = """<b>🔥 Assalomu alaykum. @videos_downbot ga Xush kelibsiz. Bot orqali quyidagilarni yuklab olishingiz mumkin:

• Instagram - stories, post va IGTV 

• TikTok - suv belgisiz video;

• Snapchat - video;


🚀 Media yuklashni boshlash uchun uning havolasini yuboring.</b>"""


async def is_user_registered(telegram_id):
    cursor.execute('''
        SELECT telegram_id FROM users WHERE telegram_id=?
    ''', (telegram_id,))
    result = cursor.fetchone()
    return result is not None

def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)



@dp.message(F.text)
async def echo_bot(message:types.Message):
    full_name =  html_escape(message.from_user.full_name)
    telegram_id = message.from_user.id
    is_premium = message.from_user.is_premium
    username = message.from_user.username
    lang_code = message.from_user.language_code

    if not await is_user_registered(telegram_id):
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO users (username,full_name,telegram_id,lang_code,registration_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (username,full_name, telegram_id, lang_code, registration_date))
        conn.commit()
        await bot.send_message(chat_id=-1002011354418,text=f"New 👤: {full_name}\nUsername📩: {f'@{username}' if username else 'None'}\nTelegram 🆔: {html.code(value=telegram_id)}\nReg 📆: {registration_date}\nPremium🤑: {is_premium}\nLang: {lang_code}",reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Profile", url=f"tg://user?id={telegram_id}")
            ]
        ]
))

    link = message.text
    if "instagram.com" in link:
        time_message = await message.answer('⏳')
        result = await Downloads.instagram(url=str(link))
        if result and 'result' in result and len(result['result']) > 0:
            for media in result['result']:
                video_url = media.get('url')
                if video_url:
                    try:
                        video = await message.answer_video(video_url,caption="<b>@videos_downbot bot orqali yuklab olindi</b>")
                        await bot.forward_message(chat_id=-1002090016379, from_chat_id=message.chat.id, message_id=video.message_id)
                    except:
                        await message.answer(f"<b>⚠️ File 📂 hajmi kattaligi tufayli bot uni yubora 📤 olmaydi vidoeni mana bu link orqali yuklab olishingiz mumkin: {html.link(value='Link', link=video_url)} </b>", disable_web_page_preview=True)
            await time_message.delete()
        else:
            await time_message.delete()
            await message.answer("Muammo yuzaga keldi iltimos keyinroq qayta urining")


    elif "tiktok.com" in link:
        time_message = await message.answer('⏳')
        result = await Downloads.tiktok(url=str(link))
        if result and 'result' in result and len(result['result']) > 0:
            video_url = result['result']['url']
            if video_url:
                try:
                    video = await message.answer_video(video_url,caption="<b>@videos_downbot bot orqali yuklab olindi</b>")
                    await bot.forward_message(chat_id=-1002090016379, from_chat_id=message.chat.id, message_id=video.message_id)
                except:
                    await message.answer(f"<b>⚠️ File 📂 hajmi kattaligi tufayli bot uni yubora 📤 olmaydi vidoeni mana bu link orqali yuklab olishingiz mumkin: {html.link(value='Link', link=video_url)} </b>")
        else:
            await message.answer("Muammo yuzaga keldi iltimos keyinroq qayta urining")

    elif 'snapchat.com' in link:
        time_message = await message.answer('⏳')
        snapchat = await Downloads.snapchat(url=str(link))
        try:
            video_url = snapchat['result']['story']['mediaUrl']
            if video_url:
                try:
                    video = await message.answer_video(video_url,caption="<b>@videos_downbot bot orqali yuklab olindi</b>")
                    await bot.forward_message(chat_id=-1002090016379, from_chat_id=message.chat.id, message_id=video.message_id)
                except:
                    await message.answer(f"<b>⚠️ File 📂 hajmi kattaligi tufayli bot uni yubora 📤 olmaydi vidoeni mana bu link orqali yuklab olishingiz mumkin: {html.link(value='Link', link=video_url)} </b>")
            await time_message.delete()
        except:
            await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qayta urining")
    else:
        await message.answer(msg_text)
        reaction_list = ["🤔","🤨", "😐","👀", "🤷‍♂", "🤷"]
        await message.answer("⚠️ Hech narsa topilmadi")
        try:
            await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
            is_big=False
        )
        except: 
            pass
    



