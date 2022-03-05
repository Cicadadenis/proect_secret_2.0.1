from datetime import datetime
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
from proxy_checking import ProxyChecker
from telethon import TelegramClient
from datetime import datetime, timedelta
from data.config import ADMINS, api_id, api_hash
from filters import IsNotSubscribed
from keyboards.inline.menu import admin_menu, main_menu, back_to_main_menu, goo
from loader import dp
from utils.db_api.db_commands import *
from utils.other_utils import get_user_date, send_message_to_chat
from datetime import datetime

from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu import back_to_main_menu, personal_menu
from loader import dp, bot
from utils.db_api.db_commands import select_user
from states.states import BroadcastState, GiveTime, TakeTime

# ========================SHOW USER CABINET========================
from utils.other_utils import get_user_date

@dp.callback_query_handler(text="deposit")
async def deposit(call: CallbackQuery):
    await call.message.answer("@satanasat")

@dp.callback_query_handler(text="give_time")
async def edit_commission(call: CallbackQuery, state: FSMContext):
    msg_to_edit = await call.message.edit_text("<b>🆔    Введите ID человека:</b>",
                                               reply_markup=back_to_main_menu)
    await GiveTime.GT1.set()
    await state.update_data(msg_to_edit=msg_to_edit)

@dp.message_handler(state=GiveTime.GT1)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit = data.get("msg_to_edit")
    user_id = message.text
    await message.delete()
    await GiveTime.next()
    await state.update_data(user_id=user_id)
    await msg_to_edit.edit_text("<b>⏰  Введите время в часах которое выдать человеку:</b>", reply_markup=back_to_main_menu)

@dp.message_handler(state=GiveTime.GT2)
async def receive_com(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_to_edit, user_id = data.get("msg_to_edit"), data.get("user_id")
    try:
        hours = int(message.text)
        await message.delete()
        date_when_expires = datetime.now() + timedelta(hours=hours)
        date_to_db = str(date_when_expires).split(".")[0].replace("-", " ").split(":")
        date_to_db = " ".join(date_to_db[:-1])
        await update_date(user_id, date_to_db)
        await state.finish()
        await msg_to_edit.edit_text("<b>Доступ выдан.</b>", reply_markup=back_to_main_menu)
    except ValueError:
        await msg_to_edit.edit_text("<b>    ⏰Не верный формат, попробуйте еще раз.</b>")


@dp.callback_query_handler(text="personal_acc")
async def personal_acc(call: CallbackQuery):
    bot_info = await bot.get_me()
    user = await select_user(call.from_user.id)
    result_date = await get_user_date(call.from_user.id)
    await call.message.edit_text(f"<b>🖥 Профиль\n\n"
                                 f"🆔Ваш ID: <code>{call.from_user.id}</code>\n"
                                 f"📦Юзер добавленного аккаунта: <code>{user[1]}</code>\n"
                                 f"🧿Ваша подписка продлится еще:</b> "
                                 f"<code>{result_date}</code>",
                                 reply_markup=personal_menu)

# ========================DELETE BROADCAST MESSAGE========================
# WITH STATE
@dp.callback_query_handler(text="delete_this_message", state="*")
async def del_broadcast_msg(call: CallbackQuery):
    await call.message.delete()
    await bot_start(call.message)


# ========================SHOW MAIN MENU========================
# /start WITHOUT STATE


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    #if not await select_user(message.from_user.id):
    #    await add_user(message.from_user.id)
    #stat, user = await select_statistic(), await select_user(message.from_user.id)
    #result_date = await get_user_date(message.from_user.id)
    #proxy = await select_user_proxy(message.from_user.id)
    #if not await select_user(message.from_user.id):
    #    await add_user(message.from_user.id)
    #stat, user = await select_statistic(), await select_user(message.from_user.id)
    #result_date = await get_user_date(message.from_user.id)
    #proxy = await select_user_proxy(message.from_user.id)
    await message.answer(
        "<b>👋 Привет, данный бот создан для удобного авто~постинга во все чаты телеграмма!\n\n"
        "♻️ Отправлять любому юзеру своё сообщение от добавленного аккаунта!\n"
        "♻️ Добавлять хоть 100 чатов (и настраивать их одновременно)\n"
        "♻️Включать / отключать рассылки.\n"
        "♻️Менять все параметры, задержки / текст / фото / и другие!\n\n"
        "🚀Удачного использования!</b>",
        reply_markup=goo)
    
@dp.callback_query_handler(text="back_to_main_menu")
async def support(call: CallbackQuery, state: FSMContext):
    result_date = await get_user_date(call.from_user.id)
    sms = open('sms.txt', 'r').read()
    tt = open('time.txt', 'r')
    ti = int(tt.read())
    tt.close()
    file_list = os.listdir('sessions')
    sms = open('sms.txt', 'r').read()
    x = len(file_list)   
    file_list = os.listdir('sessions')
    sms = open('sms.txt', 'r').read()
    x = len(file_list)
    uss = open('ussers.txt', 'r')
    ff = uss.readlines()
    z = len(ff)
    #user = await select_user(call.from_user.id)
    #stat, proxy = await select_statistic(), await select_user_proxy(call.from_user.id)
    #result_date = await get_user_date(call.from_user.id)
    try:
        sms = open('sms.txt', 'r').read()
        path = f'pics/broadcast/cicada.jpg'
        with open(path, 'rb') as f:
            photo = f.read()
        await call.message.answer_photo(photo=photo, caption=f"{sms}")
        await call.message.answer(
            f"🔼🔼🔼 <b>Так выглядит ваш пост</b> 🔼🔼🔼\n\n"
            f"👤    <b>🤖Аккаунтов добавлено: </b>   {x}\n"
            f"🕔    <b>Тайминг Установлен на</b> {ti} <b>сек.</b>\n\n"
            f"🔓    <b>Подписка активна:</b> {result_date}\n"
            f"👩‍👩‍👧‍👧    <b>Участников для спама:</b> {z}", reply_markup=await main_menu(call.message.from_user.id))
    except:
        await call.message.answer(sms)
        await call.message.answer(
            f"🔼🔼🔼 <b>Так выглядит ваш пост</b> 🔼🔼🔼\n\n"
            f"👤    <b>🤖Аккаунтов добавлено: </b>   {x}\n"
            f"🕔    <b>Тайминг Установлен на</b> {ti} <b>сек.</b>\n\n"
            f"🔓    <b>Подписка активна:</b> {result_date}\n"
            f"👩‍👩‍👧‍👧    <b>Участников для спама:</b> {z}", reply_markup=await main_menu(call.message.from_user.id))


# BACK FROM ANY HANDLER TO MAIN MENU WITH STATE
@dp.callback_query_handler(text="admin", state="*")
async def support(call: CallbackQuery, state: FSMContext):
    

    await state.finish()
    if str(call.from_user.id) in ADMINS:
        await call.message.edit_text("Админ-меню", reply_markup=admin_menu)


# ========================INFO BUTTON========================
@dp.callback_query_handler(text="inf")
async def support(call: CallbackQuery):
    await call.message.edit_text(
        "<b>👋 Привет, данный бот создан для удобного авто~постинга во все чаты телеграмма!\n\n"
        "♻️ Отправлять любому юзеру своё сообщение от добавленного аккаунта!\n"
        "♻️ Добавлять хоть 100 чатов (и настраивать их одновременно)\n"
        "♻️Включать / отключать рассылки.\n"
        "♻️Менять все параметры, задержки / текст / фото / и другие!\n\n"
        "🚀Удачного использования!</b>",
        reply_markup=back_to_main_menu)


@dp.callback_query_handler(IsNotSubscribed())
async def answer_call(call: CallbackQuery):
    await call.answer("❗️У вас нету подписки, чтобы пользоваться ботом")