from FNLP.LanguageStructure.Variables import BaseVariables


class BrainVariables(BaseVariables):
    enableAnalyzeWords = True
    enableAnalyzeStopWords = True
    enableAnalyzeWordsByDate = True
    analyzed_words_for_db = []
    analyzed_stop_words_for_db = []
    analyzed_webpages_for_db = []
    analyzed_words_by_date_for_db = []