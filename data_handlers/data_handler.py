from abc import ABC, abstractmethod
class DataHandler(ABC):
    @abstractmethod
    @staticmethod
    def init(api_key: str)->"DataHandler":
        pass

    @abstractmethod
    def handle_data(self, data: object)->object:
        pass