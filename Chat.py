from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js
import asyncio
from datetime import datetime  # Импортируем модуль datetime

chat_msgs = []  # Сохраняет сообщения чата
online_users = set()  # Список пользователей онлайн
MAX_MESSAGES_COUNT = 100  # Максимальное количество сообщений в чате

async def main():
    global chat_msgs

    put_markdown("## Это чат")

    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя", validate=lambda n: "Этот никнейм уже используется" if n in online_users or n == '' else None)
    online_users.add(nickname)

    chat_msgs.append(('', f"{nickname} присоединился к чату!", datetime.now().strftime("%H:%M:%S")))  # Добавляем время
    msg_box.append(put_markdown(f"{nickname} присоединился к чату! ({datetime.now().strftime('%H:%M:%S')})"))  # Добавляем время

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("Новое сообщение", [
            input(placeholder="Текст сообщения", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Покинуть чат", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите ваше сообщение!") if m["cmd"] == "Отправить" and not m["msg"] else None)

        if data is None:
            break

        timestamp = datetime.now().strftime("%H:%M:%S")  # Получаем текущее время
        msg_box.append(put_markdown(f"{nickname} ({timestamp}): {data['msg']}"))  # Добавляем время к сообщению
        chat_msgs.append((nickname, data['msg'], timestamp))  # Добавляем время к сообщению

    # выход из чата
    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы покинули чат!")
    msg_box.append(put_markdown(f"Пользователь {nickname} покинул чат! ({datetime.now().strftime('%H:%M:%S')})"))  # Добавляем время
    chat_msgs.append(('', f"Пользователь {nickname} покинул чат!", datetime.now().strftime("%H:%M:%S")))  # Добавляем время
    put_buttons(['Вернуться в чат'], onclick=lambda btn: run_js('window.location.reload()'))

async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)  # можно заменить на время

    while True:
        await asyncio.sleep(1)
        # Запрос на внешний сервер(recvest)
        # Отправка на внешний сервер своих ссбщений

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"{m[0]} ({m[2]}): {m[1]}"))  # Добавляем время к сообщению

        # удаление устаревших сообщений
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)

if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)