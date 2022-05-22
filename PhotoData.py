from json import JSONEncoder

class PhotoData(JSONEncoder):
    def __init__(self, id, name, height, width, enhanced: bool) -> None:
        self.id = id
        self.name = name
        self.height = height
        self.width = width
        self.enhanced = enhanced
        self.hash = None

    def photoHash(self):
        if not hasattr(self, "hash") or self.hash == None or self.hash == "":
            return None 
        return self.hash

    def toString(self):
        print(f"id: {self.id} name: {self.name} height: {self.height} width: {self.width} enhanced: {self.enhanced}")

    def setEnhanced(self, enhanced: bool):
        self.enhanced = enhanced

    def default(self, o):
        return o.__dict__