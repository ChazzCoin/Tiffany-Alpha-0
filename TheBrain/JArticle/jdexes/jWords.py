from F import DATE
from F import DICT
from F.LOG import Log
from FM.DBDatabase import DBDatabase
from FM.DBCollection import DBCollection
from FCM.Jarticle import JQ
from FCM.Jarticle.jProvider import jSearch

Log = Log("jWords")

WORDS_COLLECTION = "one_word"

"""
collections: one_word, two_word, three_word, four_word
fields: word, score, in_webpages, out_webpages, topic_scores, updatedDate
"""
WQ = lambda word: { "word": word }
BASE_MODEL = lambda word, score, in_webpages, out_webpages: {
                                                                "word": word,
                                                                "score": score,
                                                                "in_webpages": in_webpages,
                                                                "out_webpages": out_webpages
                                                              }


""" Master Class to work with Companies Collection """
class OneWord(DBDatabase):
    owc: DBCollection = None

    @classmethod
    def one_word_collection(cls):
        nc = cls()
        nc.connect("192.168.1.180", 27017).database("research")
        nc.one_word_collection = nc.collection(WORDS_COLLECTION)
        return nc

    def addUpdateWord(self, word, new_record:dict):
        return self.owc.update_record(WQ(word), new_record)

    def get_word(self, word):
        return self.owc.base_query(WQ(word))

    def add_words(self, date, words):
        # get words for date
        # merge words dict
        existingRecord = self.get_word_list_for_date(date)
        existingWordsDict = DICT.get("grams", existingRecord, False)
        if existingWordsDict:
            pass
        masterQuery = {
            "articleDate": date,
            "updatedDate": DATE.mongo_date_today_str(),
            "grams": DICT.get("grams", words),
            "bigrams": DICT.get("bigrams", words),
            "trigrams": DICT.get("trigrams", words),
            "quadgrams": DICT.get("quadgrams", words)
        }
        self.update_record(JQ.DATE(date), masterQuery)

    def get_word_list_for_date(self, date):
        return self.base_query(JQ.DATE(date))

    def add_words_to_list_for_date(self):
        pass


if __name__ == '__main__':
    jc = jWords.constructor_jwords()
