import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from handlers.user_handlers import register_user_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info("Bot Starting")
    config: Config = load_config()

    bot: Bot = Bot(token=config.token, parse_mode="markdownv2")
    dp: Dispatcher = Dispatcher(bot)

    register_user_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
