"""
Simple anomaly detection.

Rule:
- Value deviates > N standard deviations from rolling mean
"""

import statistics

STD_THRESHOLD = 3

def is_anomalous(buffer, value):
    if len(buffer) < 5:
        return False

    mean = statistics.mean(buffer)
    stdev = statistics.stdev(buffer)

    if stdev == 0:
        return False

    return abs(value - mean) > STD_THRESHOLD * stdev
