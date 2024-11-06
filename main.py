import asyncio
import threading
from sound import Sound
from window import Window

async def run_asyncio(window):
    while window.running:
        window.root.update()
        await asyncio.sleep(0.01)
    for button in window.buttons:
        print("a" if button.player else "b")
        if button.player:
            button.stop_sound()
            print(button.player)

def main():
    window = Window()
    window.add_button("Unga bunga", Sound("RAWR.mp3"))
    window.update_buttons()

    asyncio.run(run_asyncio(window))


if __name__ == "__main__":
    threading.Thread(target=main).start()
