from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import users_table


def roles_ikb():
    ikb = InlineKeyboardMarkup(row_width=2)
    users = list(filter(lambda x: 'Заказчик' in x['fields'], users_table.all()))
    for user in users:
        ikb.add(InlineKeyboardButton(text=user['fields']['Полное имя'],
                                     callback_data=f'give_{user["fields"]["tg_user_id"]}'))
    return ikb


do_role_ikb = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [InlineKeyboardButton(text='Выдать роль', callback_data='give_role'),
                                        InlineKeyboardButton(text='Забрать роль', callback_data='remove_role')],
                                       [InlineKeyboardButton(text='Изменить', callback_data='change')]
                                   ])


def create_remove():
    users = list(
        filter(lambda x: 'Администратор' not in x['fields'] and 'Заказчик' not in x['fields'], users_table.all()))
    remove_role_ikb = InlineKeyboardMarkup()
    for user in users:
        user_field = user['fields']
        remove_role_ikb.add(InlineKeyboardButton(text=user_field['Полное имя'],
                                                 callback_data=f'remove_{user_field["tg_user_id"]}_{user["id"]}'))
    return remove_role_ikb


def create_change():
    users = list(filter(lambda x: 'Администратор' not in x['fields'], users_table.all()))
    change_role_ikb = InlineKeyboardMarkup()
    for user in users:
        user_field = user['fields']
        change_role_ikb.add(InlineKeyboardButton(text=user_field['Полное имя'],
                                                 callback_data=f'change_{user["id"]}'))
    return change_role_ikb


def create_change_fields(user_id):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Сменить имя', callback_data=f'ch_name_{user_id}')]
                                ])


cancel_change_ikb = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [InlineKeyboardButton(text='Отмена❌', callback_data='cancel_change')]
                                         ])
