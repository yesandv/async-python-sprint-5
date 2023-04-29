import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(funcName)s:[%(asctime)s]:%(message)s",
    handlers=[
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)
