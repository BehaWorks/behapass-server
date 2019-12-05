import numpy as np


class Result:
    data = None

    def __init__(self, data) -> None:
        self.data = data

    @property
    def average(self):
        return np.average(self.data)

    @property
    def median(self):
        return np.median(self.data)

    @property
    def std_dev(self):
        return np.std(self.data)

    @property
    def upper_q(self):
        return np.quantile(self.data, 0.75)

    @property
    def lower_q(self):
        return np.quantile(self.data, 0.25)

    @property
    def minimum(self):
        return np.min(self.data)

    @property
    def maximum(self):
        return np.max(self.data)

    @property
    def interquartile_range(self):
        return self.upper_q - self.lower_q
