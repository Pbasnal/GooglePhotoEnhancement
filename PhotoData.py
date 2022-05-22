from json import JSONEncoder

class PhotoData(JSONEncoder):
    def __init__(self, id, name, height, width, enhanced: bool) -> None:
        self.id = id
        self.name = name
        self.height = height
        self.width = width
        self.enhanced = enhanced

    def toString(self):
        print(f"id: {self.id} name: {self.name} height: {self.height} width: {self.width} enhanced: {self.enhanced}")

    def setEnhanced(self, enhanced: bool):
        self.enhanced = enhanced

    def default(self, o):
        return o.__dict__