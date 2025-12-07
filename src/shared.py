import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S %Z')
logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, err):
        self.message = err
        super().__init__(err)