import json
import sys
import minecraft_launcher_lib
import subprocess
from uuid import uuid1
from random_username.generate import generate_username
import threading

ru_l = ["Введите версию: ", "Введите ник: ", "(если его нету нечего не вводите): ", "Загрузчик модов('fabric', 'forge', 'quilt', 'нету'): ", "Сколько RAM выделить в Gygabyte: "]
en_l = ["Enter version: ", "Enter nickname: ", "(if you don't have one, don't enter anything): ", "Mod loader('fabric', 'forge', 'quilt', 'no'): ", "How much RAM to allocate in Gygabyte: "]
ua_l = ["Введіть версію: ", "Введіть нік: ", "(якщо його немає нічого не вводьте): ", "Завантажувач модів('fabric', 'forge', 'quilt', 'нету'): ", "Скільки RAM виділити в Gygabyte: "]

ru_l_s = ["Версия не найдена", "Fabric не поддерживает эту версию", "Forge не поддерживает эту версию", "JVM не может быть запущена", "Quilt не поддерживает эту версию", "RAM должно быть целым числом"]
en_l_s = ["Version not found", "Fabric does not support this version", "Forge does not support this version", "JVM can't start", "Quilt does not support this version", "RAM must be an integer"]
ua_l_s = ["Версія не знайдена", "Fabric не підтримує цю версію", "Forge не підтримує цю версію", "JVM не може бути запущена", "Quilt не підтримує цю версію", "RAM повинно бути цілим числом"]

ru_l_lib = ["Устанавливается", "уже установлен."]
en_l_lib = ["Installing", "already installed."]
ua_l_lib = ["Встановлюється", "вже встановлено."]

l_l = []
l_l_s = []
l_l_lib = []

l1 = "forge"
l2 = "fabric"
l3 = "quilt"
l4 = "neoforge"

fabric_loader_new = minecraft_launcher_lib.fabric.FabricLoader
quilt_loader_new = minecraft_launcher_lib.quilt.QuiltLoader

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    if iteration == total:
        print()

def maximum(max_value, value):
    max_value[0] = value


minecraft_directory = ".mc" #minecraft_launcher_lib.utils.get_minecraft_directory()
lang = str(input("language 'ru', 'en', 'ua': "))
if lang == "ru":
    l_l = ru_l
    l_l_s = ru_l_s
    l_l_lib = ru_l_lib

elif lang == "ua":
    l_l = ua_l
    l_l_s = ua_l_s
    l_l_lib = ua_l_lib

elif lang == "en" or "us":
    l_l = en_l
    l_l_s = en_l_s
    l_l_lib = en_l_lib

required_packages = ["random-username", "minecraft_launcher_lib"]

def is_package_installed(package):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package])
        return True
    except subprocess.CalledProcessError:
        return False

def get_outdated_packages():
    return {pkg['name'] for pkg in json.loads(subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format", "json"]))}

def install_missing_packages(packages):
    outdated = get_outdated_packages()
    for package in packages:
        if not is_package_installed(package):
            print(f"Устанавливается: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        elif package in outdated:
            print(f"Для {package} доступно обновление, но оно не будет установлено.")
        else:
            print(f"{package} уже установлена.")

install_missing_packages(required_packages)

versionc = input(l_l[0])
username = input(l_l[1])
uuidc = input("UUID" + l_l[2])
access_token = input("Access token" + str(l_l[2]))
loader = input(l_l[3])
ram_for_java = input(l_l[4])
ffv = minecraft_launcher_lib.forge.find_forge_version(versionc)
print('=======================================================================================')

if ram_for_java == "":
    print(l_l_s[3])
    sys.exit()

if not ram_for_java.isdigit():
    print(l_l_s[5])
    sys.exit()


max_value = [0]
callback = {
        "setStatus": lambda text: print(text),
        "setProgress": lambda value: printProgressBar(value, max_value[0]),
        "setMax": lambda value: maximum(max_value, value)
}
def install_mc(versionc, loader):
    if loader.replace(" ", "").lower() == l1:
        if minecraft_launcher_lib.forge.supports_automatic_install(versionc):
            print(l_l_s[2])
            sys.exit()

        else:
            pass
        minecraft_launcher_lib.forge.install_forge_version(minecraft_launcher_lib.forge.find_forge_version(versionc), minecraft_directory, callback=callback)
        # support = minecraft_launcher_lib.forge.support_automatic_install(versionc)


    elif loader.replace(" ", "").lower() == l2:
        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(versionc):
            pass

        else:
            print(l_l_s[1])
            sys.exit()

        minecraft_launcher_lib.fabric.install_fabric(str(versionc), minecraft_directory, callback=callback)

    elif loader.replace(" ", "").lower() == l3:
        if minecraft_launcher_lib.quilt.is_minecraft_version_supported(versionc):
            pass

        else:
            print(l_l_s[4])
            sys.exit()

        minecraft_launcher_lib.quilt.install_quilt(str(versionc), minecraft_directory, callback=callback)


    else:
      # if True:
        #     minecraft_launcher_lib.install.List()
        #
        # else:
       #     print(l_l_s[0])
       #     sys.exit()

        minecraft_launcher_lib.install.install_minecraft_version(versionid=versionc,
                                                             minecraft_directory=minecraft_directory, callback=callback)

install_mc(versionc, loader)

def launch_mc(uuidc, username):
    if username == "" or " ":
        username = generate_username()[0]
    if uuidc == "" or " ":
        uuidc = uuid1()

    options = {
        'username': str(username),
        'uuid': str(uuidc),
        'token': str(access_token),
        'jvmArguments': ["-Xmx" + ram_for_java + "G", "-Xms128m"],
        'gameDirectory': str(minecraft_directory)
    }

    if loader.replace(" ", "").lower() == l2:
        pass
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(
            version="fabric-loader-" + str(fabric_loader_new) + "-" + str(versionc), minecraft_directory=minecraft_directory,
            options=options))

    if loader.replace(" ", "").lower() == l1:
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(
            version=str(versionc) + "-forge-" + ffv.replace(versionc + "-", ""), minecraft_directory=minecraft_directory,
            options=options))

    if loader.replace(" ", "").lower() == l3:
        subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(
            version="quilt-loader-" + str(quilt_loader_new) + "-" + str(versionc), minecraft_directory=minecraft_directory,
            options=options))

    else:
      subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(
            version=str(versionc), minecraft_directory=minecraft_directory,
            options=options))

threadlaunch_mc = threading.Thread(target=launch_mc, args=(uuidc, username))
threadlaunch_mc.start()
#-Xincgc