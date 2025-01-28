import asyncio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js
import random

# Глобальные переменные
chat_rooms = {}
MAX_MESSAGES_COUNT = 100

def generate_chat_id():
    """Генерация уникального ID для чата из 5 цифр"""
    while True:
        chat_id = ''.join(random.choices('0123456789', k=5))
        if chat_id not in chat_rooms:
            return chat_id

async def open_new_chat(chat_id, nickname):
    # Создание нового чата
    chat_rooms[chat_id] = {
        'chat_msgs': [],
        'online_users': set(),
        'msg_box': output()
    }
    
    await join_existing_chat(chat_id, nickname)

async def join_existing_chat(chat_id, nickname):
    chat_room = chat_rooms[chat_id]
    chat_room['online_users'].add(nickname)
    chat_room['chat_msgs'].append(('📢', f'`{nickname}` присоединился к чату!'))
    put_scrollable(chat_room['msg_box'], height=300, keep_bottom=True)
    chat_room['msg_box'].append(put_markdown(f'📢 `{nickname}` присоединился к чату'))
    
    refresh_task = run_async(refresh_msg(chat_id, nickname))
    
    while True:
        data = await input_group("💭 Новое сообщение", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label': "Выйти из чата", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)
        
        if data is None:
            break
        
        chat_room['chat_msgs'].append((nickname, data['msg']))
        chat_room['msg_box'].append(put_markdown(f"`{nickname}`: {data['msg']}"))
    
    refresh_task.close()
    chat_room['online_users'].remove(nickname)
    toast("Вы вышли из чата!")
    chat_room['msg_box'].append(put_markdown(f'📢 Пользователь `{nickname}` покинул чат!'))
    chat_room['chat_msgs'].append(('📢', f'Пользователь `{nickname}` покинул чат!'))

async def refresh_msg(chat_id, nickname):
    chat_room = chat_rooms[chat_id]
    last_idx = len(chat_room['chat_msgs'])
    
    while True:
        await asyncio.sleep(1)
        
        for m in chat_room['chat_msgs'][last_idx:]:
            if m[0] != nickname:  # если не сообщение текущего пользователя
                chat_room['msg_box'].append(put_markdown(f"`{m[0]}`: {m[1]}"))
        
        # удаление старых сообщений
        if len(chat_room['chat_msgs']) > MAX_MESSAGES_COUNT:
            chat_room['chat_msgs'] = chat_room['chat_msgs'][len(chat_room['chat_msgs']) // 2:]
        
        last_idx = len(chat_room['chat_msgs'])
