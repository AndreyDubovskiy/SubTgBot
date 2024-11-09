from datetime import datetime

import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

from db.controllers.SubscriptionsController import SubscriptionsController
from db.controllers.UsersController import UsersController
from db.controllers.TarifsController import TarifsController

class UserSubState(UserState):
    async def start_msg(self):
        self.users_controller = UsersController()
        self.tarifs_controller = TarifsController()
        self.subscriptions_controller = SubscriptionsController()

        tmp = (await self.users_controller.get_by(tg_id=self.user_id))
        if len(tmp) == 0:
            await self.users_controller.create(tg_id=self.user_id, username=self.user_name)
            tmp = (await self.users_controller.get_by(tg_id=self.user_id))

        self.user_bd_id = tmp[0].id

        self.current_subscription = None
        self.edit = "None"

        self.MAX_ON_PAGE = 7
        self.PAGE = 0
        self.IS_PAGE = False
        self.len_subscriptions = len((await self.subscriptions_controller.get_all()))
        if self.len_subscriptions > self.MAX_ON_PAGE:
            self.IS_PAGE = True
        self.current_subscriptions = await self.subscriptions_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
        return Response(text=f"Список подписок. Всего {self.len_subscriptions} штук",
                        buttons=markups.generate_list_user_subs(arr=self.current_subscriptions, page=self.IS_PAGE),
                        is_end=False)

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_subscription is not None:
                return Response(redirect="/usersubs")
            return Response(redirect="/menu")
        elif data_btn == "/next":
            self.PAGE += self.MAX_ON_PAGE
            tmp = await self.subscriptions_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
            if len(tmp) == 0:
                self.PAGE -= self.MAX_ON_PAGE
            else:
                self.current_subscriptions = tmp
            return Response(text=f"Список подписок. Всего {self.len_subscriptions} штук",
                            buttons=markups.generate_list_user_subs(arr=self.current_subscriptions, page=self.IS_PAGE),
                            is_end=False)
        elif data_btn == "/back":
            self.PAGE -= self.MAX_ON_PAGE
            if self.PAGE < 0:
                self.PAGE = 0
                return Response(text=f"Список подписок. Всего {self.len_subscriptions} штук",
                                buttons=markups.generate_list_user_subs(arr=self.current_subscriptions, page=self.IS_PAGE),
                                is_end=False)
            tmp = await self.subscriptions_controller.get_by(limit=self.MAX_ON_PAGE, offset=self.PAGE)
            self.current_subscriptions = tmp
            return Response(text=f"Список подписок. Всего {self.len_subscriptions} штук",
                            buttons=markups.generate_list_user_subs(arr=self.current_subscriptions, page=self.IS_PAGE),
                            is_end=False)
        else:
            try:
                self.current_subscription = (await self.subscriptions_controller.get_by(id=int(data_btn)))[0]
                current_tarif = None
                try:
                    current_tarif = (await self.tarifs_controller.get_by(id=self.current_subscription.tarif_id))[0]
                    return Response(text=f"Тариф: {current_tarif.name}\n"
                                         f"Действует до: {self.current_subscription.date_to.day}.{self.current_subscription.date_to.month}.{self.current_subscription.date_to.year}\n",
                                    buttons=markups.generate_cancel())
                except:
                    return Response(text=f"Тариф: Тариф было удалено\n"
                                         f"Действует до: {self.current_subscription.date_to.day}.{self.current_subscription.date_to.month}.{self.current_subscription.date_to.year}\n",
                                    buttons=markups.generate_cancel())
            except:
                raise Exception("Неправильная кнопка")
