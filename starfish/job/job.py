"""

   Job class


"""

from typing import (
    Any,
    Generic
)

from starfish.job import (
    JobStatusDone,
    JobStatusWorking
)

from starfish.types import TJob


class Job(Generic[TJob]):
    """
        Create a Job object

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param str job_id: id of the job.
    """
    def __init__(self, job_id: str, status: str = None, outputs: Any = None, error: Any = None) -> None:
        """

        init the the Job Object Base with the agent instance

        :param int job_id: id of the job
        :param str status: status of the job
        :param dict outputs: dict or None for the outputs
        """
        self._job_id = job_id
        self._status = status
        self._outputs = outputs
        self._error = error
        super().__init__()

    @staticmethod
    def create_from_result(job_id: str, result: dict) -> TJob:
        if not isinstance(result, dict):
            raise TypeError('job result is not a dict')
        return Job(
            job_id,
            status=result.get('status', None),
            outputs=result.get('outputs', None),
            error=result.get('errror', None)
        )

    @property
    def is_done(self) -> bool:
        if self._status:
            return self._status in JobStatusDone
        return False

    @property
    def is_working(self) -> bool:
        if self._status:
            return self._status in JobStatusWorking
        return False

    @property
    def job_id(self) -> str:
        """
        Return the job id

        :return: Job id
        :type: int
        """
        return self._job_id

    @property
    def status(self) -> str:
        """
        Return the status for this job

        :return: status
        :type: str
        """
        return self._status

    @property
    def outputs(self) -> Any:
        """
        Return the ouptuts for this job

        :return: results
        :type: dict or None
        """
        return self._outputs

    @property
    def error(self) -> Any:
        """
        Return the ouptuts for this job

        :return: results
        :type: dict or None
        """
        return self._error

    @property
    def result(self):
        """

        Return the job result of a completed job. If the job is not completed then
        the 'status' will contain the current job status.

        :param str job_id: Job id of the job to get the status.
        :return: Job status
        :type: str

        """
        result = {
            'status': self._status,
        }
        if self._outputs:
            result['outputs'] = self._outputs
        if self._error:
            result['error'] = self._error
        return result

    def __str__(self) -> str:
        text = 'job:'
        if self._status:
            text += f'{self._status}'
        if self._outputs:
            text += f' = {self._outputs}'
        return text
