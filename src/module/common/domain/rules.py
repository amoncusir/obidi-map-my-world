from src.module.common.domain.errors import DomainError


class Rule:

    def __call__(self): ...

    def polite(self) -> bool:
        try:
            self()
            return True
        except DomainError:
            return False
