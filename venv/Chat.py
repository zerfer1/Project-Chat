import asyncio

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100


async def main():
    global chat_msgs

    put_markdown("## 🧊 Добро пожаловать в онлайн чат!")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)