from mutagen.mp3 import MP3

class Sound:
    def __init__(self, filename: str):
        self.name = filename
        self.length = MP3(fr"C:\Users\Dorno\Desktop\Coding projects\Python\Soundboard\sounds\{self.name}").info.length
