from loguru import logger
from modules.image_hash import ImageModule
from configs.config_loader import loadConfigs, CONFIG


if __name__ == "__main__":

    loadConfigs()

    with ImageModule("modules/Knowledge tree.jpeg", CONFIG) as imageHash:
        print(f"hash of the image {imageHash.hash}")
        print(f"Hash string {imageHash.hashString} "
              + f"has length {len(imageHash.hashString)}")
        print(f"Hash in chunks format: "
              + f"{imageHash.hashChuncks()}")

    logger.debug(f"Second image")
    with ImageModule("modules/_DSC0299.NEF", CONFIG) as imageHash:
        print(f"hash of the image {imageHash.hash}")
        print(f"Hash string {imageHash.hashString} "
              + f"has length {len(imageHash.hashString)}")
        print(f"Hash in chunks format: "
              + f"{imageHash.hashChuncks()}")