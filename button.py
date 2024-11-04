import tkinter
from sound import Sound
from player import Player
import logging


class Button:
    def __init__(self, text: str, sound: Sound, logger: logging, tk_button: tkinter.Button=None):
        self.text = text
        self.sound = sound
        self.tk_button = tk_button
        self.is_rendered = False
        self.logger = logger

    def associate_tk_button(self, tk_button: tkinter.Button):
        self.tk_button = tk_button

    async def play_sound(self):
        player = Player(self.logger)
        await player.play_sound(self.sound)
        player.close()
