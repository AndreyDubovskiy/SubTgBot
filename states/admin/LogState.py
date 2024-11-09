import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class LogState(UserState):
    async def start_msg(self):
        return Response(text="Введите пароль для доступа:", buttons=markups.generate_cancel())

    async def next_msg(self, message: str):
        if config_controller.log(self.user_id, message):
            return Response(text="Пароль принято!", is_end=True, redirect="/adminmenu")
        else:
            return Response(text="Неправильный пароль!\nПопробуйте ещё раз:", buttons=markups.generate_cancel())

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return None