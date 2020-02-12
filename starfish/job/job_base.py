
"""
   Job Base class
"""

from abc import ABC

class JobBase(ABC):
    """
        Create a Job object

        :param agent: agent object that created the listing.
        :type agent: :class:`.Agent` object to assign to this Listing
        :param str job_id: id of the job.
    """

    IsWorkingStatusList = [
        'scheduled',
        'running',
        'accepted'
    ]
    def __init__(self, job_id, status=None, outputs=None):
        """

        init the the Job Object Base with the agent instance

        :param int job_id: id of the job
        :param str status: status of the job
        :param dict outputs: dict or None for the outputs
        """
        self._job_id = job_id
        self._status = status
        self._outputs = outputs
        super().__init__()

    @property
    def is_finished(self):
        if self._status:
            return self._status not in JobBase.IsWorkingStatusList
        return False

    @property
    def job_id(self):
        """
        Return the job id

        :return: Job id
        :type: int
        """
        return self._job_id

    @property
    def status(self):
        """
        Return the status for this job

        :return: status
        :type: str
        """
        return self._status

    @property
    def outputs(self):
        """
        Return the ouptuts for this job

        :return: results
        :type: dict or None
        """
        return self._outputs

    def __str__(self):
        text = 'job:'
        if self._status:
            text += f'{self._status}'
        if self._outputs:
            text += f' = {self._outputs}'
        return text
