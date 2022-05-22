import os
import imagehash

from PIL import Image

class ImageModule:
    def __init__(self, imagePath, config):
        self.imagePath = imagePath
        self.hashString: str
        self.numberOfHashChunks = config.NUMBER_OF_CHUNKS_OF_IMAGE_HASH
        

    def __enter__(self):
        if not os.path.exists(self.imagePath):
            raise Exception(f"Image {self.imagePath} doesn't exists")
        
        self.image = Image.open(self.imagePath)
        self.calculateImageHash()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.image.close()
        

    def calculateImageHash(self):
        self.hash = imagehash.average_hash(self.image)
        self.hashString = ImageModule.hashToString(self.hash.hash)

    def hashToString(imgHash):
        return ''.join(str(b) for b in 1 * imgHash.flatten())

    def hashChuncks(self):
        lengthOfHash = len(self.hashString)
        chunkSize = lengthOfHash // self.numberOfHashChunks
        return [self.hashString[i : i + chunkSize]
                for i in range(0, lengthOfHash, chunkSize)]

