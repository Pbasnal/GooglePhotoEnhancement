import pickle


cacheFilePath = "photoCache.json"
with open(cacheFilePath, "rb") as cache:
    cachedData = cache.read()
    if not cachedData.strip():
        exit()
    cache = pickle.loads(cachedData)

print(type(cache))
for id in cache.keys():
    print(cache[id].toString())