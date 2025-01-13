import pydantic_settings as ps


class Integration(ps.BaseSettings):
    enabled: bool = True
    priority: int = 0

    def start(self) -> None:
        if not self.enabled:
            return
        self._start()

    def end(self) -> None:
        if not self.enabled:
            return
        self._end()

    def _start(self) -> None: ...
    def _end(self) -> None: ...
