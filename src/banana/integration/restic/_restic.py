import datetime
import os
import subprocess as sp
from pathlib import Path

import pydantic
from loguru import logger

import banana as bn


def default_config() -> Path:
    git_root: Path = bn.git.root()
    for config in [
        git_root / ".config" / "resticprofile.toml",
        git_root / "resticprofile.toml",
    ]:
        if config.exists():
            return config
    return git_root / ".config" / "resticprofile.toml"


class Restic(bn.Integration):
    config: Path = pydantic.Field(default_factory=default_config)
    dry_run: bool = False
    name: str | None = None
    time: datetime.datetime = pydantic.Field(default_factory=bn.start_time)

    def _end(self) -> None:
        if not self.config.exists():
            logger.warning("configuration file '{}' was not found", self.config)
            return
        args: list[str | os.PathLike[str]] = [
            "resticprofile",
            "--config",
            self.config,
            "backup",
        ]
        if self.name:
            args += ["--name", self.name]
        if self.dry_run:
            args.append("--dry-run")
        if self.time:
            args += ["--time", self.time.strftime("%Y-%m-%d %H:%M:%S")]
        sp.run(args, check=False)
