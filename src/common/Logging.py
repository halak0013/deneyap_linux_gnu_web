import coloredlogs
import logging
from static.file_paths import Paths as p
""" logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# Coloredlogs konfigürasyonu
coloredlogs.install(level='DEBUG', fmt='%(asctime)s - %(levelname)s - %(message)s')

# Logger oluşturma
logger = logging.getLogger(__name__)

def example_function():
    logger.debug("Bu bir debug mesajıdır.")
    logger.info("Bu bir bilgi mesajıdır.")
    logger.warning("Bu bir uyarı mesajıdır.")
    logger.error("Bu bir hata mesajıdır.")
    logger.critical("Bu bir kritik hata mesajıdır.") """


class Log:
    def __init__(self):
        p.file_check(p.log_path)
        logging.basicConfig(filename=p.log_path + 'deneyap.log',
                            encoding='utf-8', level=logging.DEBUG)
        # Coloredlogs konfigürasyonu
        coloredlogs.install(
            level='DEBUG', fmt='%(asctime)s - %(levelname)s - %(message)s')
        # Logger oluşturma
        self.logger = logging.getLogger(__name__)

    def log(self, msg, level):
        if level == "d":  # debug
            self.logger.debug(msg)
        elif level == "i":  # info
            self.logger.info(msg)
        elif level == "w":  # warning
            self.logger.warning(msg)
        elif level == "e":  # error
            self.logger.error(msg)
        elif level == "c":  # critical
            self.logger.critical(msg)
