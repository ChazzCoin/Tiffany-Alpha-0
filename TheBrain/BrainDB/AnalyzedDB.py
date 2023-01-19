from F import DICT, DATE, LIST
from FM.FMDb import FMDB
from FM.QueryHelper import O, Q
from TheBrain.BrainDB import DB

"""
    - 1. Save all words and their count.
        "analyzed_words" collection
    - 2. Get all words and their count.
        "analyzed_words" collection
        "word" - "word_count" - "word_score"
"""
ANALYZED_WEBPAGES = "analyzed_webpages"
ANALYZED_WORDS = "analyzed_words"
ANALYZED_STOP_WORDS = "analyzed_stop_words"
ANALYZED_SENTENCES = "analyzed_sentences"
ANALYZED_WORDS_BY_DATE = "analyzed_words_by_date"

class AnalyzedDB:
    db_brain = None
    model_categories = {}
    analyzed_words = None
    analyzed_stop_words = None
    analyzed_webpages = None
    analyzed_sentences = None
    analyzed_words_by_date = None

    def __init__(self):
        self.connect_to_brain()

    def connect_to_brain(self):
        client = FMDB(**DB.mongo_config)
        self.db_brain = client.database("brain")
        self.analyzed_words = self.db_brain.collection(ANALYZED_WORDS)
        self.analyzed_stop_words = self.db_brain.collection(ANALYZED_STOP_WORDS)
        self.analyzed_webpages = self.db_brain.collection(ANALYZED_WEBPAGES)
        self.analyzed_sentences = self.db_brain.collection(ANALYZED_SENTENCES)
        self.analyzed_words_by_date = self.db_brain.collection(ANALYZED_WORDS_BY_DATE)

    def get_analyzed_count(self):
        return self.analyzed_webpages.get_document_count()
    def get_doc_count(self, collection_name):
        collection = self.db_brain.collection(collection_name)
        return collection.get_document_count()
    def addUpdate_analyzed_words_by_date(self, date_models:[{}]):
        return self.analyzed_words_by_date.addUpdate_records(date_models)

    def addUpdate_analyzed_words(self, word_counts:[{}], collection_name:str):
        collection = self.db_brain.collection(collection_name)
        return collection.addUpdate_records(word_counts)

    def save_word_counts(self, word_counts:[{}], collection_name:str):
        collection = self.db_brain.collection(collection_name)
        return collection.add_records(word_counts)

    def get_analyzed_words(self, toRecords=False):
        return self.analyzed_words.base_query({}, limit=0, toRecords=toRecords)

    def get_all_analyzed_words_by_date(self, toRecords=False):
        return self.analyzed_words_by_date.base_query({}, limit=0, toRecords=toRecords)

    def get_analyzed_words_on_date(self, date):
        query = Q.BASE("date", DATE.TO_DATETIME(date))
        results = self.analyzed_words_by_date.base_query(query, limit=0)
        item = LIST.get(0, results, None)
        return item

    def get_analyzed_word_counts_on_date(self, date):
        query = Q.BASE("date", DATE.TO_DATETIME(date))
        results = self.analyzed_words_by_date.base_query(query, limit=0)
        item = LIST.get(0, results, None)
        return DICT.get("word_counts", item, None)

    def get_analyzed_stop_words(self):
        return self.analyzed_stop_words.base_query({}, limit=0)

    def get_analyzed_webpages(self):
        return self.analyzed_webpages.base_query({}, limit=0)

    def get_analyzed_webpages_ids_only(self):
        results = self.analyzed_webpages.base_query({}, limit=0)
        if not results:
            return None
        ids = []
        for item in results:
            temp_id = DICT.get("_id", item, None)
            ids.append(temp_id)
        return ids

    def addUpdate_webpage_references(self, webpage_ids):
        for model in webpage_ids:
            webID = DICT.get("_id", model, None)
            if not webID:
                continue
            findQuery = { "_id": O.OBJECT_ID(webID)}
            self.analyzed_webpages.update_record(findQuery, model)


if __name__ == '__main__':
    results = AnalyzedDB().get_all_analyzed_words_by_date()
    print(results)