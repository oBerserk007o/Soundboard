import tkinter
from sound import Sound
from player import Player
import logging


class SoundButton:
    def __init__(self, text: str, sound: Sound, devices: dict, logger: logging, in_vol: float, out_vol: float, tk: tkinter.Button=None):
        self.text = text
        self.sound = sound
        self.tk = tk
        self.logger = logger
        self.players = []
        self.devices = devices
        self.in_vol, self.out_vol = in_vol, out_vol

    def associate_tk_button(self, tk: tkinter.Button):
        self.tk = tk

    async def play_sound(self):
        player = Player(self.devices, self.logger, self.in_vol, self.out_vol)
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
