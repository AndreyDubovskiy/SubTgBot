from telebot import types
import db.database as db
import config_controller
from typing import List


def generate_yes_no():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="✅Да✅", callback_data="/yes"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_ready_exit():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="✅Готово✅", callback_data="/yes_ready"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_delete_cancel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="🗑Удалить🗑", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_list_payments(arr, page = False, with_add = True):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in arr:
        markup.add(types.InlineKeyboardButton(text=i.name, callback_data=str(i.id)))
    if page:
        markup.add(types.InlineKeyboardButton(text="➡️️", callback_data="/next"))
        markup.add(types.InlineKeyboardButton(text="⬅️", callback_data="/back"))
    if with_add:
        markup.add(types.InlineKeyboardButton(text="❇️Добавить❇️", callback_data="/add"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_list_user_subs(arr, page = False):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in arr:
        markup.add(types.InlineKeyboardButton(text=f"Действует до {i.date_to.day}.{i.date_to.month}.{i.date_to.year}", callback_data=str(i.id)))
    if page:
        markup.add(types.InlineKeyboardButton(text="➡️️", callback_data="/next"))
        markup.add(types.InlineKeyboardButton(text="⬅️", callback_data="/back"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_cancel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_markup_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="Спасобы оплаты", callback_data="/payments"))
    markup.add(types.InlineKeyboardButton(text="Тарифы", callback_data="/tarifs"))
    markup.add(types.InlineKeyboardButton(text="Запросы", callback_data="/requests"))
    markup.add(types.InlineKeyboardButton(text="Изменить пароль админа", callback_data="/passwordadmin"))

    return markup

def generate_markup_admin_requests():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="✅Подтвердить✅", callback_data="/yes"))
    markup.add(types.InlineKeyboardButton(text="❌Отклонить❌", callback_data="/no"))
    markup.add(types.InlineKeyboardButton(text="➡️Пропустить➡️", callback_data="/skip"))
    markup.add(types.InlineKeyboardButton(text="Закончить", callback_data="/cancel"))

    return markup

def generate_markup_user_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="📊Тарифы", callback_data="/usertarifs"))
    markup.add(types.InlineKeyboardButton(text="💎Мои подписки", callback_data="/usersubs"))

    return markup

def generate_markup_user_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton(text="📊Тарифы"))
    markup.add(types.KeyboardButton(text="💎Мои подписки"))

    return markup

def generate_markup_user_buy_or_cancel():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="✅Оплачено✅", callback_data="/ready"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))

    return markup

def generate_markup_url(url):
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="Ссылка на канал", url=url))

    return markup

def generate_markup_user_tarif():
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(text="❇️Купить❇️", callback_data="/buy"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))

    return markup

def generate_payment_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="📝Редактировать📝", callback_data="/edit"))
    markup.add(types.InlineKeyboardButton(text="🗑Удалить🗑", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup

def generate_cancel_or_save():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="📝Оставить как есть📝", callback_data="/save"))
    markup.add(types.InlineKeyboardButton(text="Вернуться назад ↩️", callback_data="/cancel"))
    return markup