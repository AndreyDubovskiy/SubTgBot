import os

import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from db.controllers.RequestsController import RequestsController
from db.controllers.UsersController import UsersController
from db.controllers.TarifsController import TarifsController
from db.controllers.PaymentsController import PaymentsController
from db.controllers.SubscriptionsController import SubscriptionsController
from db.controllers.HistorysController import HistorysController

from logger.MyLogger import Logger

class RequestsState(UserState):
    async def start_msg(self):
        self.requests_controller = RequestsController()
        self.users_controller = UsersController()
        self.tarifs_controller = TarifsController()
        self.payments_controller = PaymentsController()
        self.subscriptions_controller = SubscriptionsController()
        self.historys_controller = HistorysController()

        self.logger = Logger(filename="RequestsState", autosave=True)

        self.current_request = None

        self.edit = "None"

        self.index_request = 0
        self.len_requests = len((await self.requests_controller.get_all()))

        tmp = await self.requests_controller.get_by(limit=1, offset=self.index_request)
        if len(tmp) == 0:
            return Response(text=f"Запросы закончились! \n\nВсего {self.len_requests} штук",
                            buttons=markups.generate_cancel())
        self.current_request = tmp[0]
        self.current_tarif = (await self.tarifs_controller.get_by(id=self.current_request.tarif_id))[0]
        self.current_payment = (await self.payments_controller.get_by(id=self.current_request.payment_id))[0]
        self.current_user = (await self.users_controller.get_by(id=self.current_request.user_id))[0]
        if self.current_request.path_photo != None:
            return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                            photos=[self.current_request.path_photo],
                            buttons=markups.generate_markup_admin_requests())
        else:
            return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                            buttons=markups.generate_markup_admin_requests())

    async def next_msg(self, message: str):
        if self.edit == "comment":
            self.edit = "None"
            self.logger.log("NO", f"{self.current_user.tg_id} {self.current_user.username} {self.current_tarif.name} {self.current_payment.name} {message}")
            await self.bot.send_message(chat_id=self.current_user.tg_id, text=f"Запрос отклонён! ❌\n"
                                                                              f"Тариф: {self.current_tarif.name}\n"
                                                                              f"Оплата: {self.current_payment.name}\n"
                                                                              f"Комментарий: {message}")
            os.remove(self.current_request.path_photo)
            await self.requests_controller.delete(id=self.current_request.id)
            self.len_requests -= 1
            tmp = await self.requests_controller.get_by(limit=1, offset=self.index_request)
            if len(tmp) == 0:
                return Response(text=f"Запросы закончились! \n\nВсего {self.len_requests} штук",
                                buttons=markups.generate_cancel())
            self.current_request = tmp[0]
            self.current_tarif = (await self.tarifs_controller.get_by(id=self.current_request.tarif_id))[0]
            self.current_payment = (await self.payments_controller.get_by(id=self.current_request.payment_id))[0]
            self.current_user = (await self.users_controller.get_by(id=self.current_request.user_id))[0]
            if self.current_request.path_photo != None:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                photos=[self.current_request.path_photo],
                                buttons=markups.generate_markup_admin_requests())
            else:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                buttons=markups.generate_markup_admin_requests())
        else:
            raise Exception("Неправильная кнопка")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return Response(redirect="/adminmenu")
        elif data_btn == "/skip":
            self.index_request += 1
            tmp = await self.requests_controller.get_by(limit=1, offset=self.index_request)
            if len(tmp) == 0:
                return Response(text=f"Запросы закончились! \n\nВсего {self.len_requests} штук",
                                buttons=markups.generate_cancel())
            self.current_request = tmp[0]
            self.current_tarif = (await self.tarifs_controller.get_by(id=self.current_request.tarif_id))[0]
            self.current_payment = (await self.payments_controller.get_by(id=self.current_request.payment_id))[0]
            self.current_user = (await self.users_controller.get_by(id=self.current_request.user_id))[0]
            if self.current_request.path_photo != None:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                photos=[self.current_request.path_photo],
                                buttons=markups.generate_markup_admin_requests())
            else:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                buttons=markups.generate_markup_admin_requests())
        elif data_btn == "/yes":
            self.logger.log("YES",
                            f"{self.current_user.tg_id} {self.current_user.username} {self.current_tarif.name} {self.current_payment.name}")
            user_id_to_add = self.current_user.tg_id
            group_id_to_add = self.current_tarif.group_id
            tt = await self.subscriptions_controller.get_by(user_id=self.current_user.id)
            current_tt = None
            for i in tt:
                tarif = (await self.tarifs_controller.get_by(id=i.tarif_id))[0]
                if tarif.group_id == group_id_to_add:
                    current_tt = i
                    break
            if current_tt != None:
                current_tt.date_to = current_tt.date_to + relativedelta(months=self.current_tarif.mouths, days=self.current_tarif.days)
                await self.subscriptions_controller.save(current_tt)
            else:
                await self.subscriptions_controller.create(user_id=self.current_user.id,
                                                       tarif_id=self.current_tarif.id,
                                                       date_to=(datetime.now() + relativedelta(
                                                           months=self.current_tarif.mouths,
                                                           days=self.current_tarif.days)))
            await self.bot.send_message(chat_id=self.current_user.tg_id, text=f"Запрос принят! ✅\n"
                                                                              f"Тариф: {self.current_tarif.name}\n"
                                                                                f"Оплата: {self.current_payment.name}\n",
                                        reply_markup=markups.generate_markup_url(self.current_tarif.invite_link))
            os.remove(self.current_request.path_photo)
            await self.historys_controller.create(tg_id=user_id_to_add, group_id=group_id_to_add, payment_id=self.current_payment.id, date_to=(datetime.now() + relativedelta(
                                                           months=self.current_tarif.mouths,
                                                           days=self.current_tarif.days)))
            await self.requests_controller.delete(id=self.current_request.id)
            self.len_requests -= 1
            tmp = await self.requests_controller.get_by(limit=1, offset=self.index_request)
            if len(tmp) == 0:
                return Response(text=f"Запросы закончились! \n\nВсего {self.len_requests} штук",
                                buttons=markups.generate_cancel())
            self.current_request = tmp[0]
            self.current_tarif = (await self.tarifs_controller.get_by(id=self.current_request.tarif_id))[0]
            self.current_payment = (await self.payments_controller.get_by(id=self.current_request.payment_id))[0]
            self.current_user = (await self.users_controller.get_by(id=self.current_request.user_id))[0]
            if self.current_request.path_photo != None:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                photos=[self.current_request.path_photo],
                                buttons=markups.generate_markup_admin_requests())
            else:
                return Response(text=f"Запросы. Всего {self.len_requests} штук\n"
                                 f"Пользователь: {self.current_user.tg_id} {self.current_user.username}\n"
                                 f"Тариф: {self.current_tarif.name}\n"
                                 f"Оплата: {self.current_payment.name}\n",
                                buttons=markups.generate_markup_admin_requests())
        elif data_btn == "/no":
            self.edit = "comment"
            return Response(text=f"Введите комментарий к отклонению:", buttons=markups.generate_cancel())
        else:
            raise Exception("Неправильная кнопка")
