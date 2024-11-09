import markups
from states.template.UserState import UserState
from states.template.Response import Response
import config_controller

class MenuState(UserState):
    async def start_msg(self):
        if self.user_id in config_controller.list_is_loggin_admins:
            return Response(text="Меню для админов", buttons=markups.generate_markup_menu(), is_end=True)
        else:
            return Response(text="Для доступа к меню, сначала войдите под паролем", is_end=True, redirect="/log")