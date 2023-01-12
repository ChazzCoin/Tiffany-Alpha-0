from F import DATE
from F import LIST
from F import DICT
from F.LOG import Log
from FCM.Jarticle import JQ
from FCM.Jarticle.jProvider import jSearch
from FCM.FQ import Q

Log = Log("jNLP")

NLP_COLLECTION = "nlp"

""" Master Class to work with Companies Collection """
class jNLP(jSearch):

    @classmethod
    def constructor_jnlp(cls):
        nc = cls()
        nc.construct_mcollection(NLP_COLLECTION)
        return nc

    def add_stop_words(self, list_of_stopwords):
        j = {
            "stopwords": list_of_stopwords,
            "updatedDate": DATE.mongo_date_today_str()
        }
        return self.update_record(JQ.ID('628d69b62787376f4be87c57'), j)

    def get_stop_words(self):
        record = self.base_query(Q.FIELD_EXISTENCE("stopwords", True))
        single_records = LIST.get(0, record, False)
        stopwords = DICT.get("stopwords", single_records, False)
        return stopwords

if __name__ == '__main__':
    jn = jNLP.constructor_jnlp()
    test = jn.add_stop_words(['we', 'there'])
    print(test)
