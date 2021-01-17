import psutil
import requests
import logging
import os

UNITS_MAPPING = [
    (1 << 50, 'P'),
    (1 << 40, 'T'),
    (1 << 30, 'G'),
    (1 << 20, 'M'),
    (1 << 10, 'K'),
    (1, ('B', ' bytes')),
]

def byte_to_human_read(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def human_read_to_byte(size):
    size_name = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")
    num, unit = int(size[0:-1]), size[-1]
    # index in list of sizes determines power to raise it to
    idx = size_name.index(unit)
    # ** is the "exponent" operator - you can use it instead of math.pow()
    factor = 1024 ** idx
    return num * factor

def get_free_space(directory="/"):
    ''' checks the disk usage '''
    hdd = psutil.disk_usage(directory)
    logging.debug("Free space is: %s", str(hdd.free))
    return hdd.free

def healthcheck_failure():
    if os.environ["HEALTHCHECK_URL"]:
        requests.get(os.environ["HEALTHCHECK_URL"] + '/fail')

def healthcheck_ok():
    if os.environ["HEALTHCHECK_URL"]:
        requests.get(os.environ["HEALTHCHECK_URL"] + '/fail')