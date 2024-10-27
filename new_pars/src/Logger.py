import logging
import logging.config
import sys
from abc import ABC, abstractmethod


class BaseLogger(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_logger(self):
        pass


class ResponseLogger(BaseLogger):

    def __init__(self):
        self.log = None
        self.default_config = {
                                'version': 1,
                                'formatters': {
                                    'standard': {
                                        'format': '%(asctime)s %(levelname)s: %(message)s',
                                        'datefmt': '%Y-%m-%d - %H:%M:%S'},
                                },
                                'handlers': {
                                    'console':  {'class': 'logging.StreamHandler',
                                                 'formatter': "standard",
                                                 'level': 'DEBUG',
                                                 'stream': sys.stdout},
                                    'file':     {'class': 'logging.FileHandler',
                                                 'formatter': "standard",
                                                 'level': 'DEBUG',
                                                 'filename': 'live_detector.log',
                                                             'mode': 'w'}
                                },
                                'loggers': {
                                    __name__:   {'level': 'INFO',
                                                 'handlers': ['console',
                                                              'file'],
                                                 'propagate': False},
                                }
                            }

    def create_logger(self):
        logging.config.dictConfig(self.default_config)
        self.log = logging.getLogger(__name__)
