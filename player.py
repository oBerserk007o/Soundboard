import pathlib
from pygame import mixer
from sound import Sound
import asyncio
import logging
import sounddevice as sd
import soundfile as sf


async def play_sound_sd(sound, device, volume):
    data, fs = sf.read(f"sounds/{sound.name}")
    sd.play(data * volume * 0.3, fs, device=device)


async def play_sound_mixer(sound, device, volume):
    mixer.init(devicename=device)
    mixer.music.load(fr"{pathlib.Path().resolve()}\sounds\{sound.name}")
    mixer.music.play()
    mixer.music.set_volume(volume * 0.3)


class Player:
    def __init__(self, devices: {}, logger: logging, in_vol: float, out_vol: float):
        self.logger = logger
        self.is_playing = False
        self.devices = devices
        self.in_vol, self.out_vol = in_vol, out_vol
        logger.debug("New player created")

    async def play_sound(self, sound: Sound):
        self.logger.debug(f"Playing {sound.name} for {sound.length} s")
        self.is_playing = True
        async with asyncio.TaskGroup() as tg:
            tg.create_task(play_sound_sd(sound, self.devices["headphones"], self.in_vol))
            tg.create_task(play_sound_mixer(sound, self.devices["cable"], self.out_vol))
            await asyncio.sleep(sound.length)
        self.is_playing = False
        mixer.quit()
        self.logger.debug(f"Sound {sound.name} stopped")

    def close_player(self):
        self.logger.debug("Closing player")
        del self
