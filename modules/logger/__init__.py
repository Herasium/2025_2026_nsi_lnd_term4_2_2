from modules.data import data
import time
import datetime


class Logger():

    def __init__(self,name):
        self.name = name

        self.levels = [
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR"
        ]

        self.colors = [
            "\033[0m",
            "\033[36m",
            "\033[92m",
            "\033[33m",
            "\033[31m",
        ]

        self.history = []

    def header(self,level):
        timstamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")
        header = f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timstamp} | {self.levels[level]} | "
        return header

    def debug(self,message):
        data = f"{self.header(0)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def print(self,message):
        data = f"{self.header(1)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def success(self,message):
        data = f"{self.header(2)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def warning(self,message):
        data = f"{self.header(3)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)
    
    def error(self,message):
        data = f"{self.header(4)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)