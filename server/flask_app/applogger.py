from loguru import logger

logger.add("app_logs.log", rotation="5 MB", compression="zip")