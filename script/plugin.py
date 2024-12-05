from abc import ABC, abstractmethod


class PluginBase(ABC):
    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def pre_update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def post_update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def destroy(self) -> None:
        raise NotImplementedError
