from FM.FMClient import FMClient
from FM.FMDb import FMDB
from FRedis import Redis

r = Redis(ip="192.168.1.229")
mongo_config = r.get_config("mongo")
def get_mongo_client(ip="sozindb.vaatu.co", port=1214):
    FMClient().connect(ip, port)
# def getClientObject():
#     return FMClient(**mongo_config)
#
CLIENT = lambda ip, port: get_mongo_client()

def get_brain_db(client:FMClient):
    return FMDB(dbclient=client).database("brain")

def get_research_db(client:FMClient):
    return FMDB(dbclient=client).database("research")