from F import DATE
from F.CLASS import FairClass



class WeightedScores:
    MAX_WEIGHT = 200
    HIGH_WEIGHT = 130
    MIDDLE_WEIGHT = 75
    LOW_WEIGHT = 25
    MINI_WEIGHT = 10
    NANO_WEIGHT = 3
    MIN_WEIGHT = 1


class CategoryModel(FairClass):
    model = {}
    # Fields
    name = ""
    weighted_terms = {}
    secondary_weighted_terms = {}
    updatedDate = DATE.TODAY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_weighted_terms(self):
        return self.weighted_terms

    def update_weighted_terms(self):
        pass

    def get_secondary_weighted_terms(self):
        return self.secondary_weighted_terms

    def update_secondary_weighted_terms(self):
        pass

    def get_database_json(self):
        self.model = { "name": self.name,
                       "weighted_terms": self.weighted_terms,
                       "secondary_weighted_terms": self.secondary_weighted_terms,
                       "updatedDate": self.updatedDate
                       }
        return self.model

    def load_model(self, model):
        self.fromJson(model)






