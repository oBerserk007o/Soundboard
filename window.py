import asyncio
import tkinter as tk
from tkinter import font as tkFont
from button import Button
from sound import Sound


# Massive thanks to Terry Jan Reedy for providing a solution to running tkinter with asyncio
# https://stackoverflow.com/questions/47895765/use-asyncio-and-tkinter-or-another-gui-lib-together-without-freezing-the-gui (first answer)
class Window(tk.Tk):
    def __init__(self, loop, interval=1 / 120):
        self.buttons = []
        super().__init__()
        window = super()
        window.geometry("640x360+320+180")
        window.title("Soundboard")
        window.bind("<Escape>", lambda e: e.widget.quit())
        window.configure(background='#060812')
        self.small_fonts = tkFont.Font(family='Small Fonts', size=18, weight='bold')

        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        # self.tasks.append(loop.create_task(self.add_button()))
        self.tasks.append(loop.create_task(self.updater(interval)))

        # window.mainloop()

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

    async def add_button(self, text: str, sound: Sound):
        button = Button(text, sound)
        tk_button = tk.Button(text=text, background="#141f52", activebackground="#0f163b",
                  activeforeground="white", fg="white", width=10, height=2,
                  borderwidth=0, border=0, font=self.small_fonts, command=await button.play_sound())
        button.associate_tk_button(tk_button)
        self.buttons.append(button)

    def update_buttons(self):
        for button in self.buttons:
            if not button.is_rendered:
                button.tk_button.grid(column=0, row=0)
                button.is_rendered = True
