import logging
from .utility import *

class Logger:

    def __init__(self):
        self.filename = get_logfile_name()
        
        to_terminal = logging.StreamHandler()
        to_file = logging.FileHandler(filename=self.filename)
        to_terminal.setFormatter(get_formatter())
        to_file.setFormatter(get_formatter())
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[to_terminal, to_file]
        )
        

    def debug(self, message):
        logging.debug(message)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)
        
    def critical(self, message):
        logging.critical(message)