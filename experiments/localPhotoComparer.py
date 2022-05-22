from PIL import Image
import imagehash
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

PHOTO_FOLDER = "./photos/processed/"

class PhotoInfo:
    def __init__(self, photoName):
        self.photoName = photoName
        self.photo = getImage(photoName)

class ButtonClickProcessor(object):
    def __init__(self, axes, label):
        self.button = Button(axes, label)
        self.button.on_clicked(self.process)
        self.photoPath = "empty"

    def process(self, event):
        print(self.button.label, self.photoPath)
        if os.path.exists(self.photoPath):
            os.remove(self.photoPath)
        loadNextImages(self.dataStore)

    def setPhoto(self, photoPath):
        self.photoPath = getPhotoPath(photoPath)

    def setDataStore(self, dataStore):
        self.dataStore = dataStore


def getPhotoPath(photo_name):
    return PHOTO_FOLDER + photo_name


def getImage(photo_name):
    photo_path = getPhotoPath(photo_name)
    if os.path.exists(photo_path) == False:
        return None
    return Image.open(getPhotoPath(photo_name))

def imgHash(photo_name):
    image = getImage(photo_name)
    if image == None:
        return None
    return imagehash.average_hash(getImage(photo_name))

def createImages(axes):
    nx = 50
    ny = 50

    data = np.zeros((nx, ny))

    return axes[0].imshow(data), axes[1].imshow(data)

def displayImages(axes, imgL, imgR, diffPercentage):
    axes[0].imshow(imgL.photo)
    axes[0].set_title(imgL.photoName)
    axes[0].axis('off')

    axes[1].imshow(imgR.photo)
    axes[1].set_title(f"{imgL.photoName} {diffPercentage}")
    axes[1].axis('off')


def createFigure():
    f, axarr = plt.subplots(1, 2)
    f.subplots_adjust(wspace=0, hspace=0)
    f.subplots_adjust(left=0, bottom=0, right=1, top=1)

    return f, axarr


def createButtons():
    # xposition, yposition, width, height
    photo1_dlt_button = plt.axes([0.15, 0.1, 0.08, 0.05])
    photo2_dlt_button = plt.axes([0.75, 0.1, 0.08, 0.05])

    dlt1_button = ButtonClickProcessor(photo1_dlt_button, "Delete 1")
    dlt2_button = ButtonClickProcessor(photo2_dlt_button, "Delete 2")

    return dlt1_button, dlt2_button


class DataStore:
    def __init__(self, imgHashes, fig, axarr, btn1, btn2) -> None:
        self.imgHashes = imgHashes
        self.fig = fig
        self.axarr = axarr
        self.btn1 = btn1
        self.btn2 = btn2
        self.imageIter = getSimilarPhotos(imgHashes)    

    def setImages(self, im1, im2):
        self.im1 = im1
        self. im2 = im2

def createDataStore():

    imgHashes = getImageHashes()

    f, axarr = createFigure()
    dlt1_button, dlt2_button = createButtons()

    im1, im2 = createImages(axarr)

    dataStore = DataStore(imgHashes, f, axarr, dlt1_button, dlt2_button)

    dataStore.setImages(im1, im2)

    dlt1_button.setDataStore(dataStore)
    dlt2_button.setDataStore(dataStore)

    return dataStore

def loadNextImages(dataStore):
    photo1, photo2, diffPercentage = next(dataStore.imageIter)

    if photo1 == None:
        return

    dataStore.btn1.setPhoto(photo1.photoName)
    dataStore.btn2.setPhoto(photo2.photoName)

    # displayImages(dataStore.axarr, dataStore.im1, dataStore.im2 , diffPercentage)
    dataStore.im1.set_data(photo1.photo)
    dataStore.axarr[0].set_title(photo1.photoName)
    dataStore.axarr[0].axis('off')

    dataStore.im2.set_data(photo2.photo)
    dataStore.axarr[1].set_title(f"{photo2.photoName} {diffPercentage}")
    dataStore.axarr[1].axis('off')
    

def getImageHashes():
    test_photos = [f for f in os.listdir(
        PHOTO_FOLDER) if os.path.isfile(PHOTO_FOLDER + f) and f != ".DS_Store"]
    if len(test_photos) <= 0:
        return None

    test_photos.sort()
    imgHashes = {p: imgHash(p) for p in test_photos}

    return imgHashes

def getSimilarPhotos(imgHashes):
    for photo1 in imgHashes:
        photoHash1 = imgHashes[photo1]

        photo1_path = getPhotoPath(photo1)
        if os.path.exists(photo1_path) == False:
            continue

        for photo2 in imgHashes:
            photoHash2 = imgHashes[photo2]

            diff = photoHash2 - photoHash1
            diffPercentage = (10 - diff) / 10 * 100
            if diff > 10 or photo1 == photo2:
                continue
            photo2_path = getPhotoPath(photo2)
            if os.path.exists(photo2_path) == False:
                continue

            yield PhotoInfo(photo1), PhotoInfo(photo2), diffPercentage
    yield None, None, None


def main():
    dataStore = createDataStore()
    plt.show()
    loadNextImages(dataStore)
    return
    test_photos = [f for f in os.listdir(
        PHOTO_FOLDER) if os.path.isfile(PHOTO_FOLDER + f) and f != ".DS_Store"]
    if len(test_photos) <= 0:
        return

    test_photos.sort()
    imgHashes = {p: imgHash(p) for p in test_photos}

    # print(imgHashes)
    for photo1 in imgHashes:
        photoHash1 = imgHashes[photo1]

        for photo2 in imgHashes:
            photoHash2 = imgHashes[photo2]

            diff = photoHash2 - photoHash1
            if diff > 10 or photo1 == photo2:
                continue

            diffPercentage = (10 - diff) / 10 * 100
            print(
                f"{photo1}({photoHash1}) - {photo2}({photoHash2}) => {diffPercentage}%")

            imgLr = getImage(photo1)
            imgRr = getImage(photo2)

            f, axarr = plt.subplots(1, 2)
            f.subplots_adjust(wspace=0, hspace=0)
            f.subplots_adjust(left=0, bottom=0, right=1, top=1)

            axarr[0].imshow(imgLr)
            axarr[0].axis('off')

            axarr[1].imshow(imgRr)
            axarr[1].set_title(f"Similarity = {diffPercentage}%")
            axarr[1].axis('off')

            # xposition, yposition, width, height
            photo1_dlt_button = plt.axes([0.15, 0.1, 0.08, 0.05])
            photo2_dlt_button = plt.axes([0.75, 0.1, 0.08, 0.05])

            # properties of the button
            dlt1_button = Button(photo1_dlt_button, 'Delete',
                                 color='white', hovercolor='grey')
            dlt2_button = Button(photo2_dlt_button, 'Delete',
                                 color='white', hovercolor='grey')

            def deletePhoto1(val):
                os.remove(getPhotoPath(photo1))

            def deletePhoto2(val):
                os.remove(getPhotoPath(photo2))

            # triggering event is the clicking
            dlt1_button.on_clicked(deletePhoto1)
            dlt2_button.on_clicked(deletePhoto2)

            plt.show()


if __name__ == "__main__":
    main()
