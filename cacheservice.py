class CacheService:
    def save(self, id, data):
        data = f"{{ \"id\": \"{id}\", \"data\": \"{data}\"    }}"
        print(data)
    
    def get(self):
        return ""

class FileCacheService(CacheService):

    def __init__(self, cacheFilePath, mode):
        self.cacheFilePath = cacheFilePath
        self.mode = mode
        self.pos = 0

    def __enter__(self):
        self.cacheFile = open(self.cacheFilePath, self.mode)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cacheFile.close()

    def get(self):
        line = "0"
        while True:
            line = self.cacheFile.readline()
            if line == "":
                break
            yield line.rstrip()
    
    def resetReadHead(self):
        self.pos = 0

    def save(self, id, data, is_json=False):
        if is_json:
            data = f"{{ \"id\": \"{id}\", \"data\": {data}}}\n"
        else:
            data = f"{{ \"id\": \"{id}\", \"data\": \"{data}\"}}\n"

        self.cacheFile.write(data)
