import asyncio
import json
import threading
from window import Window
import logging
import time
import sounddevice as sd

menus = {}
menu_bar = {}

try:
    with open("config/menus.json", "r") as f:
        menus = json.load(f)
except:
    logging.exception("menus.json file not found (make sure it's named correctly as 'menus.json' and in the config directory)")

try:
    with open("config/menu_bar.json", "r") as f:
        menu_bar = json.load(f)
except:
    logging.exception("menu_bar.json file not found (make sure it's named correctly as 'menu_bar.json' and in the config directory)")


queried_devices = sd.query_devices()
devices = {"cable": "CABLE Input (VB-Audio Virtual Cable)", "headphones": "Headphones (Realtek(R) Audio)"}
for element in queried_devices:
    if devices["headphones"] in element["name"]:
        devices["headphones"] = element["index"]
        break

logging.basicConfig(
    filename=f"{time.strftime('%Y%m%d_%H%M%S')}.log",
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
        await asyncio.sleep(0.01)
    logging.info("Application shutdown from main")


def main():
    window = Window(devices, menus, logging)
    window.load_menu("soundboard")
    window.load_menu_bar(menu_bar)

    asyncio.run(run_asyncio(window))


if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()
