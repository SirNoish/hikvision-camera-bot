"""Utils module."""
import asyncio
import logging
import random
import string
from datetime import datetime
from typing import Any, TYPE_CHECKING
from uuid import uuid4

from pyrogram.types import Message

from hikcamerabot.config.config import get_main_config
from hikcamerabot.constants import CmdSectionType

if TYPE_CHECKING:
    from hikcamerabot.camera import HikvisionCam


class Singleton(type):
    """Singleton class."""

    _instances = {}

    def __call__(cls, *args, **kwargs) -> Any:
        """Check whether instance already exists.

        Return existing or create new instance and save to dict."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


async def shallow_sleep_async(sleep_time: float = 0.1) -> None:
    await asyncio.sleep(sleep_time)


def gen_uuid() -> str:
    return uuid4().hex


def gen_random_str(length=4) -> str:
    return ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _
        in range(length))


def format_ts(ts: float, time_format: str = '%a %b %d %H:%M:%S %Y') -> str:
    return datetime.fromtimestamp(ts).strftime(time_format)


def make_bold(text: str) -> str:
    """Wrap input string in HTML bold tag."""
    return f'<b>{text}</b>'


def get_user_info(message: Message) -> str:
    """Return user information who interacts with bot."""
    chat = message.chat
    return f'Request from user_id: {chat.id}, username: {chat.username}, ' \
           f'full name: {chat.first_name} {chat.last_name}'


def build_command_presentation(commands: dict[str, list[str]],
                               cam: 'HikvisionCam') -> str:
    groups = []
    visibility_opts: dict[str, bool] = cam.conf.command_sections_visibility
    for section_desc, cmds in commands.items():
        if visibility_opts[CmdSectionType(section_desc).name]:
            rendered_cmds = '\n'.join([f'/{cmd}' for cmd in cmds])
            groups.append(f'{section_desc}\n{rendered_cmds}')
    return '\n\n'.join(groups)


def setup_logging() -> None:
    logging.getLogger().setLevel(get_main_config().log_level)
    logging.getLogger('pyrogram').setLevel(logging.WARNING)
    log_format = '%(asctime)s - [%(levelname)s] - [%(name)s:%(lineno)s] - %(message)s'
    logging.basicConfig(format=log_format)