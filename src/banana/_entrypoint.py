import sys
from pathlib import Path

import banana as bn


def entrypoint() -> Path:
    git_root: Path = bn.git.root().absolute()
    entrypoint: Path = Path(sys.argv[0]).absolute()
    if entrypoint.is_relative_to(git_root):
        return entrypoint.relative_to(git_root)
    return entrypoint
