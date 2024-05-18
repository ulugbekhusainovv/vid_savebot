from aiogram.filters import CommandStart
from loader import dp,bot
from aiogram import types,html
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3,re
from datetime import datetime
from aiogram.types import  InlineKeyboardButton,InlineKeyboardMarkup

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



@dp.message(CommandStart())
async def start_bot(message:types.Message):
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
    await message.answer(msg_text)


