from abc import ABC

class Channel(ABC):
    def __init__(*args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def send_data(data: bytes, size: int):
        raise NotImplementedError

    def recv_data(size: int):
        raise NotImplementedError
