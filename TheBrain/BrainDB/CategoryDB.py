from F import LIST, DICT
from FM.DBDatabase import DBDatabase


class CategoryDB:
    db_brain = None
    db_collection = None
    model_categories = {}

    def connect_to_brain(self):
        self.db_brain = DBDatabase().connect("192.168.1.180", 27017).database("research")
        self.db_collection = self.db_brain.collection("models")

    def add_model(self, model):
        self.db_collection.insert_record(model)

    def update_model(self, model):
        name = DICT.get("name", model, None)
        if not name:
            return "No Model Found."
        findQuery = {"name": name}
        self.db_collection.update_record(findQuery, model)

    def get_model(self, name):
        results = self.db_collection.base_query({ "name": name })
        return LIST.get(0, results, default=False)

    def get_all_models(self):
        return self.db_collection.base_query({})

    def load_models(self):
        model_results = self.db_collection.base_query({})
        self.model_categories = model_results

    def get_model_weighted_terms(self, name):
        model = self.get_model(name)
        return DICT.get("weighted_terms", model, default=False)

    def get_model_secondary_weighted_terms(self, name):
        model = self.get_model(name)
        return DICT.get("secondary_weighted_terms", model, default=False)