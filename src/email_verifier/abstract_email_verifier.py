from abc import ABC, abstractmethod

class AbstractEmailVerifier(ABC):
    def __init__(self, delay_between_threads: int = 5):
        super().__init__()
        self.delay_between_threads = delay_between_threads

    @abstractmethod
    def close(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    @abstractmethod
    def verify_email(self, email: str) -> bool:
        raise NotImplementedError("This method should be overridden in a subclass")
