from aiogram.filters import Command
from loader import dp,bot
from aiogram import types
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
import random
from aiogram.utils.keyboard import InlineKeyboardBuilder


def programmer_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="Dasturchi",url=f"https://t.me/ulugbekhusainov")
    btn.adjust(1)
    return btn.as_markup()

@dp.message(Command('help'))
async def help_bot(message:types.Message):
    reaction_list = ["🫡",'🧑🏻‍💻','✊','👍🏻','👌']
    try:
        await bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji=random.choice(reaction_list))],
        is_big=False
    )
    except: 
        pass
    await message.reply("<b>Sizga qanday yordam kerak </b>", reply_markup=programmer_button())