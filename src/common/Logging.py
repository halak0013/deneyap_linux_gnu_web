import coloredlogs
import logging
from static.file_paths import Paths as p
import datetime


class Log:
    def __init__(self):
        p.file_check(p.log_path)
        current_time = datetime.datetime.now().strftime("%y-%m-%d_%H:%M")
        fmt='%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=p.log_path + f'{current_time}_deneyap.log',
                            encoding='utf-8', level=logging.DEBUG,format=fmt)
        # Coloredlogs konfigürasyonu
        coloredlogs.install(
            level='DEBUG', fmt=fmt)
        # Logger oluşturma
        self.logger = logging.getLogger(__name__)

    def log(self, msg, level="i"):
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
