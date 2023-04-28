import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.config import Config, load_config
from handlers.collection_handlers import register_collection_handlers
from handlers.other_handlers import register_other_handlers
from handlers.geolocation_handlers import register_geolocation_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info("Bot Starting")
    config: Config = load_config()

    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=config.token, parse_mode="markdownv2")
    dp: Dispatcher = Dispatcher(bot, storage=storage)

    register_collection_handlers(dp, config.admin_id)
    register_geolocation_handlers(dp)
    register_other_handlers(dp)

    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
