import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class UserMenuState(UserState):
    async def start_msg(self):
        return Response(text="Меню", buttons=markups.generate_markup_user_menu(), is_end=True)