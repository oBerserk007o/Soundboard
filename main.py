import asyncio
import threading
from sound import Sound
from window import Window

async def run_asyncio(window):
    while window.running:
        window.root.update()
        await asyncio.sleep(0.01)

def main():
    window = Window()
    window.add_button("Unga bunga", Sound("RAWR.mp3"))
    window.update_buttons()

    asyncio.run(run_asyncio(window))


if __name__ == "__main__":
    threading.Thread(target=main).start()
