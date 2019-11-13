class Metric:
    """
    Base class for metrics. Subclass this class for individual metrics.
    """

    def calculate(self, data: list) -> float:
        raise AttributeError('This is a base class. Subclass this class for individual metrics.')
