from F import DICT
from FNLP import URL
from FCM.MCCore import MCCore
from FCM.FQ import QBuilder, Q
from F.LOG import Log
Log = Log("jURL")

SOURCES_COLLECTION = "sources"

F_DATE_ADDED = "dateAdded"
F_TYPE = "type"
F_ORIGIN = "origin"
F_SITE_NAME = "siteName"
F_URL = "url"

URL_TYPE = "general url"
RSS_TYPE = "rss"
GOOGLE_TYPE = "google news url"
# USER_TYPE = "user added"
FOPIC_ORIGIN = "FairResources"
COUNT = "count"
COLLECTION_NAME = "sources"

class jSources(MCCore):
    query = QBuilder()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect(COLLECTION_NAME)

    def ADD_URL(self, url, urlType=URL_TYPE):
        return self.add_url(url, urlType)

    def ADD_URLS(self, urls, urlType=URL_TYPE):
        return self.add_urls(urls, urlType)

    def build_query(self, url, urlType=URL_TYPE):
        self.query.clear_query_builder()
        siteName = URL.get_site_name(url)
        dateAdded = self.get_now_date()
        self.query.add_to_query_builder(F_DATE_ADDED, dateAdded)
        self.query.add_to_query_builder(F_SITE_NAME, siteName)
        self.query.add_to_query_builder(F_TYPE, urlType)
        self.query.add_to_query_builder(F_ORIGIN, FOPIC_ORIGIN)
        self.query.add_to_query_builder(F_URL, url)

    def add_rss_url(self, rssURL):
        return self.add_url(url=rssURL, urlType="rss")

    def add_url(self, url, urlType=URL_TYPE):
        self.build_query(url, urlType)
        return self.insert_record(self.query.query_builder)

    def add_urls(self, list_of_urls, urlType=URL_TYPE, ignoreExists=False):
        query_list = []
        for url in list_of_urls:
            self.build_query(url, urlType)
            query_list.append(self.query.query_builder)
        return self.add_records_field_match(query_list, fieldName="url", ignoreExists=ignoreExists)

    def search_urls(self, searchTerm):
        siteSearch = Q.SEARCH("siteName", searchTerm)
        urlSearch = Q.SEARCH("url", searchTerm)
        query = Q.OR([siteSearch, urlSearch])
        return self.base_query(query)

    def get_type_urls(self, typeName):
        typeQuery = Q.BASE("type", typeName)
        results = self.base_query(typeQuery)
        urls = []
        for obj in results:
            url = DICT.get("url", obj, False)
            if url:
                urls.append(url)
        return urls
    def get_metaverse_urls(self):
        return self.get_type_urls("metaverse")


if __name__ == '__main__':
    # import FairResources
    # urls = FairResources.get_metaverse_sources()
    js = jSources()
    r = js.get_metaverse_urls()
    # r = js.add_urls(list_of_urls=urls, urlType="metaverse", ignoreExists=True)
    print(r)