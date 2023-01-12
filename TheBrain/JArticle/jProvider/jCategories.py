from F import LIST
from F import DATE
from FCM.Jarticle import JQ
from FCM.FQ import Q
from FCM.Jarticle.jArticles import jArticles

def sort_articles_by_score(articles) -> list:
    # Log.v(f"sort_hookups_by_score: IN: {articles}")
    sorted_articles = LIST.SORT_BY_DICT_KEY(articles, "score")
    return sorted_articles

class jpCat(jArticles):

    def get_category_by_date(self, category, date):
        temp = self.base_query(kwargs=JQ.CATEGORY_BY_DATE(category, date))
        return temp

    def get_category(self, category):
        return self.base_query(kwargs=JQ.CATEGORY(category))

    def get_categories(self, *categories):
        full_list = []
        categories = LIST.flatten(categories)
        for cat in categories:
            temp = self.base_query(kwargs=JQ.CATEGORY(cat))
            full_list.append(temp)
        flattedList = LIST.flatten(full_list)
        sortedList = sort_articles_by_score(flattedList)
        return sortedList

    def get_no_category_date_range_list(self, daysBack):
        daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
        tempListOfArticles = []
        for day in daysbacklist:
            tempArts = self.get_no_category_by_date(day)
            if tempArts:
                tempListOfArticles.append(tempArts)
        return tempListOfArticles

    def get_no_category_last_x_days(self, daysBack=7):
        temp = self.get_no_category_date_range_list(daysBack)
        returnList = []
        if temp and len(temp) > 0:
            for item in temp:
                if not item:
                    continue
                returnList.append(item)
            if len(temp) > 0:
                return temp
        return False

    def get_no_category_last_7_days(self):
        return self.get_no_category_last_x_days(7)

    def get_no_category_by_1000(self):
        temp = self.get_only_articles_no_category()
        if temp and len(temp) > 0:
            return temp
        return False

    def get_no_category_by_date(self, date, artsOnly=True):
        if artsOnly:
            return self.get_only_articles_no_category_by_date(date)
        return self.get_articles_no_category_by_date(date)

    def get_categories_last_5_days(self, *categories):
        dateRange = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), 5)
        full_list = []
        categories = LIST.flatten(categories)
        for date in dateRange:
            for cat in categories:
                query = Q.AND([JQ.DATE(date), JQ.CATEGORY(cat)])
                temp = self.base_query(kwargs=query)
                full_list.append(temp)
        flattedList = LIST.flatten(full_list)
        # sortedList = sort_articles_by_score(flattedList)
        return flattedList

    def get_metaverse_articles(self):
        return self.get_categories("metaverse")

    def get_articles_no_category_by_date(self, date):
        return self.base_query(kwargs=JQ.NO_CATEGORY_BY_DATE(date))

    def get_only_articles_no_category_by_date(self, date):
        return self.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT_BY_DATE(date))

    def get_only_articles_no_category(self):
        return self.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT, page=0, limit=1000)