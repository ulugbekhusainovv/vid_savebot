from loader import bot,dp
from aiogram import types
from typing import Union
import sqlite3
from aiogram.types import  InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_channels():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM channels")
    channels = cursor.fetchall()
    conn.close()
    return channels

async def joinchat(chat_id):
    channels = get_channels()
    inline_keyboard = InlineKeyboardBuilder()

    uns = False

    for channel in channels:
        kanal_id, kanal_username, invite_link = channel[3], channel[1], channel[-1]
        chat_member = await bot.get_chat_member(kanal_id, chat_id)
        chat_info = await bot.get_chat(kanal_id)

        if chat_member.status not in ["creator", "administrator", "member"]:
            if kanal_username:
                kanal_url = f"https://t.me/{kanal_username}"
            else:
                kanal_url = invite_link

            button = InlineKeyboardButton(text=f"❌ {chat_info.title}", url=kanal_url)
            uns = True
            inline_keyboard.add(button)

    bot_info = await bot.get_me()
    check_button = InlineKeyboardButton(text="🔄 Tekshirish", url=f"https://t.me/{bot_info.username}?start=result")
    inline_keyboard.add(check_button)
    inline_keyboard.adjust(1)

    if uns:
        await bot.send_message(chat_id, "Bot ishlashi uchun quyidagi kanallarga qo'shiling", parse_mode='html', reply_markup=inline_keyboard.as_markup())
        return False
    else:
        return True

