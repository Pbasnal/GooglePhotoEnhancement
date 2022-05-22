class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    NUMBER_OF_CHUNKS_OF_IMAGE_HASH = 8
    IMAGE_DOWNLOAD_FOLDER = "../flask_app/frontend/static/img/"
    BATCH_SIZE_FOR_SIMILAR_PHOTO_PROCESS = 100
    BATCH_SIZE_FOR_ALBUM_PROCESS = 100

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pankaj.basnal/repos/chromeetxbasics/server/images.db'

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pankaj.basnal/repos/chromeetxbasics/server/images.db'


