import asyncio
import threading
from sound import Sound
from window import Window
import logging
import time
import sounddevice as sd

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
    print(sd.query_devices())
    window = Window(logging)
    window.add_button("Unga bunga", Sound("RAWR.mp3"))
    window.update_buttons()

    asyncio.run(run_asyncio(window))


if __name__ == "__main__":
    threading.Thread(target=main).start()
