import asyncio
import random

import aiohttp
from pyrogram import Client

from bot.config.headers import headers
from bot.config.logger import log
from bot.config.settings import config

from .api import CryptoBotApi
from .models import SessionData


class CryptoBot(CryptoBotApi):
    def __init__(self, tg_client: Client, additional_data: dict) -> None:
        super().__init__(tg_client)
        self.authorized = False
        self.sleep_time = config.BOT_SLEEP_TIME
        self.additional_data: SessionData = SessionData.model_validate(
            {k: v for d in additional_data for k, v in d.items()}
        )

    async def register_user(self, proxy: str | None) -> None:
        data = await self.get_tg_me(proxy)
        await self.register(
            json_body={
                "name": f"{data.first_name}{data.last_name}",
                "referId": config.REF_ID,
                "username": f"{data.username}",
            }
        )

    async def login_to_app(self, proxy: str | None) -> bool:
        if self.authorized:
            return True
        tg_web_data = await self.get_tg_web_data(proxy=proxy)
        self.http_client.headers["Telegramauth"] = tg_web_data
        await self.system()
        login = await self.login()
        if not login:
            await self.register_user(proxy)
            await self.login()
            await self.system()
            self.authorized = True
            return True
        self.authorized = True
        return True

    async def run(self, proxy: str | None) -> None:
        proxy, proxy_conn = await self.get_proxy_connector(proxy)

        async with aiohttp.ClientSession(
            headers=headers,
            connector=proxy_conn,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as http_client:
            self.http_client = http_client
            if proxy:
                await self.check_proxy(proxy=proxy)

            while True:
                if self.errors >= config.ERRORS_BEFORE_STOP:
                    self.logger.error("Bot stopped (too many errors)")
                    break
                try:
                    if await self.login_to_app(proxy):
                        ...
                        # await self.minigame_incubate_info()
                        # await self.worms_mint_status()
                    await self.sleeper()
                    res = await self.user()
                    self.logger.info(f'Balance <y>{res.get("balance")}</y>')
                    joined_task = await self.user_join_task()
                    joined_ids = {i.taskId for i in joined_task}
                    tasks = await self.project()

                    for task in tasks:
                        if task.id in joined_ids or task.title == "Join BIRDS Community":
                            continue
                        if any(i in task.title for i in ["Invite", "Deposit", "Boost"]):
                            continue
                        # if '🐦' in task.title:
                        # await self.update_tg_profile("🐦", replace=True)
                        if "t.me/+" in task.url:
                            await self.join_and_archive_channel(task.url)
                        self.logger.info(f"Joining task: <green>{task.title}</green>")
                        data = {"taskId": task.id, "channelId": task.channelId, "slug": task.slug, "point": task.point}
                        await self.project_join_task(json_body=data)
                        await self.sleeper()
                        self.logger.info(f"Joined task: <green>{task.title}</green> | Earned: <y>{task.point}</y>")
                        await self.sleeper()

                    sleep_time = random.randint(*config.BOT_SLEEP_TIME)
                    self.logger.info(f"Sleep minutes {sleep_time // 60} minutes")
                    await asyncio.sleep(sleep_time)

                except RuntimeError as error:
                    raise error from error
                except Exception:
                    self.errors += 1
                    self.authorized = False
                    self.logger.exception("Unknown error")
                    await self.sleeper(additional_delay=self.errors * 8)
                else:
                    self.errors = 0
                    self.authorized = False


async def run_bot(tg_client: Client, proxy: str | None, additional_data: dict) -> None:
    try:
        await CryptoBot(tg_client=tg_client, additional_data=additional_data).run(proxy=proxy)
    except RuntimeError:
        log.bind(session_name=tg_client.name).exception("Session error")
