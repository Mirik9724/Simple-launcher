import subprocess
import threading
from uuid import uuid1
import minecraft_launcher_lib
from random_username.generate import generate_username


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled = int(length * iteration // total)
    bar = fill * filled + '-' * (length - filled)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
    if iteration == total:
        print()


def get_gui_callback(progressbar_widget, label_widget):
    max_val = [0]

    def set_status(text):
        label_widget.config(text=text)

    def set_max(value):
        max_val[0] = value
        progressbar_widget["maximum"] = value

    def set_progress(value):
        progressbar_widget["value"] = value
        progressbar_widget.update_idletasks()

    return {
        "setStatus": set_status,
        "setMax": set_max,
        "setProgress": set_progress
    }



def get_callback():
    max_val = [0]
    return {
        "setStatus": lambda text: print(text),
        "setProgress": lambda val: print_progress_bar(val, max_val[0]),
        "setMax": lambda val: max_val.__setitem__(0, val)
    }


def install_version(version: str, loader: str, minecraft_dir: str, callback: dict):
    loader = loader.strip().lower()

    if loader == "forge":
        if not minecraft_launcher_lib.forge.supports_automatic_install(version):
            raise Exception("Forge unsupported for this version")
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version)
        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_dir, callback=callback)

    elif loader == "fabric":
        if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
            raise Exception("Fabric unsupported for this version")
        minecraft_launcher_lib.fabric.install_fabric(version, minecraft_dir, callback=callback)

    elif loader == "quilt":
        if not minecraft_launcher_lib.quilt.is_minecraft_version_supported(version):
            raise Exception("Quilt unsupported for this version")
        minecraft_launcher_lib.quilt.install_quilt(version, minecraft_dir, callback=callback)

    else:
        minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=minecraft_dir, callback=callback)


def generate_user_data(username: str = "", uuid: str = ""):
    if not username.strip():
        username = generate_username()[0]
    if not uuid.strip():
        uuid = str(uuid1())
    return username, uuid


def get_launch_command(version: str, loader: str, username: str, uuid: str, access_token: str, ram_gb: str, minecraft_dir: str):
    loader = loader.strip().lower()

    if loader == "forge":
        forge_version = minecraft_launcher_lib.forge.find_forge_version(version).replace(version + "-", "")
        version_str = f"{version}-forge-{forge_version}"
    elif loader == "fabric":
        version_str = f"fabric-loader-{minecraft_launcher_lib.fabric.FabricLoader}-{version}"
    elif loader == "quilt":
        version_str = f"quilt-loader-{minecraft_launcher_lib.quilt.QuiltLoader}-{version}"
    else:
        version_str = version

    options = {
        'username': username,
        'uuid': uuid,
        'token': access_token,
        'jvmArguments': [f"-Xmx{ram_gb}G", "-Xms128m"],
        'gameDirectory': minecraft_dir
    }

    return minecraft_launcher_lib.command.get_minecraft_command(version_str, minecraft_dir, options)


def launch_minecraft(command: list):
    subprocess.call(command)


def launch_in_thread(command: list):
    threading.Thread(target=launch_minecraft, args=(command,), daemon=True).start()
