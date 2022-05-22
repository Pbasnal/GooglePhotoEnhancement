import os
from loguru import logger
from configs.config import ProdConfig, DevConfig, TestingConfig

def loadConfigs():
    try:
        env = os.environ['FLASK_ENV']
    except Exception as e:
        logger.warning(e)
        env = 'Dev'

    print(env)
    if env == "Prod":
        print("setting prod")
        CONFIG = ProdConfig()
    elif env == "Testing":
        print("setting test")
        CONFIG = TestingConfig()
    else:
        print("setting dev")
        CONFIG = DevConfig()

    return CONFIG