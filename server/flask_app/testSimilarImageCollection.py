from loguru import logger

class RenderableSimilarImages(object):
    def __init__(self):
        self.imageId: str

    def serialize(self):
        return {
            "imageId": self.imageId
        }


class RenderableParentImage(object):
    def __init__(self):
        self.imageId:  str
        self.similarImages = dict()

    def addSimilarImage(self, imageId):
        if imageId in self.similarImages.keys():
            return
        similarImage = RenderableSimilarImages()
        similarImage.imageId = imageId

        self.similarImages[imageId] = similarImage

    def serialize(self):
        return {
            "imageId": self.imageId,
            "similarImages": [image.serialize() for image in self.similarImages.values()]
        }


class SimilarImageCollection(object):

    def __init__(self):
        self.imageCollection = dict()
        self.imageIdSet = set()

    def add(self, imageId):
        if imageId in self.imageIdSet:
            return

        parentImage = RenderableParentImage()
        parentImage.imageId = imageId
        self.imageCollection[imageId] = parentImage
        self.imageIdSet.add(imageId)

    def addSimilarImage(self, imageId, similarImageId):
        if imageId not in self.imageIdSet:
            return
        if imageId == similarImageId:
            return
        self.imageCollection[imageId].addSimilarImage(similarImageId)

    def serialize(self):
        return [image.serialize()
                for image in self.imageCollection.values()
                if len(image.similarImages) > 0]

similarImages = [{
    "id": "d127c396-399a-4d92-827a-d74ff49d5176",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "9241dd2c-e519-4a30-ac48-a0d96339df3c",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "1b9e26c2-4073-46d1-8c91-e2402d988689",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "fdc818a0-9309-4646-b649-cfb26dd2821c",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "569c039b-09fb-4506-a813-06f4f50224ac",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "335f25c9-39f1-4362-bf37-156347fdeb4b",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "87659efc-22e5-4d35-8d52-99fbad2ee6be",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "6d50d2c7-8e85-42da-8e18-32d626c886e5",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "f155b62c-e68b-4679-b2e2-96a015ba42a9",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "ef33712b-0ce8-4714-8dc6-576faf7a43af",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "4a45dfd5-26b0-4d21-965d-e8b792a17243",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 99.0
},
{
    "id": "85cfcd8e-f42d-4f5a-9eb0-5411c3a4a41f",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "8755cfac-ddd1-4360-a77c-4416ed0df906",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "3b79a685-25e8-4169-a19f-b3323fc99898",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "8f86e88c-0d55-4169-9b31-78f4cd5354bb",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "1e7922de-c5c1-4a5d-8149-ab6a64635ac8",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "838a2942-cffd-4fba-8c9b-bfeec46d9282",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "cf816cf3-3e1f-4ba3-9b43-8c30e44019e2",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "32072371-bf81-461a-b7ce-5aaeb0fad25b",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "d3abaddf-65b2-47a7-9255-a89815ac8016",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarityScore": 99.0
},
{
    "id": "9e46f118-3b5d-4705-8845-8aa4e50eed15",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "284fe134-deff-4df6-89f8-b037e27f3b79",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "b649df9a-ee46-458c-8031-3305da42d6bf",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 99.0
},
{
    "id": "85cfcd8e-f42d-4f5a-9eb0-5411c3a4a41f",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "8755cfac-ddd1-4360-a77c-4416ed0df906",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "3b79a685-25e8-4169-a19f-b3323fc99898",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "6fb2eec3-438c-474a-8833-07eca4480a49",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarityScore": 99.0
},
{
    "id": "8f86e88c-0d55-4169-9b31-78f4cd5354bb",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "1e7922de-c5c1-4a5d-8149-ab6a64635ac8",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 100.0
},
{
    "id": "838a2942-cffd-4fba-8c9b-bfeec46d9282",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "cf816cf3-3e1f-4ba3-9b43-8c30e44019e2",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "32072371-bf81-461a-b7ce-5aaeb0fad25b",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "9e46f118-3b5d-4705-8845-8aa4e50eed15",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "284fe134-deff-4df6-89f8-b037e27f3b79",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 100.0
},
{
    "id": "d127c396-399a-4d92-827a-d74ff49d5176",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "9241dd2c-e519-4a30-ac48-a0d96339df3c",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "1b9e26c2-4073-46d1-8c91-e2402d988689",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "fdc818a0-9309-4646-b649-cfb26dd2821c",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "569c039b-09fb-4506-a813-06f4f50224ac",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarImageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarityScore": 100.0
},
{
    "id": "335f25c9-39f1-4362-bf37-156347fdeb4b",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "87659efc-22e5-4d35-8d52-99fbad2ee6be",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "6d50d2c7-8e85-42da-8e18-32d626c886e5",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "f155b62c-e68b-4679-b2e2-96a015ba42a9",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "ef33712b-0ce8-4714-8dc6-576faf7a43af",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSjkzXWQH8Q1LfYkeNRJg_IVqAmlO66VQssJZr7u6lGcqroOC8MrDhiRdJ9dCuw4lU7TWgPA9wMd1DVAkRgNMTMKtuG8A",
    "similarImageId": "AJ36JaQx23UBqd4Hx3zIF3yEQfP_7uQvzO691I2RGLSzLEweONkQjWmUaMJOvWk0mNeMFiuENKLOwkLaTn1RcWApmJ14jh1XnA",
    "similarityScore": 100.0
},
{
    "id": "b649df9a-ee46-458c-8031-3305da42d6bf",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarImageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarityScore": 99.0
},
{
    "id": "4a45dfd5-26b0-4d21-965d-e8b792a17243",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarImageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarityScore": 99.0
},
{
    "id": "6fb2eec3-438c-474a-8833-07eca4480a49",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA",
    "similarImageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarityScore": 99.0
},
{
    "id": "d3abaddf-65b2-47a7-9255-a89815ac8016",
    "userId": "116817479258426889709",
    "imageId": "AJ36JaSpcd3fk2IYEswTrzOT-aaPl-Ad_BvZwS2l8e7W9SO_sysvvj3Jax0-SfQk2sx7zP8sEiFwm7F80J4AKJgGRaP9Kgj5qg",
    "similarImageId": "AJ36JaSuAIS59w5q5ypsSZuL_5EM6-T1XbV9xEa_gPYHrGY_ZXDsgW-mH2nRbXHI3goQQuNX3LwKG-zvnJMwKHMftemPpm_Tpg",
    "similarityScore": 99.0
}]


def buildSimilarImageCollection(allSimilarImages):
    similarImageCollection = SimilarImageCollection()
    imagesHashSet = set()
    for similarImage in allSimilarImages:
        # logger.debug(similarImage)

        if similarImage["imageId"] == "AJ36JaSQDWrxpG3hPaI6g7ryYCgV49fHqSuNfx2itWhmQoT1Ysn5c90Pc7-eWcEmmHekc0baTJf5SZCF2ieXNriMkhl1hWc-TA":
            print("to break")
        keyImageId: str()
        similarImageId = str()
        if similarImage["imageId"] not in imagesHashSet \
                and similarImage["similarImageId"] not in imagesHashSet:
            imagesHashSet.add(similarImage["imageId"])
            keyImageId = similarImage["imageId"]
            similarImageId = similarImage["similarImageId"]

        elif similarImage["imageId"] in imagesHashSet:
            keyImageId = similarImage["imageId"]
            similarImageId = similarImage["similarImageId"]
        elif similarImage["similarImageId"] in imagesHashSet:
            keyImageId = similarImage["similarImageId"]
            similarImageId = similarImage["imageId"]
        
        similarImageCollection.add(keyImageId)
        similarImageCollection.addSimilarImage(keyImageId, similarImageId)
        # logger.debug(f"{keyImageId} - {similarImageId}")
    return similarImageCollection.serialize()


logger.debug(buildSimilarImageCollection(similarImages))

print(len(similarImages))