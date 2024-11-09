from telebot.async_telebot import AsyncTeleBot
from telebot import types
from states.template.UserState import UserState
from states.admin.MenuState import MenuState
from states.admin.ChangeAdminState import ChangeAdminState
from states.admin.LogState import LogState
from states.admin.PaymentsState import PaymentsState
from states.admin.TarifsState import TarifsState
from states.user.UserMenuState import UserMenuState
from states.user.StartState import StartState
from states.user.ErrorState import ErrorState
from states.admin.RequestsState import RequestsState
from states.user.UserTarifsState import UserTarifsState
from states.user.UserSubState import UserSubState

class BuilderState:
    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot

    def create_state(self, data_txt: str, user_id: str, user_chat_id: str, bot: AsyncTeleBot, user_name: str = None, message: types.Message = None) -> UserState:
        defoult = ErrorState
        clssses = {
            "/menu": UserMenuState,
            "/adminmenu": MenuState,
            "/payments": PaymentsState,
            "/tarifs": TarifsState,
            "/passwordadmin": ChangeAdminState,
            "/log": LogState,
            "/start": StartState,
            "/requests": RequestsState,
            "/usertarifs":UserTarifsState,
            "📊Тарифы":UserTarifsState,
            "/usersubs": UserSubState,
            "💎Мои подписки": UserSubState

        }
        if data_txt in clssses:
            return clssses[data_txt](user_id, user_chat_id, bot, user_name, message)
        else:
            return defoult(user_id, user_chat_id, bot, user_name, message)