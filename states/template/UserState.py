from telebot.async_telebot import AsyncTeleBot
from telebot import types
from logger.MyLogger import Logger
class UserState:
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot, user_name: str = None, message: types.Message = None):
        self.user_id = user_id
        self.user_chat_id = user_chat_id
        self.bot = bot
        self.user_name = user_name
        self.message_obj = message

        self.logger = Logger(filename=self.__class__.__name__)

    async def start_msg(self):
        pass

    async def next_msg(self, message: str):
        raise Exception("Неправильная кнопка")
        pass

    async def next_msg_photo_and_video(self, message: types.Message):
        pass

    async def next_btn_clk(self, data_btn: str):
        pass

    async def next_btn_clk_message(self, data_btn:str, message: types.Message):
        pass

    async def next_msg_document(self, message: types.Message):
        pass

    async def async_work(self):
        pass