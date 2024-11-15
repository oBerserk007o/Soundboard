from functools import partial

class Shwoop:
    def __init__(self):
        self.commands = {
            "1": lambda a: print(a[0], a[1])
        }

    def exec(self, settings):
        func = partial(self.commands["1"], settings)
        func()

shwoop = Shwoop()
args = ["wo", "ow"]

run_pls = partial(commands["1"], args)
commands["1"](args)
print(callable(commands["1"]))
