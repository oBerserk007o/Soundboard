import pathlib

from pygame import mixer
from sound import Sound
import asyncio
import logging

cable = "CABLE Input (VB-Audio Virtual Cable)"
headphones = "Headphones (Realtek(R) Audio)"


async def play_sound_through_device(sound: Sound, device: str):
    mixer.init(devicename=device)
    mixer.music.load(fr"{pathlib.Path().resolve()}\Sounds\{sound.name}")
    mixer.music.play()
    mixer.music.set_volume(0.15)


class Player:
    def __init__(self, logger: logging):
        self.logger = logger
        self.is_playing = False
        logger.debug("New player created")

    async def play_sound(self, sound: Sound):
        self.logger.debug(f"Playing {sound.name}")
        self.is_playing = True
        async with asyncio.TaskGroup() as tg:
            tg.create_task(play_sound_through_device(sound, cable))
            tg.create_task(play_sound_through_device(sound, headphones))
            await asyncio.sleep(sound.length)
        self.is_playing = False
        mixer.quit()
        self.logger.debug(f"Sound {sound.name} stopped")

    def close(self):
        self.logger.debug("Closing player")
        del self
