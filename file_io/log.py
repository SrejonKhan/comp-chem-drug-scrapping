
class Logger:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def write_log(self, txt):
        with open(self.filepath, 'a') as f:
            f.write(f"{txt}\n")
            print(txt)