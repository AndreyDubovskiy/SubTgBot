from telebot import types

import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

from db.controllers.TarifsController import TarifsController
from db.controllers.PaymentsController import PaymentsController
from db.controllers.RequestsController import RequestsController
from db.controllers.UsersController import UsersController

class UserTarifsState(UserState):
    async def start_msg(self):
        self.tarifs_controller = TarifsController()
        self.payments_controller = PaymentsController()
        self.requests_controller = RequestsController()
        self.users_controller = UsersController()

        tmp = (await self.users_controller.get_by(tg_id=self.user_id))
        if len(tmp) == 0:
            await self.users_controller.create(tg_id=self.user_id, username=self.user_name)
            tmp = (await self.users_controller.get_by(tg_id=self.user_id))

        self.user_bd_id = tmp[0].id

        self.edit = "None"

        self.current_tarif = None
        self.current_payment = None

        self.MAX_ON_PAGE = 7
        self.PAGE = 0
        self.PAGE_PAYMENT = 0
        self.IS_PAGE = False
        self.IS_PAGE_PAYMENT = False
        self.len_tarifs = len((await self.tarifs_controller.get_all()))
        self.len_payments = len((await self.payments_controller.get_all()))
        if self.len_payments > self.MAX_ON_PAGE:
            self.IS_PAGE_PAYMENT = True
        if self.len_tarifs > self.MAX_ON_PAGE:
            self.IS_PAGE = True
        self.current_tarifs = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
        return Response(text=f"Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку",
                        buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE, with_add=False),
                        is_end=False)

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_payment is not None:
                return Response(redirect="/usertarifs")
            return Response(redirect="/menu")
        elif data_btn == "/next":
            self.PAGE += self.MAX_ON_PAGE
            tmp = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
            if len(tmp) == 0:
                self.PAGE -= self.MAX_ON_PAGE
            else:
                self.current_tarifs = tmp
            return Response(text=f"Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку", buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE), is_end=False)
        elif data_btn == "/back":
            self.PAGE -= self.MAX_ON_PAGE
            if self.PAGE < 0:
                self.PAGE = 0
                return Response(text=f"Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку",
                                buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE),
                                is_end=False)
            else:
                tmp = await self.tarifs_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
                self.current_tarifs = tmp
                return Response(text=f"Чтобы ознакомиться с тарифом, выберите необходимый, нажав на соответствующую кнопку",
                                buttons=markups.generate_list_payments(arr=self.current_tarifs, page=self.IS_PAGE),
                                is_end=False)
        elif data_btn == "/next" and self.edit == "buy_tarif":
            self.PAGE_PAYMENT += self.MAX_ON_PAGE
            tmp = await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE_PAYMENT)
            if len(tmp) == 0:
                self.PAGE_PAYMENT -= self.MAX_ON_PAGE
            return Response(text="Выберете способ оплаты:", buttons=markups.generate_list_payments(arr=(await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE_PAYMENT)), page=self.IS_PAGE_PAYMENT, with_add=False))
        elif data_btn == "/back" and self.edit == "buy_tarif":
            self.PAGE_PAYMENT -= self.MAX_ON_PAGE
            if self.PAGE_PAYMENT < 0:
                self.PAGE_PAYMENT = 0
            return Response(text="Выберете способ оплаты:", buttons=markups.generate_list_payments(
                    arr=(await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE_PAYMENT)),
                    page=self.IS_PAGE_PAYMENT, with_add=False))
        elif data_btn == "/ready":
            self.edit = "add_doc_or_photo"
            return Response(text="Следующим сообщением отправьте скриншот оплаты: ", buttons=markups.generate_cancel())
        elif data_btn == "/buy":
            self.edit = "buy_tarif"
            return Response(text="Выберете способ оплаты:", buttons=markups.generate_list_payments(arr=(await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE_PAYMENT)), page=self.IS_PAGE_PAYMENT, with_add=False))
        else:
            try:
                if self.edit == "buy_tarif":
                    self.edit = "None"
                    self.current_payment = (await self.payments_controller.get_by(id=int(data_btn)))[0]
                    return Response(text=f"{self.current_payment.description}", buttons=markups.generate_markup_user_buy_or_cancel())
                else:
                    self.current_tarif = (await self.tarifs_controller.get_by(id=int(data_btn)))[0]
                    return Response(text=f"Название: *{self.current_tarif.name}*\n{self.current_tarif.description}", buttons=markups.generate_markup_user_tarif())
            except:
                raise Exception("Неправильная кнопка")

    async def next_msg_photo_and_video(self, message: types.Message):
        if self.edit == "add_doc_or_photo":
            if message.photo:
                i = message.photo[-1]
                file_info = await self.bot.get_file(i.file_id)
                file_path = file_info.file_path
                bytess = await self.bot.download_file(file_path)
                with open(f'post_tmp/{i.file_id}.jpg', 'wb') as file:
                    file.write(bytess)
                await self.requests_controller.create(user_id=self.user_bd_id,
                                                      tarif_id=self.current_tarif.id,
                                                      payment_id=self.current_payment.id,
                                                      path_photo=f'post_tmp/{i.file_id}.jpg',
                                                      path_doc=None)
                return Response(text="Запрос отослано!\n\nЧерез некоторое время его проверят и отправят результат", redirect="/usertarifs")
        else:
            raise Exception("Неправильная кнопка")