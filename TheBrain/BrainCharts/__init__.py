import pandas as pd
import matplotlib.pyplot as plt
from TheBrain.BrainDB.BrainData import BrainData

bata = BrainData()
records = bata.db.get_all_analyzed_words_by_date(toRecords=True)

WORD = "facebook"

test = records.prepare_word_count(WORD)
data = records.map_fields(test, "date", WORD, sortByKey=True)

df = pd.DataFrame(data)
df.plot(x='date', y=WORD)
plt.show()
