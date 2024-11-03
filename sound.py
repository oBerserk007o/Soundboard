from mutagen.mp3 import MP3
import pathlib


class Sound:
    def __init__(self, filename: str):
        self.name = filename
        self.length = MP3(fr"{pathlib.Path().resolve()}\Sounds\{self.name}").info.length
