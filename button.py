import tkinter
from sound import Sound
from player import Player


class Button:
    def __init__(self, text: str, sound: Sound, tk_button: tkinter.Button=None):
        self.text = text
        self.sound = sound
        self.tk_button = tk_button
        self.is_rendered = False


    def associate_tk_button(self, tk_button: tkinter.Button):
        self.tk_button = tk_button


    async def play_sound(self):
        player = Player()
        await player.play_sound(self.sound)
        player.close()
