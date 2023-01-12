from F import DATE, LIST, DICT
from FCM.MCCore import MCCore

COLLECTION_NAME = "models"

""" Master Class to work with Companies Collection """
class jModels(MCCore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect(COLLECTION_NAME)

    @staticmethod
    def create_model_query(name, weighted_terms, secondary_weighted_terms):
        today = DATE.TO_DATETIME(DATE.get_now_month_day_year_str())
        return {
                "name": name,
                "weighted_terms": weighted_terms,
                "secondary_weighted_terms": secondary_weighted_terms,
                "date_added": today
                }

    def add_model(self, model):
        self.insert_record(model)

    def get_model(self, name):
        results = self.base_query({ "name": name })
        return LIST.get(0, results, default=False)

    def get_all_models(self):
        return self.base_query({})

    def get_model_weighted_terms(self, name):
        model = self.get_model(name)
        return DICT.get("weighted_terms", model, default=False)

    def get_model_secondary_weighted_terms(self, name):
        model = self.get_model(name)
        return DICT.get("secondary_weighted_terms", model, default=False)

if __name__ == '__main__':
    jm = jModels()
    print(jm.get_model_weighted_terms("metaverse"))