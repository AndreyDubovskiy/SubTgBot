import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class ChangeAdminState(UserState):
    async def start_msg(self):
        return Response(text="Введите следующим сообщением новый пароль: ", buttons=markups.generate_cancel())

    async def next_msg(self, message: str):
        if (await config_controller.change_password_admin(self.user_chat_id, message)):
            return Response(text="Пароль изменено!", redirect="/adminmenu")
        else:
            return Response(text="Что-то пошло не так! Возможно вы не ввошли под паролем", redirect="/adminmenu")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return Response(redirect="/adminmenu")
        else:
            raise Exception("Неправильная кнопка")