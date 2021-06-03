import os
import pynzbgetapi
import logging

ng_api = pynzbgetapi.NZBGetAPI(os.environ["NZB_HOST"], os.environ["NZB_USERNAME"], os.environ["NZB_PASSWORD"])

def is_paused():
    try:
        # RemainingSizeMB PostPaused
        return ng_api.status()["ServerStandBy"]
    except Exception as ex:
        logging.exception("Could not connect to NZBGet: {}".format(str(ex)))
        # if we can't connect to NZBGet, we asume it's paused.
        return True