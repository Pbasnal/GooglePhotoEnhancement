import pickle
import json


class CacheService:
    def save(self, id, data, isJson=False):
        data = f"{{ \"id\": \"{id}\", \"data\": \"{data}\"    }}"
        print(data)

    def get(self):
        return ""
    
    def getForKey(self, key):
        return ""


class DictCache(CacheService, ):

    def __init__(self, cacheFilePath, serializer='pickle'):
        self.serializer = serializer
        
        with open(cacheFilePath, self.getOpenMode()) as _:
            # To create the file if it doesn't exists
            pass
        self.cacheFilePath = cacheFilePath
        self.cache = dict()

    def __enter__(self):
        with open(self.cacheFilePath, self.getReadMode()) as cache:
            cachedData = cache.read()
            if not cachedData.strip():
                return self
            self.cache =  self.deserializeData(cachedData)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.cacheFilePath, self.getWriteMode()) as cacheFile:
            serializedData = self.serializeData(self.cache)
            cacheFile.write(serializedData)

    def get(self):
        for cacheKey in self.cache.keys():
            yield cacheKey, self.cache[cacheKey]

    def getForKey(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def save(self, id, data):
        self.cache[id] = data
    
    def getOpenMode(self):
        return "ab+" if self.serializer == 'pickle' else "a+"
    def getReadMode(self):
        return "rb" if self.serializer == 'pickle' else "r"
    def getWriteMode(self):
        return "wb" if self.serializer == 'pickle' else "w"
    def serializeData(self, data):
        if self.serializer == 'pickle':
            return pickle.dumps(data)

        return json.dumps(data)

    def deserializeData(self, data):
        if self.serializer == 'pickle':
            return pickle.loads(data)

        return json.loads(data)
            


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
