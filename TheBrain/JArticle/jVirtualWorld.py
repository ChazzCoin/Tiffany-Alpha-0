from F import LIST, DICT
from F.LOG import Log
from FCM.MCCore import MCCore

Log = Log("jVirtualWorld")

COLLECTION_NAME = "virtual_worlds"

""" Master Class to work with Companies Collection """
class jVirtualWorld(MCCore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect(COLLECTION_NAME)

    def add_virtual_world(self, list_of_virtual_worlds):
        for item in list_of_virtual_worlds:
            print(item)
            self.insert_record(item)

    def find_world_by_ticker(self, ticker):
        ticker = str(ticker).upper()
        world_record = self.base_query({'symbol': ticker})
        if world_record:
            single_record = LIST.get(0, world_record, False)
            return single_record
        return False

    def find_ticker_by_world(self, worldName, tickerOnly=False):
        company_record = self.base_query({'name': worldName})
        if company_record:
            single_record = LIST.get(0, company_record, False)
            if tickerOnly:
                ticker = DICT.get("symbol", single_record)
                return ticker
            return single_record
        return False

    def get_world_id_for_ticker(self, ticker):
        world = self.find_world_by_ticker(ticker)
        if world:
            id = DICT.get("_id", world)
            return id
        return False

    def get_list_of_all_worlds(self, page=False, limit=False):
        all_ = self.base_query({}, page=page, limit=limit)
        return all_
    def get_all_world_names(self):
        all_ = self.base_query({}, page=False, limit=False)
        names = []
        for world in all_:
            name = DICT.get("name", world, False)
            names.append(name)
        return names
    def get_all_world_tickers(self):
        all_ = self.base_query({}, page=False, limit=False)
        tickers = []
        for world in all_:
            ticker = DICT.get("symbol", world, False)
            tickers.append(ticker)
        return tickers
    def get_all_world_names_and_tickers(self):
        all_ = self.base_query({}, page=False, limit=False)
        names_tickers = []
        for world in all_:
            name = DICT.get("name", world, False)
            ticker = DICT.get("symbol", world, False)
            names_tickers.append((name, ticker))
        return names_tickers

if __name__ == '__main__':
    jc = jVirtualWorld()
    record = jc.get_all_world_names_and_tickers()
    print(record)