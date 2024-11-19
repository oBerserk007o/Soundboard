import asyncio
from pygame import mixer
import pathlib
import sounddevice as sd
import soundfile as sf

cable = "CABLE Input (VB-Audio Virtual Cable)"
found_cable = False
headphones = "Headphones (Realtek(R) Audio)"
devices = sd.query_devices()

for element in devices:
    if headphones in element["name"]:
        print(element["name"])
        print(element["index"])
        headphones = element["index"]
        found_cable = True
        break


async def play_sound_sd(device):
    data, fs = sf.read("../sounds/RAWR.mp3")
    sd.play(data * 0.1, fs, device=device)
    print(f"playing through {device}")


async def play_sound_mixer(device):
    mixer.init(devicename=device)
    mixer.music.load(fr"{pathlib.Path().resolve()}\sounds\RAWR.mp3")
    mixer.music.play()
    mixer.music.set_volume(0.15)


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(play_sound_sd(headphones))
        tg.create_task(play_sound_mixer(cable))
        await asyncio.sleep(5)


asyncio.run(main())
