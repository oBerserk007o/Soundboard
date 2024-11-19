import asyncio
import json
import threading
from window import Window
import logging
import time
import sounddevice as sd
from tkinter import messagebox


def load_config_files():
    menus = {}
    menu_bar = {}
    settings = {}
    
    try:
        with open("config/menus.json", "r") as f:
            menus = json.load(f)
    except:
        message = "menus.json file not found (make sure it's named correctly as 'menus.json' and in the config directory)"
        logging.exception(message)
        messagebox.showerror("Something happened", message)
        exit(0)
    
    try:
        with open("config/menu_bar.json", "r") as f:
            menu_bar = json.load(f)
    except:
        message = "menu_bar.json file not found (make sure it's named correctly as 'menu_bar.json' and in the config directory)"
        logging.exception(message)
        messagebox.showerror("Something happened", message)
        exit(0)
    
    try:
        with open("config/settings.json", "r") as f:
            settings = json.load(f)
    except:
        message = "settings.json file not found (make sure it's named correctly as 'settings.json' and in the config directory)"
        logging.exception(message)
        messagebox.showerror("Something happened", message)
        exit(0)

    return menus, menu_bar, settings


queried_devices = sd.query_devices()
devices = {"cable": "CABLE Input (VB-Audio Virtual Cable)", "headphones": "Headphones (Realtek(R) Audio)"}
for element in queried_devices:
    if devices["headphones"] in element["name"]:
        devices["headphones"] = element["index"]
        break

logging.basicConfig(
    filename=f"{time.strftime("%Y%m%d_%H%M%S")}.log",
    encoding="utf-8",
    filemode="a",
    format="[{asctime}] {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

logging.info("Application starting")


async def run_asyncio(window):
    while window.running:
        window.root.update()
        await asyncio.sleep(1 / window.settings["tps"])
    logging.info("Application shutdown from main")


def main():
    menus, menu_bar, settings = load_config_files()
    window = Window(devices, menus, settings, logging)
    window.load_menu("soundboard")
    window.load_menu_bar(menu_bar)

    asyncio.run(run_asyncio(window))

main_thread = threading.Thread(target=main)

if __name__ == "__main__":
    main_thread.start()
    main_thread.join()
