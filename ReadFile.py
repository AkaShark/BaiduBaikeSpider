class ReadFile(object):
    def __init__(self, filePath):
        self.filePath = filePath

    def read(self):
        with open(self.filePath, "rt", encoding="utf-8") as f:
            return f.readlines()
