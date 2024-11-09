import pickle
from db.controllers.ConfigsController import ConfigsController
controller = ConfigsController()
PASSWORD_ADMIN = "admin"

list_is_loggin_admins = []

async def preload_config():
    resp = await controller.get_config(name="config")
    if resp.binary_data != None:
        await read_ini()
    else:
        await write_ini()
async def write_ini():
    config = {}
    config["PASSWORD_ADMIN"] = PASSWORD_ADMIN
    await controller.set_config(name="config",
                          binary_data=pickle.dumps(config))


async def read_ini():
    global PASSWORD_ADMIN
    config = pickle.loads((await controller.get_config(name="config")).binary_data)
    PASSWORD_ADMIN = str(config["PASSWORD_ADMIN"])

def log(chat_id, password):
    global list_is_loggin_admins
    if password == PASSWORD_ADMIN and (not chat_id in list_is_loggin_admins):
        list_is_loggin_admins.append(chat_id)
        return True
    elif chat_id in list_is_loggin_admins:
        return True
    return False

async def change_password_admin(chat_id, password):
    global PASSWORD_ADMIN, list_is_loggin_admins
    if chat_id in list_is_loggin_admins:
        PASSWORD_ADMIN = password
        await write_ini()
        list_is_loggin_admins = []
        return True
    else:
        return False