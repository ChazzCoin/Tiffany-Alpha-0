from F import DATE, LIST
from FCM.FQ import AO
from FCM.Jarticle import JQ
from FCM.Jarticle.jProvider import jPro
from FCM.Jarticle.jVirtualWorld import jVirtualWorld
from FCM.Jarticle.jCompany import jCompany

def sort_articles_by_score(articles) -> list:
    # Log.v(f"sort_hookups_by_score: IN: {articles}")
    sorted_articles = LIST.SORT_BY_DICT_KEY(articles, "score")
    return sorted_articles


class harkPipe:
    DATE_RANGE = lambda gte, lte: {"$match": {"pub_date": {"$gte": DATE.TO_DATETIME(gte), "$lte": DATE.TO_DATETIME(lte)}}}
    CATEGORY = lambda categoryName: { "$match": { "category": { "$eq": categoryName } } }

class MetaFeeds:
    meta_dynamic = lambda gte, lte, *searchTerms: [
        # { "$match": { "pub_date": { "$gte": weekBack, "$lte": DATE.TO_DATETIME(today) } } },
        harkPipe.DATE_RANGE(gte, lte),
        {"$match": {"$or": [ JQ.SEARCH_ALL_STRICT(search_term=term) for term in searchTerms ] }},
        {"$sort": {"pub_date": -1}},
        {AO.LIMIT: 500}
    ]

    meta_v1 = lambda gte, lte: [
        # { "$match": { "pub_date": { "$gte": weekBack, "$lte": DATE.TO_DATETIME(today) } } },
        harkPipe.DATE_RANGE(gte, lte),
        { "$match": { "$or": [JQ.SEARCH_ALL_STRICT(search_term="virtual world"),
                              JQ.SEARCH_ALL_STRICT(search_term="virtual reality"),
                              JQ.SEARCH_ALL_STRICT(search_term="metaverse"),
                              { "category": { "$eq": "metaverse" } }]}},
        { "$sort": { "pub_date": -1 }},
        { AO.LIMIT: 500 }
    ]
    meta_v2 = lambda gte, lte, sortBy: [
        # { "$match": { "pub_date": { "$gte": weekBack, "$lte": DATE.TO_DATETIME(today) } } },
        harkPipe.DATE_RANGE(gte, lte),
        harkPipe.CATEGORY("metaverse"),
        { "$sort": { "score" if str(sortBy).startswith("score") else "pub_date": -1 } },
        {AO.LIMIT: 500}
    ]
    meta_v3 = lambda gte, lte: [
        # { "$match": { "pub_date": { "$gte": weekBack, "$lte": DATE.TO_DATETIME(today) } } },
        harkPipe.DATE_RANGE(gte, lte),
        { "$match": { "$or": [JQ.SEARCH_ALL_STRICT(search_term="virtual world"),
                              JQ.SEARCH_ALL_STRICT(search_term="virtual reality"),
                              JQ.SEARCH_ALL_STRICT(search_term="VR"),
                              JQ.SEARCH_ALL_STRICT(search_term="AR"),
                              JQ.SEARCH_ALL_STRICT(search_term="metaverse"),
                              { "category": { "$eq": "metaverse" } }]}},
        {"$sort": {"pub_date": -1}},
        {AO.LIMIT: 500}
    ]
    meta_v4_land = lambda gte, lte: [
        # { "$match": { "pub_date": { "$gte": weekBack, "$lte": DATE.TO_DATETIME(today) } } },
        harkPipe.DATE_RANGE(gte, lte),
        {"$match": {"$or": [JQ.SEARCH_ALL_STRICT(search_term="virtual land"),
                            JQ.SEARCH_ALL_STRICT(search_term="virtual property"),
                            JQ.SEARCH_ALL_STRICT(search_term="virtual real estate"),
                            JQ.SEARCH_ALL_STRICT(search_term="metaverse land"),
                            JQ.SEARCH_ALL_STRICT(search_term="metaverse property"),
                            JQ.SEARCH_ALL_STRICT(search_term="metaverse real estate"),
                            JQ.SEARCH_ALL_STRICT(search_term="digital land"),
                            JQ.SEARCH_ALL_STRICT(search_term="digital property"),
                            JQ.SEARCH_ALL_STRICT(search_term="digital real estate")]}},
        {"$sort": {"pub_date": -1}},
        {AO.LIMIT: 500}
    ]


class harkPro(jPro):
    jworld = jVirtualWorld()
    jcompany = jCompany()
    # def __int__(self):
    #     self.init_references()
    # def init_references(self):
    #     jworld = jVirtualWorld()
    #     jcompany = jCompany()
    def get_ticker(self, ticker):
        return self.jworld.find_world_by_ticker(ticker)
    # "2022-09-01T00:00:00.000Z"#
    def get_meta_feed_v1(self, daysBack=7):
        """ Search + Category """
        today = DATE.get_now_month_day_year_str()
        weekBack = DATE.subtract_days(today, daysBack=daysBack, toString=False)
        m2 = MetaFeeds.meta_v1(weekBack, today)
        results = self.base_aggregate(m2)
        return results

    def get_meta_feed_v2(self, daysBack):
        """ Category Only SORT BY DATE """
        today = DATE.get_now_month_day_year_str()
        weekBack = DATE.subtract_days(today, daysBack=daysBack, toString=False)
        m2 = MetaFeeds.meta_v2(weekBack, today, sortBy="pub_date")
        results = self.base_aggregate(m2)
        return results

    def get_meta_feed_v3(self, daysBack):
        """ Category Only SORT BY SCORE """
        today = DATE.get_now_month_day_year_str()
        weekBack = DATE.subtract_days(today, daysBack=daysBack, toString=False)
        m2 = MetaFeeds.meta_v2(weekBack, today, sortBy="score")
        results = self.base_aggregate(m2)
        return results

    def get_meta_feed_v4(self, daysBack):
        """ Search for Land/Property """
        today = DATE.get_now_month_day_year_str()
        weekBack = DATE.subtract_days(today, daysBack=daysBack, toString=False)
        m2 = MetaFeeds.meta_v4_land(weekBack, today)
        results = self.base_aggregate(m2)
        return results


if __name__ == '__main__':
    hk = harkPro()
    date = hk.get_meta_feed_v2(7)
    score = hk.get_meta_feed_v3(7)
    print("done")