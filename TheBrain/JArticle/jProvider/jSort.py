from F import CONVERT, DATE, DICT, LIST
from F.LOG import Log
Log = Log("FArt.artSort")

def sort_articles_by_date(articles, toDict=True):
    with_dates = []
    without_dates = []
    for art in articles:
        pDate = DICT.get("published_date", art, False)
        if not pDate:
            without_dates.append(art)
            continue
        with_dates.append(art)
    sorted_articles = LIST.SORT_BY_DICT_KEY(with_dates, "published_date")
    if not toDict:
        return sorted_articles
    by_date_dict = CONVERT.list_OF_Dicts_TO_Dict_BY_KeyValue(sorted_articles, "published_date")
    return by_date_dict

def sort_articles_into_lists_by_date(articles, daysBack=7) -> list:
    by_date = sort_articles_by_date(articles, toDict=True)
    today = DATE.mongo_date_today_str()
    range_of_dates = DATE.get_range_of_dates_by_day(today, daysBack)
    temp_list = []
    for date in range_of_dates:
        current_date_list = DICT.get(date, by_date, False)
        if current_date_list:
            sorted_date_list = sort_articles_by_score(current_date_list)
            temp_list.append(sorted_date_list)
    return temp_list

def sort_articles_by_score(articles) -> list:
    Log.v(f"sort_hookups_by_score: IN: {articles}")
    sorted_articles = LIST.SORT_BY_DICT_KEY(articles, "score")
    return sorted_articles