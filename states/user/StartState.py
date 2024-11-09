import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class StartState(UserState):
    async def start_msg(self):
        return Response(text="Управляйте ботом с помощью кнопок, или же введите /menu", is_end=True, buttons=markups.generate_markup_user_menu_keyboard())