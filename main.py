from prometheus_client import start_http_server, Summary, Gauge, Histogram
import random
import time
import math

# Create Prometheus metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
LEVEL = Gauge('current_sea_level', 'Height of Tide at Time (Seconds)')
STATUS = Gauge('current_tide_direction', 'Status of tide (Incoming Outgoing High Low)')

buckets = (0, 0.05, 0.1, .15, .2, .25, .3, .35, .4, .45, .5, .55, math.inf)
REQUEST_HIST = Histogram('latency_histogram', 'Latency Histogram', buckets=buckets)


@REQUEST_TIME.time()
def measure_sea_level(t):
    """A toy function that 'measures sea level' with some latency."""

    t = t/10

    time.sleep(max(0, random.normalvariate(0.3, 0.1)))
    level = 4 * math.asin(math.sin(t / 2)) * math.cos(t - 2)
    df = dfdt(t)

    # {rising: 1, falling: -1, high: 2, low: -2}
    if abs(df) > 0.25:
        status = math.copysign(1, df)
    elif dfdt(t - 1) > 0:
        status = 2
    else:
        status = -2

    return level, status


def dfdt(t):
    return 2 * (math.cos(t / 2) * math.cos(t - 2)) / \
           (2 * math.sqrt(1 - math.sin(t / 2) ** 2)) - \
           4 * math.asin(math.sin(t / 2)) * math.sin(t - 2)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.

    while True:
        with REQUEST_HIST.time():
            tide_level, tide_status = measure_sea_level(time.time())
            LEVEL.set(tide_level)
            STATUS.set(tide_status)

            if tide_level > 4 and tide_status == 2:
                print('Extreme High Tide')
