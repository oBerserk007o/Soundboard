import pathlib
from pygame import mixer
from sound import Sound
import asyncio
import logging
import sounddevice as sd
import soundfile as sf


async def play_sound_sd(sound, device):
    data, fs = sf.read(f"sounds/{sound.name}")
    sd.play(data * 0.1, fs, device=device)


async def play_sound_mixer(sound, device):
    mixer.init(devicename=device)
    mixer.music.load(fr"{pathlib.Path().resolve()}\sounds\{sound.name}")
    mixer.music.play()
    mixer.music.set_volume(0.1)


class Player:
    def __init__(self, devices: {}, logger: logging):
        self.logger = logger
        self.is_playing = False
        self.devices = devices
        logger.debug("New player created")

    async def play_sound(self, sound: Sound):
        self.logger.debug(f"Playing {sound.name} for {sound.length} s")
        self.is_playing = True
        async with asyncio.TaskGroup() as tg:
            tg.create_task(play_sound_sd(sound, self.devices["headphones"]))
            tg.create_task(play_sound_mixer(sound, self.devices["cable"]))
            await asyncio.sleep(sound.length)
        self.is_playing = False
        mixer.quit()
        self.logger.debug(f"Sound {sound.name} stopped")

    def close_player(self):
        self.logger.debug("Closing player")
        del self
