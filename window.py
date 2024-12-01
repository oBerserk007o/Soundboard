import asyncio
import json
import os
import pathlib
import tkinter as tk
from tkinter import font as tk_font, messagebox, Menu, simpledialog
from tkinter.filedialog import askopenfilename
import logging
from functools import partial

from buttons import SoundButton
from layout_manager import LayoutManager
from player import Sound


def choose_settings_for_button():
    name = simpledialog.askstring(title="Name", prompt="What do want to name it? : ")
    if name != None:
        file = askopenfilename().split("/")[-1]
    else:
        return
    if file is None:
        return
    return [name, file]


class Window:
    def __init__(self, devices: dict, menus: dict, settings: dict, logger: logging):
        self.sounds = {}
        self.elements = []
        self.logger = logger
        self.running = True
        self.devices = devices

        self.root = tk.Tk()
        self.root.geometry("640x360+320+180")
        self.root.title("Soundboard")
        # self.root.bind("<Escape>", lambda e: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.configure(background="#060812")
        self.small_fonts = tk_font.Font(family="Small Fonts", size=18, weight="bold")

        self.menus = menus

        self.commands = {
            "navigate": lambda to: self.load_menu(to[0]),
            "add_sound_button": lambda: self.add_sound_button_from_button(),
            "save_sounds": lambda: self.save_sounds(),
            "load_sounds": lambda: self.load_sounds()
        }

        self.settings = settings

        self.layout_manager = LayoutManager(self.root, [], self.commands, menus, 12, logger)

        logger.info("Window created")

    def add_label(self, text: str, pos: tuple):
        label = (tk.Label(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=int(len(text) * 0.8) + 2, height=2,
                              borderwidth=0, border=0, font=self.small_fonts))
        label.grid(column=pos[0], row=pos[1])
        self.elements.append(label)

    def add_sound_button_from_button(self):
        settings = choose_settings_for_button()
        if settings is not None:
            try:
                name = settings[0]
                sound = Sound(settings[1])
                pos = (0, 0)
                self.add_sound_button(settings[0], sound, (pos[0], pos[1] + 1))
                self.sounds["elements"][str(int(max(self.sounds["elements"].keys())) + 1)] = {"name": name, "sound": sound.name, "pos": f"{pos[0]},{pos[1]}"}
            except:
                self.logger.exception("")
                self.logger.error("Please choose a sound file within the 'sounds' directory")

    def add_sound_button(self, text: str, sound: Sound, pos: tuple):
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

        if "sounds" in menu:
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
        else:
            pass
        self.logger.info(f"Loaded menu {menu['name']}")

    def load_menu_bar(self, menu_bar: dict):
        menu_bar_tk = Menu()
        self.root.config(menu=menu_bar_tk)

        for i in range(len(menu_bar["elements"])):
            i = str(i)
            element = menu_bar["elements"][i]
            match element["type"]:
                case "command":
                    if ":" in element["command"]:
                        command = element["command"].split(":")[0]
                        settings = element["command"].split(":")[1:]
                        func = partial(self.commands[command], settings)
                        menu_bar_tk.add_command(label=element["title"], command=func)
                    else:
                        func = partial(self.commands[element["command"]])
                        menu_bar_tk.add_command(label=element["title"], command=func)
                case "cascade":
                    new_menu = Menu(menu_bar_tk)
                    menu_bar_tk.add_cascade(menu=new_menu, label=element["title"])
                    for j in range(len(element["elements"])):
                        j = str(j)
                        nested_element = element["elements"][j]
                        match nested_element["type"]:
                            case "command":
                                if ":" in nested_element["command"]:
                                    command = nested_element["command"].split(":")[0]
                                    settings = nested_element["command"].split(":")[1:]
                                    func = partial(self.commands[command], settings)
                                    menu_bar_tk.add_command(label=nested_element["title"], command=func)
                                else:
                                    func = partial(self.commands[nested_element["command"]])
                                    new_menu.add_command(label=nested_element["title"], command=func)
                            case "separator":
                                new_menu.add_separator()

        self.logger.info("Loaded menu bar")

    def save_sounds(self):
        valid_file = False
        i = 0
        while not valid_file:
            name = f"sounds_save{i}.json"
            if not os.path.exists(fr"{pathlib.Path().resolve()}\{name}"):
                with open(name, "w") as save_file:
                    json.dump(self.sounds, save_file, indent=2)
                valid_file = True
            else:
                i += 1

    def load_sounds(self):
        pass

    def reload_settings(self):
        with open(self.menus["settings"]["file"]) as settings_file:
            self.settings = json.load(settings_file)

    def clear(self):
        for element in self.elements:
            try:
                element.tk.destroy()
            except:
                element.destroy()
        self.elements.clear()

    def close(self):
        if not self.settings["warn_before_close"] or messagebox.askyesno("Quit", "Do you want to quit?"):
            for element in self.elements:
                if isinstance(element, SoundButton):
                    if len(element.players) != 0:
                        element.stop_sound()
            self.root.destroy()
            self.running = False
            self.logger.info("Window closed")
