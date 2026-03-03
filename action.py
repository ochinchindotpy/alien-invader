from abc import ABC, abstractmethod

class Action(ABC):
    def _validate(self, *args, **kwargs) -> bool:
        return True

    def _before(self, *args, **kwargs) -> None:
        pass

    def action(self, *args, **kwargs) -> None:
        if not self._validate(*args, **kwargs):
            return

        self._before(*args, **kwargs)
        self._do(*args, **kwargs)
        self._after(*args, **kwargs)

    @abstractmethod
    def _do(self, *args, **kwargs) -> None:
        pass

    def _after(self, *args, **kwargs) -> None:
        pass
    
    
    