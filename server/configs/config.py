class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pankaj.basnal/repos/chromeetxbasics/server/images.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    NUMBER_OF_CHUNKS_OF_IMAGE_HASH = 4


class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pankaj.basnal/repos/chromeetxbasics/server/images.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    NUMBER_OF_CHUNKS_OF_IMAGE_HASH = 4


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/pankaj.basnal/repos/chromeetxbasics/server/images.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    NUMBER_OF_CHUNKS_OF_IMAGE_HASH = 4



