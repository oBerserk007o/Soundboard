import tkinter as tk
from tkinter import font as tkFont
from button import Button
from sound import Sound


class Window:
    def __init__(self):
        self.buttons = []
        window = tk.Tk()
        window.geometry("640x360+320+180")
        window.title("Soundboard")
        window.bind("<Escape>", lambda e: e.widget.quit())
        window.configure(background='#060812')

        self.small_fonts = tkFont.Font(family='Small Fonts', size=18, weight='bold')

        window.mainloop()


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

