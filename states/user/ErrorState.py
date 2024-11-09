import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class ErrorState(UserState):
    async def start_msg(self):
        return Response(text="Ошибка! Вы что-то ввели не так...", is_end=True)