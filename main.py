import asyncio
import logging
import sys
import threading
from handlers.callback import router
from Support_Utils.imports import dp
from Support_Utils.imports import bot
from handlers import user_check_callback
from handlers import update_subscription_callback


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    user_check_thread = threading.Thread(target=user_check_callback.run_user_check)
    update_sub = threading.Thread(target=update_subscription_callback.update_user_sub)
    user_check_thread.start()
    update_sub.start()
    asyncio.run(main())