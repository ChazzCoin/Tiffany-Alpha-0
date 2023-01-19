import pandas as pd
import matplotlib.pyplot as plt
from TheBrain.BrainDB.BrainData import BrainData

bata = BrainData()

def to_dataframe(data:dict):
    return pd.DataFrame(data)

def show_chart(data, x, y):
    dataframe = to_dataframe(data)
    dataframe.plot(x=x, y=y)
    plt.show()

def chart_word(word):
    x = 'date'
    y = word
    records = bata.db.get_all_analyzed_words_by_date(toRecords=True)
    prepared_records = records.prepare_word_count(word)
    data = records.map_fields(prepared_records, "date", word, sortByKey=True)
    show_chart(data, x, y)

chart_word("covid")


