import asyncio
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

# Импорт функций и глобальной переменной chat_rooms из другого файла
from chat_room import open_new_chat, join_existing_chat, generate_chat_id, chat_rooms

async def main():
  
    # Выбор или создание чата
    while True:
        action = await actions('Выберите действие:', buttons=['Создать новый чат', 'Присоединиться к существующему чату', 'Выйти'])
        
        if action == 'Создать новый чат':
            chat_id = generate_chat_id()
            nickname = await input("Введите ваш ник", required=True, placeholder="Ваше имя", validate=lambda n: "Такой ник уже используется!" if any(n in room['online_users'] for room in chat_rooms.values()) or n == '📢' else None)
            
            # Сохраняем текущий ID чата в глобальную переменную
            globals()['current_chat_id'] = chat_id
            
            # Обновляем заголовок с новым ID чата
            put_markdown(f"## 🧊 Добро пожаловать в онлайн чат! ID: {chat_id}\nИсходный код данного чата укладывается в 100 строк кода!")
            
            # Передаем управление в файл с логикой чата
            await open_new_chat(chat_id, nickname)

        elif action == 'Присоединиться к существующему чату':
            chat_id = await input("Введите ID чата (5 цифр)", required=True, placeholder="ID чата", type=NUMBER, validate=lambda n: "Такого чата не существует!" if str(n) not in chat_rooms else None)
            chat_id = str(chat_id)  # Преобразуем к строке, чтобы соответствовать ключам в словаре chat_rooms
            nickname = await input("Введите ваш ник", required=True, placeholder="Ваше имя", validate=lambda n: "Такой ник уже используется!" if n in chat_rooms[chat_id]['online_users'] or n == '📢' else None)
            
            # Сохраняем текущий ID чата в глобальную переменную
            globals()['current_chat_id'] = chat_id
            
            # Обновляем заголовок с новым ID чата
            put_markdown(f"## 🧊 Добро пожаловать в онлайн чат! ID: {chat_id}\nИсходный код данного чата укладывается в 100 строк кода!")
            
            # Присоединение к существующему чату
            await join_existing_chat(chat_id, nickname)

        elif action == 'Выйти':
            break

# Эта часть не нужна, так как запуск будет осуществляться через app.py
# if __name__ == "__main__":
#     start_server(main, debug=True, port=8080, cdn=False)
