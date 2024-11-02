import asyncio
from sound import Sound
from window import Window

async def main():
    loop = asyncio.get_event_loop()
    window = Window(loop)
    await window.add_button("Unga bunga", Sound("FS.mp3"))
    window.update_buttons()
    # loop.run_forever()
    # loop.close()


asyncio.run(main())
