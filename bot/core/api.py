import json
from datetime import datetime
from itertools import chain

from aiocache import Cache, cached
from pyrogram import Client
from pytz import UTC

from bot.helper.decorator import error_handler, handle_request

from .base_api import BaseBotApi
from .models import JoinedTask, Task


class CryptoBotApi(BaseBotApi):
    def __init__(self, tg_client: Client):
        super().__init__(tg_client)

    @error_handler()
    @handle_request("/system", method="GET")
    async def system(self, *, response_json: dict) -> bool:
        if response_json.get("success", False):
            self.logger.success("Login successful")
            return True
        return False

    @error_handler()
    @handle_request("/user")
    async def register(self, *, response_json: dict, json_body: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/user", method="GET")
    async def login(self, *, response_json: dict) -> bool:
        return response_json

    @error_handler()
    @handle_request("/user")
    async def register(self, *, response_json: dict, json_body: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/minigame/incubate/info", method="GET")
    async def minigame_incubate_info(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/worms/mint-status", method="GET")
    async def worms_mint_status(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/user", method="GET")
    async def user(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/project", method="GET")
    async def project(self, *, response_json: dict) -> list[Task]:
        tasks = [task.get("tasks") for task in response_json]
        return [Task(**item) for item in chain.from_iterable(tasks)]

    @error_handler()
    @handle_request("/user-join-task", method="GET")
    async def user_join_task(self, *, response_json: dict) -> list[JoinedTask]:
        return [JoinedTask(**i) for i in response_json]

    @error_handler()
    @handle_request("/project/join-task")
    async def project_join_task(self, *, response_json: dict, json_body: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/minigame/incubate/info", method="GET", raise_for_status=False)
    async def incubate_info(self, *, response_json: dict) -> dict | str:
        return response_json

    @error_handler()
    @handle_request("/minigame/incubate/upgrade", method="GET")
    async def incubate_upgrade(self, *, response_json: dict) -> dict:
        return response_json

    @cached(ttl=2 * 60 * 60, cache=Cache.MEMORY)
    @error_handler()
    @handle_request(
        "https://raw.githubusercontent.com/testingstrategy/musk_daily/main/daily.json",
        method="GET",
        full_url=True,
    )
    async def get_helper(self, *, response_json: str) -> dict:
        response_json = json.loads(response_json)
        return FundHelper(
            funds=response_json.get(str(datetime.now(UTC).date()), {}).get("funds", set()),
            **response_json,
        )
