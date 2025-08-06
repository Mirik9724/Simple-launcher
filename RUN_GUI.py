import tkinter as tk
from tkinter import ttk, messagebox
from slcore import *

def start_install():
    version = version_entry.get()
    loader = loader_entry.get()
    username = username_entry.get()
    uuid = uuid_entry.get()
    token = token_entry.get()
    ram = ram_entry.get()
    directory = dir_entry.get()

    if not ram.isdigit():
        messagebox.showerror("Ошибка", "RAM должно быть числом")
        return

    username_final, uuid_final = generate_user_data(username, uuid)
    callback = get_gui_callback(progress, status_label)

    def run():
        try:
            install_version(version, loader, directory, callback)
        except Exception as e:
            messagebox.showerror("Ошибка установки", str(e))
            return

        command = get_launch_command(version, loader, username_final, uuid_final, token, ram, directory)
        launch_in_thread(command)
        messagebox.showinfo("Успех", "Minecraft запускается...")

    threading.Thread(target=run, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Minecraft Launcher")

tk.Label(root, text="Версия:").grid(row=0, column=0, sticky="e")
version_entry = tk.Entry(root)
version_entry.grid(row=0, column=1)

tk.Label(root, text="Загрузчик:").grid(row=1, column=0, sticky="e")
loader_entry = tk.Entry(root)
loader_entry.grid(row=1, column=1)

tk.Label(root, text="Ник:").grid(row=2, column=0, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=2, column=1)

tk.Label(root, text="UUID:").grid(row=3, column=0, sticky="e")
uuid_entry = tk.Entry(root)
uuid_entry.grid(row=3, column=1)

tk.Label(root, text="Token:").grid(row=4, column=0, sticky="e")
token_entry = tk.Entry(root)
token_entry.grid(row=4, column=1)

tk.Label(root, text="RAM (ГБ):").grid(row=5, column=0, sticky="e")
ram_entry = tk.Entry(root)
ram_entry.grid(row=5, column=1)

tk.Label(root, text="Minecraft Директория:").grid(row=6, column=0, sticky="e")
dir_entry = tk.Entry(root)
dir_entry.grid(row=6, column=1)

# Прогресс-бар и статус
progress = ttk.Progressbar(root, length=300)
progress.grid(row=7, column=0, columnspan=2, pady=10)

status_label = tk.Label(root, text="Ожидание...")
status_label.grid(row=8, column=0, columnspan=2)

# Кнопка запуска
start_button = tk.Button(root, text="Установить и запустить", command=start_install)
start_button.grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()
