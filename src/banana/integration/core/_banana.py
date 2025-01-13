import datetime

import avocado as ac
import pydantic

import banana as bn


class Banana(bn.Integration):
    start_time: datetime.datetime = pydantic.Field(default_factory=bn.start_time)
    comet: bn.Comet = pydantic.Field(default_factory=bn.Comet)
    git: bn.Git = pydantic.Field(default_factory=bn.Git)
    restic: bn.Restic = pydantic.Field(default_factory=bn.Restic)

    def __init__(self, **values) -> None:
        bn.assign_if_missing(values, "enabled", val=True)
        bn.assign_if_missing(values, "start_time", bn.start_time())
        comet: bn.Comet = bn.Comet.model_validate(values.get("comet", {}))
        bn.assign_if_missing(
            values, "git.auto_commit_footers.Experiment Name", comet.experiment_name
        )
        bn.assign_if_missing(
            values, "git.auto_commit_footers.Experiment URL", comet.experiment_url
        )
        bn.assign_if_missing(values, "restic.time", values["start_time"])
        super().__init__(**values)

    def _start(self) -> None:
        # TODO: reorder based on priority
        ac.init_logging()
        self.git.start()
        self.comet.start()
        self.restic.start()

    def _end(self) -> None:
        self.restic.end()
        self.comet.end()
        self.git.end()
