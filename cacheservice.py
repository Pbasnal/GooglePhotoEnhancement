import pickle


class CacheService:
    def save(self, id, data, isJson=False):
        data = f"{{ \"id\": \"{id}\", \"data\": \"{data}\"    }}"
        print(data)

    def get(self):
        return ""


class DictCache(CacheService):
    def __init__(self, cacheFilePath):
        with open(cacheFilePath, "ab+") as _:
            # To create the file if it doesn't exists
            pass
        self.cacheFilePath = cacheFilePath
        self.cache = dict()

    def __enter__(self):
        with open(self.cacheFilePath, "rb") as cache:
            cachedData = cache.read()
            if not cachedData.strip():
                return self
            self.cache = pickle.loads(cachedData)
            # print(self.cache)
            # self.cache = json.loads(cachedData)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.cacheFilePath, "wb") as cacheFile:
            serializedData = pickle.dumps(self.cache)
            cacheFile.write(serializedData)

    def get(self):
        for cacheKey in self.cache.keys():
            yield cacheKey, self.cache[cacheKey]

    def save(self, id, data, is_json=False):
        self.cache[id] = data

class FileCacheService(CacheService):

    def __init__(self, cacheFilePath, mode):
        with open(cacheFilePath, "w+") as _:
            # To create the file if it doesn't exists
            pass
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
            self.cacheFile.write(data)
        else:
            self.cacheFile.write(pickle.dumps(data))
