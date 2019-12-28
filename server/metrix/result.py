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

    def average_chunk(self, chunks=1, chunk=0):
        return np.average(
            self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1])

    def median_chunk(self, chunks=1, chunk=0):
        return np.median(self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1])

    def std_dev_chunk(self, chunks=1, chunk=0):
        return np.std(self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1])

    def upper_q_chunk(self, chunks=1, chunk=0):
        return np.quantile(
            self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1], 0.75)

    def lower_q_chunk(self, chunks=1, chunk=0):
        return np.quantile(
            self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1], 0.25)

    def minimum_chunk(self, chunks=1, chunk=0):
        return np.min(self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1])

    def maximum_chunk(self, chunks=1, chunk=0):
        return np.max(self.data[chunk * int(len(self.data) / chunks):(chunk + 1) * int(len(self.data) / chunks) - 1])

    def interquartile_range_chunk(self, chunks=1, chunk=0):
        return self.upper_q_chunk(chunks, chunk) - self.lower_q_chunk(chunks, chunk)
