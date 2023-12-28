import logging

class LoggerMixin:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.FileHandler(
                filename=f"log/{self.__class__.__name__}.log", mode= "a"
                )
        
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
