import asyncio
import json
import tkinter as tk
from tkinter import font as tkFont, messagebox, Menu
from buttons import SoundButton
from sound import Sound
import logging


class Window:
    def __init__(self, devices: dict, menus: dict, logger: logging):
        self.buttons = []
        self.logger = logger
        self.running = True
        self.devices = devices

        self.root = tk.Tk()
        self.root.geometry("640x360+320+180")
        self.root.title("Soundboard")
        self.root.bind("<Escape>", lambda e: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.configure(background="#060812")
        self.small_fonts = tkFont.Font(family="Small Fonts", size=18, weight="bold")

        self.menus = menus

        self.commands = {
            "navigate:soundboard": lambda: self.load_menu(menus["soundboard"]),
            "navigate:settings": lambda: self.load_menu(menus["settings"]),
            "save_sounds": None,
            "load_sounds": None
        }

        logger.info("Window created")

    def add_button(self, text: str, sound: Sound, pos: ()):
        button = SoundButton(text, sound, self.devices, self.logger)
        tk_button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=int(len(text) * 0.8) + 2, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=lambda: asyncio.run_coroutine_threadsafe(button.play_sound(),
                                                                               asyncio.get_running_loop()))
        button.associate_tk_button(tk_button)
        self.buttons.append(button)

        button.tk.grid(column=pos[0], row=pos[1])
        button.is_rendered = True
        self.logger.debug(f"New button added with text '{button.text}' and sound '{button.sound.name}'")

    def update_buttons(self):
        for button in self.buttons:
            if not button.is_rendered:
                button.tk_button.grid(column=0, row=0)
                button.is_rendered = True

    def load_menu(self, selected_menu: str):
        menu = self.menus["soundboard"]

        try:
            with open(menu["sounds"]) as f:
                sounds = json.load(f)
            for i in range(len(sounds["elements"])):
                i = str(i)
                self.add_button(sounds["elements"][i]["name"], Sound(sounds["elements"][i]["sound"]),
                                tuple(sounds["elements"][i]["pos"].split(",")))
            self.update_buttons()
            self.logger.info(f"Loaded menu {menu["name"]}")
        except:
            self.logger.exception("Invalid menu file")

    def load_menu_bar(self, menu_bar: dict):
        menu_bar_tk = Menu()
        self.root.config(menu=menu_bar_tk)
        print(menu_bar["elements"])

        for i in range(len(menu_bar["elements"])):
            i = str(i)
            element = menu_bar["elements"][i]
            match element["type"]:
                case "command":
                    menu_bar_tk.add_command(label=element["title"], command=self.commands[element["command"]])
                case "cascade":
                    new_menu = Menu(menu_bar_tk)
                    menu_bar_tk.add_cascade(menu=new_menu, label=element["title"])
                    for j in range(len(element["elements"])):
                        j = str(j)
                        nested_element = element["elements"][j]
                        match nested_element["type"]:
                            case "command":
                                new_menu.add_command(label=nested_element["title"],
                                                     command=self.commands[nested_element["command"]])
                            case "separator":
                                new_menu.add_separator()

        self.logger.info(f"Loaded menu bar")

    def close(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            for button in self.buttons:
                print(button.players)
                if len(button.players) != 0:
                    button.stop_sound()
                print(button.players, " should be empty")
            self.root.destroy()
            self.running = False
            self.logger.info("Window closed")
