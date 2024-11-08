import asyncio
import json
import threading
from sound import Sound
from window import Window
import logging
import time
import sounddevice as sd

configurations = {}
try:
    with open("configurations.json", "r") as f:
        configurations = json.load(f)
except:
    logging.exception("Configuration file not found (make sure it's named correctly as 'configurations.json')")

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
    window = Window(devices, logging)
    window.load_configuration(configurations["soundboard"])
    # window.add_button("Unga bunga", Sound("RAWR.mp3"), (2, 0))
    # window.add_button("skibidibopmdada", Sound("skibidibopmdada.mp3"), (3, 0))
    # window.add_button("skibidibopmdada edge", Sound("skibidibopmdadaedge.mp3"), (0, 0))
    # window.update_buttons()

    asyncio.run(run_asyncio(window))


if __name__ == "__main__":
    threading.Thread(target=main).start()
