import asyncio
import tkinter as tk
from tkinter import font as tkFont, messagebox
from button import Button
from sound import Sound
import logging


class Window:
    def __init__(self, logger: logging):
        self.buttons = []
        self.logger = logger
        self.running = True
        self.root = tk.Tk()
        self.root.geometry("640x360+320+180")
        self.root.title("Soundboard")
        self.root.bind("<Escape>", lambda e: self.close())
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.configure(background="#060812")
        self.small_fonts = tkFont.Font(family="Small Fonts", size=18, weight="bold")
        logger.info("Window created")

    def add_button(self, text: str, sound: Sound):
        button = Button(text, sound, self.logger)
        tk_button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                              activeforeground="white", fg="white", width=10, height=2,
                              borderwidth=0, border=0, font=self.small_fonts,
                              command=lambda: asyncio.run_coroutine_threadsafe(button.play_sound(),
                                                                               asyncio.get_running_loop()))
        button.associate_tk_button(tk_button)
        self.buttons.append(button)
        self.logger.debug(f"New button added with text '{button.text}' and sound '{button.sound.name}'")

    def update_buttons(self):
        for button in self.buttons:
            if not button.is_rendered:
                button.tk_button.grid(column=0, row=0)
                button.is_rendered = True

    def close(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.running = False
        self.logger.info("Window closed")
