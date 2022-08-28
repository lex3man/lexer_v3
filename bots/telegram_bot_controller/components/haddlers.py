from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

async def command_react(message : types.Message):
    
    
    
    await message.answer(str(message.bot.id), reply_markup = ReplyKeyboardRemove())

def register_message_handlers(dp:Dispatcher, auth_token:str):
    
    dp.register_message_handler(command_react, commands = ['start'])