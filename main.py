import asyncio
from sound import Sound
from window import Window

async def main():
    window = Window()
    await window.add_button("Unga bunga", Sound("FS.mp3"))
    window.update_buttons()

asyncio.run(main())

