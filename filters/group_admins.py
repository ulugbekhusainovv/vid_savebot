from aiogram.filters import BaseFilter
from aiogram import types
from loader import bot

class IsGroupAdmin(BaseFilter):
    
    async def __call__(self, message: types.Message) -> bool:
        chat_id = message.chat.id
        user_id = message.from_user.id

        admins = await bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        return user_id in admin_ids or await is_user_anonymous(chat_id=chat_id, user_id=user_id) or user_id == 777000


async def is_user_anonymous(chat_id, user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id)
        return chat_member.user.username == "GroupAnonymousBot" if chat_member.user else False
    except:
        return False
