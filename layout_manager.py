import asyncio
import json
import logging
import tkinter as tk
from functools import partial
from tkinter import font as tk_font

from buttons import SoundButton
from player import Sound


class LayoutManager:
    def __init__(self, root: tk.Tk, elements: list, commands: dict, menus: dict, default_size: int, logger: logging):
        self.root = root
        self.elements = elements
        self.commands = commands
        self.menus = menus
        self.default_size = default_size
        self.sounds = {}

        self.logger = logger
        self.small_fonts = tk_font.Font(family="Small Fonts", size=18, weight="bold")
        print("Currently layout managing!")

    def load_menu(self, selected_menu: str):
        menu = self.menus[selected_menu]
        self.clear()

        for i in range(len(menu["elements"])):
            i = str(i)
            element = menu["elements"][i]
            match element["type"]:
                case "label":
                    self.add_label(element["name"], tuple(element["pos"].split(",")))
                case "add_button":
                    self.add_button(element["name"], tuple(element["pos"].split(",")), element["command"])

        match menu["name"]:
            case "soundboard":
                try:
                    with open(menu["sounds"]) as f:
                        sounds = json.load(f)
                        self.sounds = sounds
                    for i in range(len(sounds["elements"])):
                        i = str(i)
                        self.add_sound_button(sounds["elements"][i]["name"], Sound(sounds["elements"][i]["sound"]),
                                              tuple(sounds["elements"][i]["pos"].split(",")))
                except:
                    self.logger.exception("Invalid menu file")
            case "settings":
                pass

        self.logger.info(f"Loaded menu {menu['name']}")

    def add_label(self, text: str, pos: tuple):
        label = (tk.Label(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=10, height=2,
                              borderwidth=0, border=0, font=self.small_fonts))
        label.grid(column=pos[0], row=pos[1])
        self.elements.append(label)

    def add_sound_button(self, text: str, sound: Sound, pos: tuple, button: SoundButton):
        button = SoundButton(text, sound, self.devices, self.logger, self.settings["in_volume"], self.settings["out_volume"])
        tk_button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=12, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=lambda: asyncio.run_coroutine_threadsafe(button.play_sound(),
                                                                               asyncio.get_running_loop()))
        button.associate_tk_button(tk_button)
        self.elements.append(button)

        button.tk.grid(column=pos[0], row=pos[1])

    def add_button(self, text: str, pos: tuple, command: str):
        func = partial(self.commands[command])
        button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=12, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=func)
        self.elements.append(button)

        button.grid(column=pos[0], row=pos[1])

    def clear(self):
        for element in self.elements:
            try:
                element.tk.destroy()
            except:
                element.destroy()
        self.elements.clear()

