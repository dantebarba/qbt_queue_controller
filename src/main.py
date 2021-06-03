import qbt_api
import nzb_api
import helpers
import logging
import os
import sys
import scheduler

space_threshold = 1073741824
buffer = 2048

def start():
    configure(os.environ["LOG_LEVEL"])
    if "BUILD_VERSION" in os.environ.keys():
        logging.info("BUILD VERSION IS %s", os.environ["BUILD_VERSION"])

    if not "INTERVAL" in os.environ.keys():
        raise AssertionError("Cron expression is not set")

    logging.debug(
        "Scheduler is enabled. Task will be scheduled to run at %s", os.environ["INTERVAL"])

    scheduler.configure(os.environ["INTERVAL"], pause_verify_nzb)
    scheduler.start()


def configure(log_level='INFO'):
    root = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    root.setLevel(eval("logging."+log_level))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(eval("logging."+log_level))

    handler.setFormatter(formatter)
    root.addHandler(handler)

    if "LOG_FILE" in os.environ.keys():
        fh = logging.FileHandler(os.environ["LOG_FILE"])
        fh.setLevel(eval("logging."+log_level))
        fh.setFormatter(formatter)
        root.addHandler(fh)

def pause_all():
    qbt_api.pause_all()
    logging.debug("Pausing all downloads")
    helpers.healthcheck_failure()

def pause_on_low_space():
    logging.debug("Space threshold is: %s", str(space_threshold))
    if helpers.get_free_space() < space_threshold:
        pause_all()
    if helpers.get_free_space() >= space_threshold:
        qbt_api.resume_all()
        logging.debug("Resuming all downloads")
        helpers.healthcheck_ok()

def pause_verify_nzb():
    if os.environ["NZB_HOST"] and not nzb_api.is_paused():
        pause_all()
    else:
        pause_on_low_space()

if __name__ == '__main__':
    start()