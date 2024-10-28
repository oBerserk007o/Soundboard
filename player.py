from pygame import mixer
from sound import Sound
import asyncio

cable = "CABLE Input (VB-Audio Virtual Cable)"
headphones = "Headphones (Realtek(R) Audio)"


class Player:
    def __init__(self):
        self.is_playing = False


    async def play_sound(self, sound: Sound):
        self.is_playing = True
        print(f"Playing {sound.name}")
        await self.play_sound_through_device(sound, cable)
        await self.play_sound_through_device(sound, headphones)
        await asyncio.sleep(sound.length)
        self.is_playing = False
        mixer.quit()


    async def play_sound_through_device(self, sound: Sound, device: str):
        mixer.init(devicename=device)
        mixer.music.load(fr"C:\Users\Dorno\Desktop\Coding projects\Python\Soundboard\sounds\{sound.name}")
        mixer.music.play()
        mixer.music.set_volume(0.15)


    def close(self):
        del self


if __name__ == "__main__":
    async def main():
        player = Player()
        await player.play_sound(Sound("SG.mp3"))
    asyncio.run(main())