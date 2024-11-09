from telebot import types

import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

from db.controllers.TarifsController import TarifsController

class TarifsState(UserState):
    async def start_msg(self):
        self.tarifs_controller = TarifsController()

        self.current_tarif = None
        self.current_payment = None
        self.edit = "None"

        self.MAX_ON_PAGE = 7
        self.PAGE = 0
        self.IS_PAGE = False
        self.len_tarifs = len((await self.tarifs_controller.get_all()))
        if self.len_tarifs > self.MAX_ON_PAGE:
            self.IS_PAGE = True
        self.current_tarifs = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
        return Response(text=f"Список тарифов. Всего {self.len_tarifs} штук", buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE), is_end=False)

    async def next_msg(self, message: str):
        if self.edit == "add_name":
            self.add_name = message
            self.edit = "add_description"
            return Response(text="Введите следующим сообщением описание тарифа: ", buttons=markups.generate_cancel())
        elif self.edit == "add_description":
            self.add_description = message
            self.edit = "add_days"
            return Response(text="Введите срок действия тарифа у формате дд-мм, где дд - количество дней, мм - количество месяцев. Например, 15-1 (15 дней и 1 месяц): ", buttons=markups.generate_cancel())
        elif self.edit == "add_days":
            try:
                message = message.replace(" ", "")
                self.add_days = int(message.split("-")[0])
                self.add_months = int(message.split("-")[1])
                self.edit = "add_group"
                return Response(
                    text="Бот должен быть админом канала!\n\nВведите следующим сообщением айди канала, или же перешлите любой пост с канала в бота: ",
                    buttons=markups.generate_cancel())
            except:
                return Response(text="Вы ввели что-то неправильно! Попробуйте ещё раз:", buttons=markups.generate_cancel())
        elif self.edit == "add_group":
            try:
                print("USER CHAT ID", self.user_chat_id)
                print("CHAT ID", str(self.message_obj.forward_from_chat.id))
                if self.user_chat_id == str(self.message_obj.forward_from_chat.id):
                    self.add_group = message
                else:
                    self.add_group = str(self.message_obj.forward_from_chat.id)
            except Exception as ex:
                print("EXCEPTION", ex)
                self.add_group = message
            self.edit = "None"
            await self.tarifs_controller.create(name=self.add_name, description=self.add_description, group_id=self.add_group, days=self.add_days, mouths=self.add_months, invite_link=(await self.get_invate_link(self.add_group)))
            return Response(text="Тариф добавлен!", redirect="/tarifs")

    async def get_invate_link(self, grp_id: str):
        tmp = await self.tarifs_controller.get_by(group_id=grp_id)
        if len(tmp) == 0:
            return str((await self.bot.create_chat_invite_link(chat_id=grp_id, creates_join_request=True)).invite_link)
        else:
            return tmp[0].invite_link


    async def next_msg_photo_and_video(self, message: types.Message):
        if self.edit == "add_group":
            print("USER CHAT ID", self.user_chat_id)
            print("CHAT ID", str(self.message_obj.forward_from_chat.id))
            self.add_group = str(self.message_obj.forward_from_chat.id)
            self.edit = "None"
            await self.tarifs_controller.create(name=self.add_name, description=self.add_description, group_id=self.add_group, days=self.add_days, mouths=self.add_months, invite_link=(await self.get_invate_link(self.add_group)))
            return Response(text="Тариф добавлен!", redirect="/tarifs")

    async def next_msg_document(self, message: types.Message):
        if self.edit == "add_group":
            print("USER CHAT ID", self.user_chat_id)
            print("CHAT ID", str(self.message_obj.forward_from_chat.id))
            self.add_group = str(self.message_obj.forward_from_chat.id)
            self.edit = "None"
            await self.tarifs_controller.create(name=self.add_name, description=self.add_description, group_id=self.add_group, days=self.add_days, mouths=self.add_months, invite_link=(await self.get_invate_link(self.add_group)))
            return Response(text="Тариф добавлен!", redirect="/tarifs")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_payment is not None:
                return Response(redirect="/tarifs")
            return Response(redirect="/adminmenu")
        elif data_btn == "/next":
            self.PAGE += self.MAX_ON_PAGE
            tmp = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
            if len(tmp) == 0:
                self.PAGE -= self.MAX_ON_PAGE
            else:
                self.current_tarifs = tmp
            return Response(text=f"Список тарифов. Всего {self.len_tarifs} штук", buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE), is_end=False)
        elif data_btn == "/back":
            self.PAGE -= self.MAX_ON_PAGE
            if self.PAGE < 0:
                self.PAGE = 0
                return Response(text=f"Список тарифов. Всего {self.len_tarifs} штук",
                                buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE),
                                is_end=False)
            else:
                tmp = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
                self.current_tarifs = tmp
                return Response(text=f"Список тарифов. Всего {self.len_tarifs} штук",
                                buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE),
                                is_end=False)
        elif data_btn == "/add":
            self.edit = "add_name"
            return Response(text="Введите следующим сообщением название тарифа: ", buttons=markups.generate_cancel())
        elif data_btn == "/delete":
            await self.tarifs_controller.delete(id=self.current_tarif.id)
            return Response(text="Тариф удалено!", redirect="/tarifs")
        else:
            self.current_tarif = (await self.tarifs_controller.get_by(id=int(data_btn)))[0]
            return Response(text=f"Название: {self.current_tarif.name}\nОписание: {self.current_tarif.description}", buttons=markups.generate_payment_menu())