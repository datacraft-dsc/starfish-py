"""

    Job Module

"""


class JobStatus():
    SCHEDULE = 'scheduled'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


JobStatusWorking = [
    JobStatus.SCHEDULE,
    JobStatus.RUNNING,
]

JobStatusDone = [
    JobStatus.SUCCEEDED,
    JobStatus.FAILED,
    JobStatus.CANCELLED
]

JobStatusFailed = [
    JobStatus.FAILED,
    JobStatus.CANCELLED
]

from starfish.job.job import Job                               # noqa: F401 E402
