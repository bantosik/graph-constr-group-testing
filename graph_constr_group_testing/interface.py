from abc import abstractmethod, ABCMeta


class ExperimentStatistics(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.results = []

    @abstractmethod
    def verify(self, result, faulty_set):
        raise NotImplementedError()

    def set_result(self, solver, problem, statistics):
        self.results.append((solver, problem, statistics))
