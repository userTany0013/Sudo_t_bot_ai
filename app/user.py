from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
from app.database.requests import set_user, get_user, calculate

from decimal import Decimal


user = Router()

@user.message(F.text == 'Отмена')
@user.message(CommandStart())

async def cmd_start(message: Message, state: FSMContextF):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать!', reply_markup=kb.main)
    await state.clear()


@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balanse) > 0:
        await state.set_state(Chat.text)
        await message.answer('Введите запрос', reply_markup=kb.cansel)
    else:
        await message.answer('Недостаточно средств')


@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if Decimal(user.balanse) > 0:
        await state.set_state(Chat.wait)
        response = await gpt_text(message.text, '')
        await calculate(messag.from_user.id, response['usage'], '')
        await message.answer(response['response'])
        await state.set_state(Chat.text)
    else:
        await message.answer('Недостаточно средств')


@user.message(Chat.wait)
async def wait(message: Message):
    await message.answer('Подождите запрос выполняется')
