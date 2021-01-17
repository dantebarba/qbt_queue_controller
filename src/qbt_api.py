import qbittorrentapi
import os


qbt_client = qbittorrentapi.Client(host=os.environ["QBT_HOST"], port=int(os.environ["QBT_PORT"]), username=os.environ["QBT_USERNAME"], password=os.environ["QBT_PASS"])

def pause_all():
    qbt_client.torrents.pause.all()
    
def resume_all():
    qbt_client.torrents.resume.all()

