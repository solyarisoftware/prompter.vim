#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime


def duration_min_sec(seconds):
    m = seconds // 60
    s = seconds % 60
    return '{:02d}:{:02d}'.format(m, s)


def start_timer():
    return datetime.datetime.now()


def stop_timer_msecs(start_time):
    ''' calculate elapsed time in milliseconds '''

    stop_time = datetime.datetime.now()
    delta = stop_time - start_time
    duration_msecs = int(delta.total_seconds() * 1000)
    return duration_msecs


def stop_timer_secs(start_time):
    ''' calculate elapsed time in seconds '''

    stop_time = datetime.datetime.now()
    delta = stop_time - start_time
    duration_secs = int(delta.total_seconds())
    return duration_secs


def stop_timer_mins(start_time):
    ''' calculate elapsed time in minutes:seconds '''

    return duration_min_sec(stop_timer_secs(start_time))


def stop_timer(start_time):
    ''' calculate elapsed time in seconds (milliseconds '''

    stop_time = datetime.datetime.now()
    delta = stop_time - start_time
    milliseconds = int(delta.total_seconds() * 1000)
    seconds = round(milliseconds / 1000, 1)

    return f"{milliseconds }ms ({seconds}s)", milliseconds


if __name__ == "__main__":

    start = start_timer()

    time.sleep(2)

    # print(stop_timer_msecs(start))
    # print(stop_timer_secs(start))
    # print(stop_timer_mins(start))
    print(stop_timer(start))
