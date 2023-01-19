from F import DICT, DATE
from F.LOG import Log
from TheBrain.BrainDB.BrainData import BrainData
from TheBrain.BrainDB.BrainModels import ANALYZED_WORDS_BY_DATE
from TheBrain.BrainModels.BaseModel import BaseBrain
from TheBrain.BrainModels.Variables import BrainVariables

from TheBrain import BrainMath
from FNLP.LanguageManagers import ContentManager, WordsManager

Log = Log("BrainManager")


"""
BrainModel -> Gets existing data from Brain Database.
            - Imports/Merges in ContentModel.
            - Updates Brain Database.

ContentModel -> Facilitates each of the following models.
WordModel -> Breaks down All Words in content.
SentenceModel -> Breaks down All Sentences in content.
ParagraphModel -> Breaks down All Paragraphs in content.
"""
class BrainManager(BaseBrain, BrainVariables):
    saveToBrain = True
    brainData: BrainData = BrainData()
    contentManager: ContentManager.ContentManager = None

    """
    config:
        enableAnalyzeWords = True
        enableAnalyzeStopWords = True
        enableAnalyzeWordsByDate = True
    for db:
        analyzed_words_for_db = []
        analyzed_stop_words_for_db = []
        analyzed_webpages_for_db = []
        analyzed_words_by_date_for_db = []
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_brain_manager(self):
        self.prepare_for_brain()
        if self.saveToBrain:
            self.update_brain_database()

    def add_content_manager(self, content_manager:[ContentManager]):
        self.contentManager = content_manager

    def prepare_for_brain(self):
        mw: WordsManager.WordsManager = self.contentManager.model_words
        self.analyzed_words_for_db = BrainMath.add_word_frequency_counts(self.brainData.analyzed_words, mw.overall_counts)
        self.analyzed_stop_words_for_db = BrainMath.add_word_frequency_counts(self.brainData.analyzed_stop_words, mw.overall_stop_counts)
        self.analyzed_webpages_for_db = mw.webpage_models
        """ Words By Date """
        dates = mw.overall_words_by_date
        for dateKey in dates:
            model = dates[dateKey]
            self.create_date_counts_model(dateKey, model)

    def create_date_counts_model(self, dateKey, dateCountModel:WordsManager):
        # dateModel: WordsManager.WordsManager = dates[dateKey]
        dateCounts = dateCountModel.overall_counts
        wasUpdated, dateCounts = self.merge_date_counts_with_brain(dateKey, dateCounts)
        if wasUpdated:
            self.analyzed_words_by_date_for_db.append(dateCounts)
            return
        dateCounted = len(dateCounts)
        query = ANALYZED_WORDS_BY_DATE(dateKey, dateCounts, dateCounted)
        self.analyzed_words_by_date_for_db.append(query)

    def merge_date_counts_with_brain(self, dateKey, dateCounts:dict) -> (bool, dict):
        db_word_counts_model = self.brainData.db.get_analyzed_words_on_date(dateKey)
        if not db_word_counts_model:
            return False, dateCounts
        db_word_counts = DICT.get("word_counts", db_word_counts_model, None)
        dateCounts = BrainMath.add_word_counts(db_word_counts, dateCounts)
        db_word_counts_model["word_counts"] = dateCounts
        db_word_counts_model["words_counted"] = len(dateCounts)
        db_word_counts_model["updatedDate"] = DATE.TODAY
        return True, db_word_counts_model


    def update_brain_database(self):
        if self.enableAnalyzeWords:
            self.brainData.db.addUpdate_analyzed_words(self.analyzed_words_for_db, "analyzed_words")
        if self.enableAnalyzeStopWords:
            self.brainData.db.addUpdate_analyzed_words(self.analyzed_stop_words_for_db, "analyzed_stop_words")
        if self.enableAnalyzeWordsByDate:
            self.brainData.db.addUpdate_analyzed_words_by_date(self.analyzed_words_by_date_for_db)
        self.brainData.db.addUpdate_webpage_references(self.analyzed_webpages_for_db)

