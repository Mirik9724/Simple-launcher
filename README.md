# Simple-launcher

A lightweight, modular Minecraft launcher core in Python, based on [`minecraft-launcher-lib`](https://github.com/AnonymousX102/minecraft-launcher-lib).
Supports **Vanilla**, **Forge**, **Fabric**, and **Quilt**.

---

## 📌 About the Project

This repository contains a **core launcher module** (`slcore.py`) that can be used to:

* Install Minecraft versions with modloader support
* Track installation progress (CLI or GUI)
* Generate user data (username, UUID)
* Create and launch Minecraft commands

The rest of the files are **tests** or **examples** of how to use the core.

---

## 📁 Structure

```
Simple-launcher/
│
├── slcore.py            # ✅ Core module (installing, launching, progress handling)
│
├── RUN_GUI.py       # 🧾 CLI usage example
├── RUN_LAUNCHER.py       # 🧾 Tkinter GUI usage example
└── README.md
```

> Only `slcore.py` is considered the actual core logic. Everything else is either for testing or demonstrating how to use it.

---

## ✅ Features of `slcore.py`

* Install Minecraft (with or without Forge/Fabric/Quilt)
* Modular callbacks for progress display
* Clean user data generator (username/UUID)
* Launch via subprocess or background thread
* Works with CLI, GUI, or any Python frontend

---

## 📦 Requirements

Install required packages:

```bash
pip install minecraft-launcher-lib random-username
```

Tkinter is required for GUI examples. Usually preinstalled, or install via:

```bash
# Debian/Ubuntu
sudo apt install python3-tk
```

---

## 🔧 How to Use `slcore.py`

### 1. Install Minecraft Version

```python
from slcore import install_version, get_callback

callback = get_callback()  # CLI-style progress
install_version("1.20.1", "forge", "/path/to/.minecraft", callback)
```

### 2. Generate User

```python
from slcore import generate_user_data

username, uuid = generate_user_data()
```

### 3. Get Launch Command

```python
from slcore import get_launch_command

command = get_launch_command(
    version="1.20.1",
    loader="forge",
    username=username,
    uuid=uuid,
    access_token="token",
    ram_gb="4",
    minecraft_dir="/path/to/.minecraft"
)
```

### 4. Launch Minecraft

```python
from slcore import launch_in_thread

launch_in_thread(command)  # or launch_minecraft(command) for blocking call
```

---

## 🖥️ CLI Example

See `RUN_GUI.py` for full terminal usage demo using `input()` and the CLI progress bar.

---

## 🖼️ GUI Example

See `gui_example.py` for an example using **Tkinter** with a `ttk.Progressbar` and a status label.

Use `get_gui_callback(progressbar, label)` from `slcore.py` to connect the UI to the install logic.

---

## ⚙️ Supported Loaders

| Loader   | Supported |
|----------| --------- |
| Vanilla  | ✅         |
| Forge    | ✅         |
| Fabric   | ✅         |
| Quilt    | ✅         |
| NeoForge | ❌         |
| Custom   | ❌         |

---

## 💡 Notes

* You can use `slcore.py` in **any** Python-based frontend: CLI, Tkinter, PyQt, Flask, etc.
* All launcher configuration (version, modloader, memory, path, etc.) must be passed from external code.
* No hardcoded GUI or logic — only backend.

---