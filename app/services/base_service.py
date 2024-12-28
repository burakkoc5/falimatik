from abc import ABC, abstractmethod
from typing import Any

class BaseService(ABC):
    """
    Abstract base class for all services.
    Defines the common interface that all services must implement.
    """
    
    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method that must be implemented by all services.
        This is the main method that will be called to perform the service's operation.
        """
        pass 