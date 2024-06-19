async def on_startup(dp):
    from handlers.admins.reboot_msg import reboot_msg
    print(1)
    await reboot_msg(message=None)
    print(2)

    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)
    print(3)

    from utils.set_bot_commands import set_default_commands

    await set_default_commands(dp)
    print(4)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    print(5)
    executor.start_polling(dp, on_startup=on_startup)