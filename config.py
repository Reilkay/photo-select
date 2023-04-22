import os
import json


class Config:
    _instance = None
    __first_init = False

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if not self.__first_init:
            self.__first_init = True
            self.__path_name = './config.json'
            if not os.path.isfile(self.__path_name):
                self.init_config_file()
            self.__config = self.get_from_file()

    def get_from_file(self) -> dict:
        with open(self.__path_name, encoding='utf-8') as f:
            config = json.load(f)
            return config

    def update(self, config: dict) -> None:
        with open(self.__path_name, 'w') as f:
            json.dump(config, f)
        self.__config = self.get_from_file()

    def get(self) -> dict:
        return self.__config

    def init_config_file(self):
        init_data = {
            "default_ext": ["bmp", "gif", "jpg", "tif", "psd", "png", "webp"]
        }
        with open(self.__path_name, 'w') as f:
            json.dump(init_data, f, indent=4)