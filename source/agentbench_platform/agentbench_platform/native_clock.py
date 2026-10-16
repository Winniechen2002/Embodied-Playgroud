"""Freeze the native 120 Hz period without accumulating float32 representation error."""
import math
import struct

PERIODS=(1/120,struct.unpack('f',struct.pack('f',1/120))[0])


def period_from_samples(first_step,first_time,last_step,last_time):
    if (type(first_step) is not int or type(last_step) is not int or last_step<=first_step
            or not all(math.isfinite(v) for v in (first_time,last_time))):
        raise ValueError('Invalid native clock reference')
    observed=(last_time-first_time)/(last_step-first_step)
    period=min(PERIODS,key=lambda value:abs(value-observed))
    if abs(period-observed)>1e-12:
        raise ValueError('Native clock period differs from declared 120 Hz')
    return period


def check_elapsed(time,origin,steps,period):
    if (period not in PERIODS or type(steps) is not int or steps<0
            or not all(math.isfinite(v) for v in (time,origin))
            or abs(time-origin-steps*period)>2e-6):
        raise ValueError('Native clock does not match fixed period and step count')
