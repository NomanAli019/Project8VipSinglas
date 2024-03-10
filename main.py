import asyncio
import logging
import sys
from aiogram.enums import ParseMode
from handlers.callback import router
from Support_Utils.imports import dp
from Support_Utils.imports import bot





async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())