import qbittorrentapi
import os


qbt_client = qbittorrentapi.Client(host=os.environ["QBT_HOST"], port=int(os.environ["QBT_PORT"]), username=os.environ["QBT_USERNAME"], password=os.environ["QBT_PASS"])

def pause_all():
    for torrent in qbt_client.torrents.info.active():
        if torrent.progress < 100:
            torrent.pause()
    
def resume_all():
    for torrent in qbt_client.torrents.info.paused():
        torrent.resume()
