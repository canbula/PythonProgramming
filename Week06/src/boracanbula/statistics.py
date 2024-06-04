import random


def simple_random_sampling(data, n, replacement=False):
    """Simple Random Sampling with or without replacement."""
    if replacement:
        return [random.choice(data) for _ in range(n)]
    return random.sample(data, min(n, len(data)))


def stratified_sampling(data, n, strata):
    """Strafied Sampling with proportional representation of strata."""
    sample = []
    for key in strata:
        sample += random.sample(data[key], min(n // len(strata), len(data[key])))
    return sample


def cluster_sampling(data, n, clusters):
    """Cluster Sampling with random selection of clusters."""
    picked_clusters = random.sample(clusters, min(n, len(clusters)))
    sample = []
    for cluster in picked_clusters:
        sample += data[cluster]
    sample = list(set(sample))
    return sample


def systematic_sampling(data, n):
    """Systematic Sampling."""
    sample = []
    for i in range(0, len(data), n):
        sample.append(data[i])
    return sample


def mean(x: list) -> float:
    """Calculate the mean of a list of numbers."""
    return sum(x) / len(x)


def median(data):
    """Find the median of a list of numbers."""
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[int((n + 1) / 2) - 1]
    return (data[(n // 2) - 1] + data[((n // 2) + 1) - 1]) / 2


def mode(data):
    """Find the mode(s) of a list of numbers."""
    counts = {}
    for value in data:
        if value in counts:
            counts[value] += 1
        else:
            counts[value] = 1
    max_count = max(counts.values())
    mode = [value for value, count in counts.items() if count == max_count]
    return mode


def range(x):
    """Calculate the range of x."""
    return max(x) - min(x)


def variance(x):
    """Calculate the variance of x."""
    mean_ = mean(x)
    return sum((xi - mean_) ** 2 for xi in x) / (len(x) - 1)


def standard_deviation(x):
    """Calculate the standard deviation of x."""
    return variance(x) ** 0.5


def coefficient_of_variation(x):
    """Calculate the coefficient of variation of x."""
    return standard_deviation(x) / mean(x)
