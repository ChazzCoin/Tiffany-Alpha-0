from F import DICT
from F import DATE
from FNLP.Regex import Re
from F.LOG import Log
from FM.Jarticle.jProvider import jPro as jpro
Log = Log("FWEB.Core.Validator")

jp = jpro()


def validateAndSave(article: {}, saveToArchive=False, setDateToToday=False) -> bool:
    date = DICT.get("published_date", article)
    body = DICT.get("body", article)
    if not date and setDateToToday and body and not body.startswith("Something went wrong"):
        date = DATE.mongo_date_today_str()
        article["published_date"] = date
    if date and not body.startswith("Something went wrong"):
        Log.s(f"Article Validated. Saving Now. DATE=[ {date} ]")
        if saveToArchive:
            save_article(article)
            return True
    else:
        Log.w("Failed to Validate Article.", warning=f"DATE=[ {date} ]")
        return False

# -> MAIN
def validate_article2(article):
    date = DICT.get("published_date", article, default=False)
    body = DICT.get("body", article, default=False)
    if date and body and not body.startswith("Something went wrong"):
        Log.s(f"Article Validated. DATE=[ {date} ]")
        return True
    else:
        Log.w("Failed to Validate Article.", warning=f"DATE=[ {date} ]")
        return False

def validate_article(article):
    """
        Takes in JsonArticle or DownloadWebPage and converts it into JSON
        -> Returns JSON of Article only. or False.
    """
    if type(article) is not dict:
        article = DICT.get("json", article, default=article)
    date = DICT.get("published_date", article, default=False)
    body = DICT.get("body", article, default=False)
    if not v_date(date):
        title = DICT.get("title", article, default=False)
        if v_title(title) and v_body(body):
            Log.s(f"Article Validated by [ TITLE ] and [ BODY ].")
            newArticle = DICT.replace_key_value(article, "published_date", DATE.mongo_date_today_str())
            return newArticle
    # Date has been validated here.
    if v_body(body) and v_date(date):
        Log.s(f"Article Validated by [ BODY ] and [ DATE=[ {date} ] ]")
        return article
    # Last resort, False
    Log.w("Failed to Validate Article.", warning=f"DATE=[ {date} ]")
    return False

def v_body(body):
    if body and not body.startswith("Something went wrong"):
        if len(body) > 10:
            return True
    return False

def v_title(title):
    if title:
        if Re.contains_any(["UNKNOWN"], title):
            return False
        elif len(title) > 0:
            return True
    return False

def v_date(date):
    if date and date != "False":
        return True
    return False

def save_article(article):
    return jp.ADD_ARTICLES(article)

def mongo_save(func):
    """ -> DECORATOR <- """
    def wrapper(*args):
        # -> func() should return Article in JSON format.
        article = func(*args)
        if article:
            Log.i("ARTICLE HAS BEEN WRAPPED AND VALIDATED!")
            jp.ADD_ARTICLES(article)
            return article
        return article
    return wrapper

def mongo_update(func):
    """ -> DECORATOR <- """
    def wrapper(*args):
        # -> func() should return Article in JSON format.
        article = func(*args)
        if article:
            Log.i("ARTICLE HAS BEEN WRAPPED AND VALIDATED!")
            jp.ADD_ARTICLES(article)
            return article
        return article
    return wrapper