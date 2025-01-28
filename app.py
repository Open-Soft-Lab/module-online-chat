from pywebio.platform.tornado import start_server
from chat_menu import main as chat_menu_main

if __name__ == "__main__":
    # Запуск сервера с функцией главного меню чатов
    start_server(chat_menu_main, debug=True, port=8080, cdn=False)
