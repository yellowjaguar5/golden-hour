import datetime
import logging
import math
import time

from astral import Astral
import pytz


logger = logging.getLogger()


ASTRAL_CITY_NAME_SEATTLE = 'seattle'

def get_timezone(city):
    return pytz.timezone(Astral()[city].timezone)


def get_today_sunset_time(city, today=None):
    if today is None:
        local_timezone = get_timezone(city)
        now = datetime.datetime.now(local_timezone)
        today = now.date()

    return Astral()[city].sun(today)['sunset']


def get_seconds_until(earlier_time, later_time):
    tdelta = later_time - earlier_time
    return tdelta.total_seconds()


def wait_for_sunset(minutes_before=0):
    city = ASTRAL_CITY_NAME_SEATTLE
    local_timezone = get_timezone(city)
    now = datetime.datetime.now(local_timezone)
    sunset_time = get_today_sunset_time(city, now.date())
    start_time = sunset_time - datetime.timedelta(minutes=minutes_before)
    if start_time < now:
        logger.error('ERROR: too late to start for today\'s sunset')
        exit()

    sleep_seconds = get_seconds_until(now, start_time)
    hours = math.floor(sleep_seconds // (60 * 60))
    minutes = math.floor((sleep_seconds // 60) % 60)
    seconds = math.floor(sleep_seconds % 60)
    logger.info(
        'Waiting {hours} {minutes} {seconds} to start, {minutes_before} minutes before sunset'.format(
            hours='{} hours'.format(hours) if hours > 0 else '',
            minutes='{} minutes'.format(minutes) if minutes > 0 else '',
            seconds='{} seconds'.format(seconds),
            minutes_before=minutes_before,
        )
    )
    time.sleep(sleep_seconds)
