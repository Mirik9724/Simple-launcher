# main.py

from slcore import *

def main():
    version = input("Версия: ")
    loader = input("Загрузчик (forge/fabric/quilt/none): ")
    username = input("Ник (пусто = рандом): ")
    uuid = input("UUID (пусто = сгенерируется): ")
    token = input("Access Token (пусто = любой): ")
    ram = input("RAM (в ГБ): ")
    directory = input("Директория майнкрафта (например, .mc): ")

    if not ram.isdigit():
        print("ОШИБКА: RAM должно быть целым числом")
        return

    username, uuid = generate_user_data(username, uuid)
    callback = get_callback()

    try:
        install_version(version, loader, directory, callback)
    except Exception as e:
        print("Ошибка установки:", e)
        return

    cmd = get_launch_command(version, loader, username, uuid, token, ram, directory)
    launch_in_thread(cmd)
    print("Minecraft запускается...")

if __name__ == "__main__":
    main()
