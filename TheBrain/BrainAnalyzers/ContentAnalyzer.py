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
    c.init_by_date_range("July 01 2022", "July 02 2022")
    c.start()