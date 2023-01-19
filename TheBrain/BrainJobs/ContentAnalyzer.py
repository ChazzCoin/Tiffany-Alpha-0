from F.LOG import Log
from TheBrain.BrainDB.ArticleProvider import Provider
from TheBrain.BrainModels.BrainManager import BrainManager
from FNLP.LanguageManagers.ContentManager import ContentManager

"""
checklist

1. get webpages/article id's already looked at... "analyzed_webpages"
2. Query for webpages that do not have the _id of "analyzed_webpages"
3. Add Articles to ContentModel()
4. Get BrainModel()
4. Run Analyzer
5. Merge ContentModel with BrainModel
6. Update Brain

- ContentModel
- BrainModel
- BrainDB
- BrainMath
"""

"""
Analyzer 
Manager
Engine

"""
Log = Log("Word-Analyzer")

class ContentAnalyzer(Provider, BrainManager, ContentManager):
    saveToBrain = False
    webpages = []

    """
    WORDS:
    -> Organizes words analyzed by Date of webpage/content.
        overall_words_by_date       = { "_id": datetime, "word_counts": { "ALL_WORDS": count }, "words_counted": XX }
        stop_words_by_date          = { "_id": datetime, "word_counts": { "FILTERED_WORDS": count }, "words_counted": XX }

    -> Raw overall memory of words and how many times we've counted that word.
        overall_counts: dict        = { "ALL_WORDS": count }
        overall_words_counted: int  = 0
        overall_stop_counts: dict   = { "FILTERED_WORDS": count }

    -> Organizing Unique words looked at/counted.
        unique_words: list          = ["word1", "word2] -> No duplicate words.
        unique_words_counted: int   = XX -> Count of unique words.
    
    SENTENCES:
    -> Organizes sentences analyzed by Date of webpage/content.
        sentences_by_date: dict         = { "datetime": [sentenceOne, sentenceTwo], "datetime": [sentenceOne, sentenceTwo] }

    -> Raw overall memory of sentences and how many were counted.       
        overall_sentences: list         = [ "sentence1", "sentence2" ]
        overall_sentences_counted: int  = 2
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_by_date_range(self, gte, lte):
        results = self.get_articles_by_date_range(gte, lte)
        self.add_webpages(results)
    def start(self):
        self.run_content_analyzer()
        self.run_brain_manager()


if __name__ == '__main__':
    c = ContentAnalyzer()
    c.init_by_date_range("July 03 2022", "July 04 2022")
    c.start()


