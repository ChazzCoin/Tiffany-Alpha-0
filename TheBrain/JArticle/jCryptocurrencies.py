from F import LIST
from F import DICT
from F.LOG import Log
from FCM.MCCore import MCCore

Log = Log("jCryptocurrencies")

COLLECTION_NAME = "cryptocurrencies"

""" Master Class to work with Collection """
class jCryptocurrencies(MCCore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect(COLLECTION_NAME)

    def add_cryptocurrency(self, list_of_companies):
        for item in list_of_companies:
            print(item)
            self.insert_record(item)

    def find_crypto_by_ticker(self, ticker):
        ticker = str(ticker).upper()
        company_record = self.base_query({'symbol': ticker})
        if company_record:
            single_record = LIST.get(0, company_record, False)
            return single_record
        return False

    def find_ticker_by_crypto(self, companyName, tickerOnly=False):
        company_record = self.base_query({'$or': [{"name": companyName}, {"slug": companyName}]})
        if company_record:
            single_record = LIST.get(0, company_record, False)
            if tickerOnly:
                ticker = DICT.get("symbol", single_record)
                return ticker
            return single_record
        return False

    def get_crypto_id_for_ticker(self, ticker):
        company = self.find_crypto_by_ticker(ticker)
        if company:
            id = DICT.get("_id", company)
            return id
        return False

    def get_list_of_all_cryptos(self):
        all_ = self.base_query({}, page=False, limit=False)
        return all_

    def get_list_of_all_tickers(self):
        all_ = self.base_query({}, page=False, limit=False)
        tickers = []
        for item in all_:
            ticker = DICT.get("symbol", item, default=False)
            tickers.append(ticker)
        return tickers

    def get_list_of_all_crypto_names(self):
        all_ = self.base_query({}, page=False, limit=False)
        names = []
        for item in all_:
            name = DICT.get("name", item, default=False)
            names.append(name)
        return names


if __name__ == '__main__':
    jc = jCryptocurrencies()
    record = jc.find_crypto_by_ticker("XRP")
    print(record)