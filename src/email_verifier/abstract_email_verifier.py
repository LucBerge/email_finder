from abc import ABC, abstractmethod

class AbstractEmailVerifier(ABC):
    @abstractmethod
    def close(self):
        raise NotImplementedError("This method should be overridden in a subclass")

    @abstractmethod
    def verify_email(self, email: str) -> bool:
        raise NotImplementedError("This method should be overridden in a subclass")
