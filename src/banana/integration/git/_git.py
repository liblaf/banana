from collections.abc import Mapping
from typing import Any

import banana as bn


class Git(bn.Integration):
    auto_commit: bool = True
    auto_commit_message: str = "chore(exp): auto commit"
    auto_commit_footers: Mapping[str, Any] = {}

    def _start(self) -> None:
        if self.auto_commit:
            bn.git.auto_commit(
                message=self.auto_commit_message, footers=self.auto_commit_footers
            )
