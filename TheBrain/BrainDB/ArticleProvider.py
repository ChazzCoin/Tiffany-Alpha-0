from F import DATE
from TheBrain.JArticle import JQ, F
from FM.DBDatabase import DBDatabase
from FM.QueryHelper import Q, A


class STAGE_MATCH(A):


    MATCH_SEARCH = lambda searchTerm: {"$match": JQ.SEARCH_ALL(search_term=searchTerm)}
    MATCH_SINGLE_FIELD_VALUE = lambda field, value: {A.MATCH: {field: value}}
    MATCH_SINGLE_FIELD_EXISTS = lambda field, exists: {A.MATCH: Q.FIELD_EXISTENCE(field, exists)}

# class STAGE_SORT(A):
#     SORT_BY_SCORE_DATE = {A.SORT: {F.SCORE: DESCENDING, F.PUB_DATE: DESCENDING}}

class STAGE_LOOKUP(A):
    LOOKUP = lambda fromCollection, localField, foreignField, outputName: {
        "from": fromCollection,
        "localField": localField,
        "foreignField": foreignField,
        "as": outputName
    }
MATCH_DATE_RANGE = lambda gte, lte: {"$match": {"$and": [JQ.DATE_PUB_GREATER_THAN(gte), JQ.DATE_PUB_LESS_THAN(lte)]}}
class Provider(DBDatabase):
    db_core = None
    db_brain: DBDatabase = None
    db_research: DBDatabase = None
    article_collection = None

    def __init__(self):
        super().__init__()
        self.connect_to_research()

    def connect_to_research(self):
        self.db_core = DBDatabase().connect("192.168.1.180", 27017)
        self.db_research = self.db_core.database("research")
        self.db_brain = self.db_core.database("brain")
        self.article_collection = self.db_research.collection("articles")

    def get_articles(self, limit=100):
        return self.article_collection.base_query({}, limit=limit)

    def get_articles_by_date(self, date, limit=0):
        results = self.db_core.database("research").collection("articles").base_query(kwargs=JQ.DATE(date), limit=limit)
        return results

    def get_articles_by_date_range(self, gte, lte):
        if type(gte) in [str]:
            gte = DATE.TO_DATETIME(gte)
        if type(lte) in [str]:
            lte = DATE.TO_DATETIME(lte)
        results = self.db_core.database("research").collection("articles").base_aggregate([MATCH_DATE_RANGE(gte, lte)])
        return results

    def get_articles_not_analyzed(self, limit=100):
        webpage_id_collection = self.db_brain.collection("analyzed_webpages")
        webpages_ids = webpage_id_collection.base_query({}, limit=0)
        if not webpages_ids:
            temp = self.db_core.database("research").collection("articles").base_query({}, limit=limit)
            return temp
        ids = self.prepare_webpage_ids(webpages_ids)
        return self.db_core.database("research").collection("articles").base_query({"_id": {"$nin": ids}}, limit=limit)

    def get_articles_analyzed(self, limit=100):
        webpage_id_collection = self.db_brain.collection("analyzed_webpages")
        webpages_ids = webpage_id_collection.base_query({}, limit=0)
        if not webpages_ids:
            temp = self.db_core.database("research").collection("articles").base_query({}, limit=limit)
            return temp
        ids = self.prepare_webpage_ids(webpages_ids)
        return self.db_core.database("research").collection("articles").base_query({"_id": {"$in": ids}}, limit=limit)

    @staticmethod
    def prepare_webpage_ids(webpage_ids: list):
        ids = []
        id_queries = []
        for webpage in webpage_ids:
            temp_id = webpage["_id"]
            single_query = {"_id": Q.NOT_EQUALS(temp_id)}
            ids.append(temp_id)
            id_queries.append(single_query)
        return ids

if __name__ == '__main__':
    db = Provider()
    # result = db.get_articles_not_analyzed()
    result = db.get_articles_by_date_range(gte="July 01 2022", lte="August 01 2022")
    print(result)