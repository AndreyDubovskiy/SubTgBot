from telebot.async_telebot import AsyncTeleBot
from telebot import types

class Response:
    def __init__(self, text: str = None, documents: list = None, photos: list = None, videos: list = None, buttons: types.InlineKeyboardMarkup = None, is_end: bool = False, redirect: str = None, async_end: bool = None):
        self.text = text
        self.documents = documents
        self.photos = photos
        self.videos = videos
        self.buttons = buttons
        self.is_end = is_end
        self.redirect = redirect
        self.async_end = async_end

    async def send(self, user_chat_id: str, bot: AsyncTeleBot):
        if (self.text is not None) and (self.photos is not None):
            with open(self.photos[0], "rb") as file:
                if self.buttons is not None:
                    await bot.send_photo(user_chat_id, file, self.text, reply_markup=self.buttons, parse_mode="Markdown")
                else:
                    await bot.send_photo(user_chat_id, file, self.text, parse_mode="Markdown")
                return
        if self.text is not None:
            if self.buttons is not None:
                await bot.send_message(user_chat_id, self.text, reply_markup=self.buttons, parse_mode="Markdown")
            else:
                await bot.send_message(user_chat_id, self.text, parse_mode="Markdown")
        if self.documents is not None:
            for document in self.documents:
                await bot.send_document(user_chat_id, document)
        if self.photos is not None:
            for photo in self.photos:
                await bot.send_photo(user_chat_id, photo)
        if self.videos is not None:
            for video in self.videos:
                await bot.send_video(user_chat_id, video)
