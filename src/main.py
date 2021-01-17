import qbt_api
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

    if not os.environ["CRON"]:
        raise AssertionError("Cron expression is not set")

    logging.debug(
        "Scheduler is enabled. Task will be scheduled to run at %s", os.environ["CRON"])

    scheduler.configure(os.environ["CRON"], pause_on_low_space)
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

    if os.environ["LOG_FILE"]:
        fh = logging.FileHandler(os.environ["LOG_FILE"])
        fh.setLevel(eval("logging."+log_level))
        fh.setFormatter(formatter)
        root.addHandler(fh)

def pause_on_low_space():
    logging.debug("Space threshold is: %s", str(space_threshold))
    if helpers.get_free_space() < space_threshold:
        qbt_api.pause_all()
        logging.debug("Pausing all downloads")
        helpers.healthcheck_failure()
    
    if helpers.get_free_space() >= space_threshold:
        qbt_api.resume_all()
        logging.debug("Resuming all downloads")
        helpers.healthcheck_ok()


# def check_torrents_queue():
#     blocked_torrents = []
#     torrents = []
#     if helpers.get_free_space() < space_threshold:
#         qbt_api.pause_all()

#     if helpers.get_free_space() >= space_threshold:
#         pass
#         if torrents.downloading():
#             for download in torrents.downloading():
#                 if download.remaining_space() > helpers.get_free_space() - buffer:
#                     blocked_torrents.append(download)

#             active_torrents = torrents.downloading() - blocked_torrents

#             if len(active_torrents) == 1:
#                 qbt_api.pause_all()
#                 active_torrents[0].resume()
        
#         if not torrents.downloading() and helpers.get_free_space() > buffer:
#             qbt_api.resume_all()


if __name__ == '__main__':
    start()