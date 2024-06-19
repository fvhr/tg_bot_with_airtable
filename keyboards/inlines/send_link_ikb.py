from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_link_ikb = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [InlineKeyboardButton(text='Отмена❌', callback_data='cancel_send_link')]
                                  ])
