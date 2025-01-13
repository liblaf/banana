from collections.abc import Mapping
from typing import Any

import git


def auto_commit(
    message: str = "chore(exp): auto commit", *, footers: Mapping[str, Any] = {}
) -> None:
    repo: git.Repo = git.Repo(search_parent_directories=True)
    if not repo.is_dirty(untracked_files=True):
        return
    if footers:
        message += "\n\n"
        for key, value in footers.items():
            message += f"{key}: {value}\n"
    repo.git.add(all=True)
    repo.git.commit(message=message.strip())
