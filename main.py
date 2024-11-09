import sys
import config_controller
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from states.template.BuilderState import BuilderState
from states.template.UserState import UserState
from states.template.Response import Response
import os


tokkey = os.environ.get('BOT_TOKEN')

bot = AsyncTeleBot(tokkey)


state_list = {}

@bot.message_handler(commands=['off'])
async def off(message):
    await bot.send_message(chat_id=message.chat.id, text="Выключаю...")
    sys.exit()

@bot.message_handler(commands=['del_log'])
async def off(message):
    tmp = os.listdir("./logger/log")
    for i in tmp:
        os.remove(f"./logger/log/{i}")
    await bot.send_message(chat_id=message.chat.id, text="Deleted logs")


@bot.message_handler(commands=['get_log'])
async def off(message):
    filename = message.text.split("/get_log ")[-1]
    with open("./logger/log/"+filename, "rb") as file:
        await bot.send_document(chat_id=message.chat.id, document=file)

@bot.message_handler(commands=['list_log'])
async def off(message):
    tmp = os.listdir("./logger/log")
    with open("testlog.txt", "w") as file:
        for i in tmp:
            file.write(i+"\n")

    with open("testlog.txt", "rb") as file:
        await bot.send_document(chat_id=message.chat.id, document=file)


@bot.message_handler(commands=['passwordadmin','help', 'passwordmoder', 'helpadmin', 'log', 'textafter', 'start', 'texthelp', 'texthello', 'textcontact','menu'])
async def passwordadmin(message):
    await handle_message(message)

@bot.callback_query_handler(func= lambda call: True)
async def callback(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    chat_id = str(call.message.chat.id)
    try:
        user_name = str(call.from_user.username)
    except:
        user_name = None
    text = call.data
    id_list = user_id+chat_id
    if state_list.get(id_list, None) != None:
        try:
            state: UserState = state_list[id_list]
            res: Response = await state.next_btn_clk(text)
            await chek_response(chat_id, user_id, id_list, res, user_name, call.message)
        except:
            builder = BuilderState(bot)
            if not text.startswith("/geturl"):
                state = builder.create_state(text, user_id, chat_id, bot, user_name, call.message)
            else:
                state = builder.create_state("/geturl", user_id, chat_id, bot, user_name, call.message)
            state_list[id_list] = state
            if not text.startswith("/geturl"):
                state.message_obj = call.message
                res: Response = await state.start_msg()
                await chek_response(chat_id, user_id, id_list, res, user_name, call.message)
            else:
                state.message_obj = call.message
                res: Response = await state.next_btn_clk_message(text, call.message)
                await chek_response(chat_id, user_id, id_list, res, user_name, call.message)
    else:
        builder = BuilderState(bot)
        if not text.startswith("/geturl"):
            state = builder.create_state(text, user_id, chat_id, bot, user_name, call.message)
        else:
            state = builder.create_state("/geturl", user_id, chat_id, bot, user_name, call.message)
        state_list[id_list] = state
        if not text.startswith("/geturl"):
            state.message_obj = call.message
            res: Response = await state.start_msg()
            await chek_response(chat_id, user_id, id_list, res, user_name, call.message)
        else:
            state.message_obj = call.message
            res: Response = await state.next_btn_clk_message(text, call.message)
            await chek_response(chat_id, user_id, id_list, res, user_name, call.message)
    if not text.startswith("/geturl"):
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def comand(message: types.Message):
    await handle_message(message)
@bot.message_handler(func=lambda message: True, content_types=["photo", "video"])
async def comand(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    try:
        user_name = str(message.from_user.username)
    except:
        user_name = None
    id_list = user_id + user_chat_id
    if state_list.get(id_list, None) == None:
        builder = BuilderState(bot)
        state = builder.create_state("photo", user_id, user_chat_id, bot, user_name, message)
        state_list[id_list] = state
        res: Response = await state.start_msg()
        await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
    else:
        try:
            state: UserState = state_list[id_list]
            state.message_obj = message
            res: Response = await state.next_msg_photo_and_video(message)
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
        except:
            builder = BuilderState(bot)
            state = builder.create_state("photo", user_id, user_chat_id, bot, user_name, message)
            state_list[id_list] = state
            res: Response = await state.start_msg()
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)


@bot.message_handler(func=lambda message: True, content_types=["document"])
async def comand(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    try:
        user_name = str(message.from_user.username)
    except:
        user_name = None
    id_list = user_id + user_chat_id
    if state_list.get(id_list, None) == None:
        return
    else:
        try:
            state: UserState = state_list[id_list]
            state.message_obj = message
            res: Response = await state.next_msg_document(message)
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
        except:
            return

async def chek_response(user_chat_id, user_id, id_list, res: Response = None, user_name: str = None, message: types.Message = None):
    tmp_state = state_list.get(id_list)
    task_as = None
    if res != None:
        await res.send(user_chat_id, bot)
        if res.is_end:
            state_list.pop(id_list)
        if res.async_end:
            task_as = asyncio.create_task(tmp_state.async_work())
        if res.redirect != None:
            builder = BuilderState(bot)
            state = builder.create_state(res.redirect, user_id, user_chat_id, bot, user_name, message)
            state_list[id_list] = state
            res: Response = await state.start_msg()
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
        if res.async_end:
            await task_as
    else:
        state_list.pop(id_list)
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    user_chat_id = str(message.chat.id)
    try:
        user_name = str(message.from_user.username)
    except:
        user_name = None
    id_list = user_id+user_chat_id
    text = message.text
    if state_list.get(id_list, None) == None:
        builder = BuilderState(bot)
        state = builder.create_state(text, user_id, user_chat_id, bot, user_name, message)
        state_list[id_list] = state
        res: Response = await state.start_msg()
        await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
    else:
        try:
            state: UserState = state_list[id_list]
            print("msg", message)
            state.message_obj = message
            res: Response = await state.next_msg(text)
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)
        except:
            builder = BuilderState(bot)
            state = builder.create_state(text, user_id, user_chat_id, bot, user_name, message)
            state_list[id_list] = state
            res: Response = await state.start_msg()
            await chek_response(user_chat_id, user_id, id_list, res, user_name, message)

from db.controllers.UsersController import UsersController
from db.controllers.SubscriptionsController import SubscriptionsController
from db.controllers.TarifsController import TarifsController

users_controller = UsersController()
sub_controller = SubscriptionsController()
tarifs_controller = TarifsController()

@bot.chat_join_request_handler()
async def join_request_handler(join_request: types.ChatJoinRequest):
    user_id = join_request.from_user.id  # ID пользователя, запрашивающего доступ
    chat_id = join_request.chat.id       # ID группы или канала

    tmp = (await users_controller.get_by(tg_id=str(user_id)))
    if len(tmp) == 0:
        await bot.decline_chat_join_request(chat_id, user_id)
        return

    user_db = tmp[0]
    tmp = (await sub_controller.get_by(user_id=user_db.id))
    if len(tmp) == 0:
        await bot.decline_chat_join_request(chat_id, user_id)
        return
    errors = 0
    for sub in tmp:
        try:
            tarif = (await tarifs_controller.get_by(id=sub.tarif_id))[0]
            if tarif.group_id == str(chat_id):
                await bot.approve_chat_join_request(chat_id, user_id)
                return
        except:
            errors += 1

    if errors > 0:
        await bot.approve_chat_join_request(chat_id, user_id)
        return
    await bot.decline_chat_join_request(chat_id, user_id)

import asyncio
from datetime import datetime, timedelta

async def check_subscriptions():
    while True:
        now = datetime.now()
        if now.hour == 0:
            tmp = (await sub_controller.get_all())
            for sub in tmp:
                if sub.date_to < now:
                    try:
                        user_tmp = (await users_controller.get_by(id=sub.user_id))[0]
                        tarif = (await tarifs_controller.get_by(id=sub.tarif_id))[0]
                        await bot.ban_chat_member(chat_id=tarif.group_id,
                                                  user_id=user_tmp.tg_id,
                                                  until_date=datetime.now() + timedelta(minutes=3))
                        await bot.send_message(chat_id=user_tmp.tg_id, text="Ваша подписка закончилась!")
                        await sub_controller.delete(id=sub.id)
                    except:
                        pass
        await asyncio.sleep(3600)


async def start_main():
    print((await bot.get_me()))
    task1 = asyncio.create_task(bot.polling(non_stop=True))
    task2 = asyncio.create_task(config_controller.preload_config())
    task3 = asyncio.create_task(check_subscriptions())
    await task1
    await task2
    await task3

asyncio.run(start_main())






