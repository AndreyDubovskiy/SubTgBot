import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

from db.controllers.PaymentsController import PaymentsController

class PaymentsState(UserState):
    async def start_msg(self):
        self.payments_controller = PaymentsController()

        self.current_payment = None
        self.edit = "None"

        self.MAX_ON_PAGE = 7
        self.PAGE = 0
        self.IS_PAGE = False
        self.len_payments = len((await self.payments_controller.get_all()))
        if self.len_payments > self.MAX_ON_PAGE:
            self.IS_PAGE = True
        self.current_payments = await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
        return Response(text=f"Список методов оплаты. Всего {self.len_payments} штук", buttons=markups.generate_list_payments(arr=self.current_payments, page=self.IS_PAGE), is_end=False)

    async def next_msg(self, message: str):
        if self.edit == "add_name":
            self.add_name = message
            self.edit = "add_description"
            return Response(text="Введите следующим сообщением описание к оплате, инструкцию, реквизиты, и т.д.: ", buttons=markups.generate_cancel())
        elif self.edit == "add_description":
            self.add_description = message
            self.edit = "None"
            await self.payments_controller.create(name=self.add_name, description=self.add_description)
            return Response(text="Способ оплаты добавлен!", redirect="/payments")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_payment is not None:
                return Response(redirect="/payments")
            return Response(redirect="/adminmenu")
        elif data_btn == "/next":
            self.PAGE += self.MAX_ON_PAGE
            tmp = await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
            if len(tmp) == 0:
                self.PAGE -= self.MAX_ON_PAGE
            else:
                self.current_payments = tmp
            return Response(text=f"Список методов оплаты. Всего {self.len_payments} штук", buttons=markups.generate_list_payments(arr=self.current_payments, page=self.IS_PAGE), is_end=False)
        elif data_btn == "/back":
            self.PAGE -= self.MAX_ON_PAGE
            if self.PAGE < 0:
                self.PAGE = 0
                return Response(text=f"Список методов оплаты. Всего {self.len_payments} штук",
                                buttons=markups.generate_list_payments(arr=self.current_payments, page=self.IS_PAGE),
                                is_end=False)
            else:
                tmp = await self.payments_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
                self.current_payments = tmp
                return Response(text=f"Список методов оплаты. Всего {self.len_payments} штук",
                                buttons=markups.generate_list_payments(arr=self.current_payments, page=self.IS_PAGE),
                                is_end=False)
        elif data_btn == "/add":
            self.edit = "add_name"
            return Response(text="Введите следующим сообщением название оплаты: ", buttons=markups.generate_cancel())
        elif data_btn == "/delete":
            await self.payments_controller.delete(id=self.current_payment.id)
            return Response(text="Способ оплаты удалено!", redirect="/payments")
        else:
            self.current_payment = (await self.payments_controller.get_by(id=int(data_btn)))[0]
            return Response(text=f"Название: {self.current_payment.name}\nОписание: {self.current_payment.description}", buttons=markups.generate_payment_menu())
