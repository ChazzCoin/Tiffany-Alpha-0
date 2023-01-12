from F import DATE
from FCM.Jarticle import JQ, Pipelines
from FCM.FQ import Q
from FCM.Jarticle.jArticles import jArticles

class jpSearch(jArticles):
    """
            -> Article Extension for Specifically Search Functionality.
        """

    def search_by_date_range(self, searchTerm, gte, lte, limit=1000):
        gte2 = DATE.TO_DATETIME(gte)
        lte2 = DATE.TO_DATETIME(lte)
        return self.base_aggregate(Pipelines.SEARCH_BY_DATE_RANGE(searchTerm=searchTerm, gte=gte2, lte=lte2, limit=limit), allowDiskUse=True)

    def search_field(self, search_term, field_name, page=0, limit=100):
        return self.base_query(kwargs=Q.SEARCH(field_name, search_term), page=page, limit=limit)

    def search_all(self, search_term, page=0, limit=100, strict=False):
        if strict:
            return self.base_query(kwargs=JQ.SEARCH_ALL_STRICT(search_term), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=page, limit=limit)

    def search_unlimited(self, search_term):
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=False, limit=False)

    def search_cli(self, search_term, filters):
        kwargs = Q.AND([JQ.SEARCH_ALL(search_term), filters])
        return self.base_query(kwargs=kwargs, page=False, limit=False)

    def search_unlimited_filters(self, search_term, filters):
        kwargs = Q.AND([JQ.SEARCH_ALL(search_term), filters])
        return self.base_query(kwargs=kwargs, page=False, limit=False)

    def search_before_or_after_date(self, search_term, date, page=0, limit=100, before=False):
        if before:
            return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_LTE(search_term, date), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_GTE(search_term, date), page=page, limit=limit)

    def search_field_by_date(self, date, search_term, field_name):
        return self.base_query(kwargs=JQ.SEARCH_FIELD_BY_DATE(date, field_name, search_term))

    # def find_records_where_date(self, date: str, toDict=False) -> cursor or dict:
    #     """ -> RETURN Cursor of all Records for Date. <- """
    #     result = self.base_query(JQ.DATE(date))
    #     if toDict:
    #         return MCore.to_counted_dict(result)
    #     else:
    #         return result
    #
    # def find_records_where_count(self, date: str, limit=1000, toDict=False) -> list or dict:
    #     """ -> RETURN List/Dict of all Records for Date with count under limit. <- """
    #     result = self.base_query({F.DATE: date, F.COUNT: Q.LTE(limit)})
    #     if toDict:
    #         _result = MCore.to_counted_dict(result)
    #     else:
    #         _result = list(result)
    #     return _result