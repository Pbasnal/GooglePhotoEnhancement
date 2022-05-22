import subprocess
import shutil
from subprocess import PIPE
from gphotospy.media import *

PATH_PHOTO_TO_ENHANCE = "DPED/dped/iphone/test_data/full_size_test_images/"

def enhancePhotosInFolder(folderPath):

    print(folderPath)
    print(os.listdir(folderPath))

    fileNames = [f for f in os.listdir(folderPath)
                 if os.path.isfile(os.path.join(folderPath, f))]
    print(fileNames)

    for fileName in fileNames:
        if fileName == ".DS_Store":
            continue
        filePath = os.path.join(folderPath, fileName)
        shutil.move(filePath, PATH_PHOTO_TO_ENHANCE)
        
        print(f"\n\n Enhancing photo {fileName}")
        command = "python runmodel.py model=iphone_orig test_subset=full".split()
        process = subprocess.run(command, stdout=PIPE, stderr=PIPE)

        if process.returncode != 0:
            print(f"runmodel stdout> {process.stdout}")
            print(f"runmodel stderr> {process.stderr}")
            print(f"runmodel returncode> {process.returncode}")

        filePath = os.path.join(folderPath, f"processed/{fileName}")
        shutil.move(os.path.join(PATH_PHOTO_TO_ENHANCE, fileName), filePath)


def main():

    enhancePhotosInFolder("photos")


if __name__ == "__main__":
    main()