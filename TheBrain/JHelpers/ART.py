from datetime import datetime
import F
from F import DICT, LIST

def remove_duplicate_articles(listOfArticles:[]):
    cleaned_list = []
    for item in listOfArticles:
        newItem = DICT.remove_key_value("_id", item)
        cleaned_list.append(newItem)
    noDups = LIST.remove_duplicates(cleaned_list)
    return noDups

def get_content(article):
    title = DICT.get("title", article, False)
    body = DICT.get("body", article, False)
    description = DICT.get("description", article, False)
    content = F.combine_args_str(title, body, description)
    return content

def extract_content(article):
    title = DICT.get("title", article, None)
    body = DICT.get("body", article, None)
    description = DICT.get("description", article, None)
    tags = DICT.get("tags", article, None)
    keywords = DICT.get("keywords", article, None)
    content = F.combine_args_str(title, body, description, tags, keywords)
    return content

def extract_field_values(articles, field_name):
    field_values = []
    for art in articles:
        temp_field = DICT.get(field_name, art, None)
        if not temp_field:
            continue
        field_values.append(temp_field)
    return field_values

def extract_dates(articles):
    dates = []
    for art in articles:
        pub_date = DICT.get("pub_date", art, None)
        if not pub_date:
            continue
        dates.append(pub_date)
    return dates



def get_highest_score(dic:dict):
    highest_score = 0
    highest_word = ""
    for key in dic:
        score = dic[key]
        if int(score) > highest_score:
            highest_word = key
            highest_score = score
    return highest_word, highest_score


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

