
"""
Operation class
"""
from abc import ABC, abstractmethod


class OperationBase(ABC):

    def __init__(self, agent,did):
        """init the the Operation with the agent instance"""
        self._agent = agent
        self._did=did
        super().__init__()

    @abstractmethod
    def invoke(self, **kwargs):
        """

        """
        pass
