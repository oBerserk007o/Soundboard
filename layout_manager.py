import asyncio
import logging
import math
import tkinter as tk
from functools import partial
from tkinter import font as tk_font
from buttons import SoundButton


class LayoutManager:
    def __init__(self, root: tk.Tk, elements: list, commands: dict, menus: dict, button_config: dict, logger: logging):
        self.root = root
        self.elements = elements
        self.commands = commands
        self.menus = menus
        self.button_config = button_config
        self.sounds = {}

        self.logger = logger
        self.small_fonts = tk_font.Font(family="Small Fonts", size=18, weight="bold")
        print("Currently layout managing!")

    def add_label(self, text: str):
        label = (tk.Label(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=10, height=2,
                              borderwidth=0, border=0, font=self.small_fonts))
        self.elements.append(label)

    def add_sound_button(self, text: str, button: SoundButton):
        tk_button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=12, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=lambda: asyncio.run_coroutine_threadsafe(button.play_sound(),
                                                                               asyncio.get_running_loop()))
        button.associate_tk_button(tk_button)
        self.elements.append(tk_button)
        self.update_soundboard_layout()

    def add_button(self, text: str, command: str):
        func = partial(self.commands[command])
        button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=12, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=func)
        self.elements.append(button)

    def update_soundboard_layout(self):
        root_width = self.root.winfo_width()
        i = 0
        buttons_per_row = 0

        while 2 * self.button_config["min_pad_x"] + buttons_per_row * self.button_config["button_x_size"] <= root_width:
            buttons_per_row += 1

        pad_x = int((root_width - (buttons_per_row * self.button_config["button_x_size"])) / (buttons_per_row + 1))

        for element in self.elements:
            element.grid(column=i % buttons_per_row, row=math.floor(i / buttons_per_row), padx=pad_x,
                         pady=self.button_config["pad_y"])

    def clear(self):
        for element in self.elements:
            element.destroy()
        self.elements.clear()

