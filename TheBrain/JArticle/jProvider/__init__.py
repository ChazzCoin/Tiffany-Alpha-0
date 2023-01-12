from F import LIST
from FCM.Jarticle.jProvider.jDate import jpDate
from FCM.Jarticle.jProvider.jCategories import jpCat
from FCM.Jarticle.jProvider.jSocial import jpSocial
from FCM.Jarticle.jProvider.jSearch import jpSearch
from FCM.Jarticle.jProvider import jSort
ARTICLES_COLLECTION = "articles"

"""
This is a Full Interface for ARTICLES collection in MongoDB.
- It will auto initialize connection to DB/Collection.
- You use this class direction.
Usage:
    - jp = jPro()
    - jp.get_article_count()
"""

class jPro(jpSearch, jpDate, jpCat, jpSocial):

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
        # dbUri = self.get_arg("dbUri", kwargs, default=False)
        # dbName = self.get_arg("dbName", kwargs, default=False)
        # # self.connect(collectionName=self.mcollection_name, dbUri=dbUri, dbName=dbName)
        # print(self.mcollection_name)

    def get_meta_feed(self):
        search_results = self.search_all("metaverse")
        cat_results = self.get_metaverse_articles()
        flattened_list = LIST.flatten(search_results, cat_results)
        final_results = jSort.sort_articles_by_date(flattened_list, toDict=False)
        fr = final_results[:100]
        return fr

    def get_article_count(self):
        return self.get_document_count()

    def get_search(self, searchTerm):
        return self.search_all(search_term=searchTerm)

    def get_articles_by_key_value(self, kwargs):
        return self.base_query(kwargs=kwargs)

    def get_no_published_date(self, unlimited=False):
        return self.get_articles_no_date(unlimited=unlimited)

    def get_no_published_date_not_updated_today(self, unlimited=False):
        return self.get_articles_no_date_not_updated_today(unlimited=unlimited)

    def get_ready_to_enhance(self):
        temp = self.get_no_category_last_7_days()
        if temp:
            return temp
        temp2 = self.get_no_category_by_1000()
        if temp2:
            return temp2
        return False



if __name__ == '__main__':
    uri = f"mongodb://192.168.1.180:27017"
    t = jPro(dbUri=uri, dbName="research")
    print(t.get_document_count())
    # r = t.search_by_date_range("ripple", "July 01 2022", "August 16 2022", limit=35)
    # print(r)
#     r = t.get_method_names()
#     # p = t.add_pub_date()
#     # p = t.by_date_range_test()
#     # p = t.test_new_pub_date()
#     # p = t.new_search()
#     i = t.get_func(r[38])
#     u = i()
#     p = t.get_article_count()
#     print(p)