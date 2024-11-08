import tkinter
from sound import Sound
from player import Player
import logging


class SoundButton:
    def __init__(self, text: str, sound: Sound, devices: {}, logger: logging, tk_button: tkinter.Button=None):
        self.text = text
        self.sound = sound
        self.tk_button = tk_button
        self.is_rendered = False
        self.logger = logger
        self.players = []
        self.devices = devices

    def associate_tk_button(self, tk_button: tkinter.Button):
        self.tk_button = tk_button

    async def play_sound(self):
        player = Player(self.devices, self.logger)
        self.players.append(player)
        await player.play_sound(self.sound)
        self.players.remove(player)
        player.close_player()

    def stop_sound(self):
        for player in self.players:
            print(self.players)
            self.players.remove(player)
            logging.debug(f"Closing player {player} from button")
            player.close_player()