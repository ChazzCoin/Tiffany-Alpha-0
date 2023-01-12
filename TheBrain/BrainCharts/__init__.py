import pandas as pd
import matplotlib.pyplot as plt
from F import DICT, LIST, CONVERT
from TheBrain.BrainDB.BrainData import BrainData
from FNLP.Language import Words

bata = BrainData()
all = bata.db.get_all_analyzed_words_by_date()

WORD = "facebook"

a = {}
all_count = len(all)
divide_number = int(all_count / 2)
count = all_count / divide_number
i = 0
for item in all:
    date = DICT.get("date", item, None)
    word_counts = DICT.get("word_counts", item, None)
    capital = Words.make_capital(WORD)
    word_count = DICT.get(capital, word_counts, 0)
    word_count2 = DICT.get(str(WORD).lower(), word_counts, 0)
    if not word_count or not date or str(date) == "Unknown":
        continue
    keyName = str(date)
    a[keyName] = int(word_count) + int(word_count2)
    i += 1



def map_dict(dic:dict, keyField:str, valueField:str, sortByKey=True):
    if sortByKey:
        dic = DICT.SORT_BY_KEY(dic, False)
    keyList = CONVERT.dict_TO_List_OF_Keys(dic)
    valueList = CONVERT.dict_TO_List_OF_Values(dic)
    mapped = { keyField: keyList, valueField: valueList }
    return mapped

# ws = CONVERT.dict_TO_List_OF_Values(ab)
# ds = CONVERT.dict_TO_List_OF_Keys(a)

data = map_dict(a, "date", WORD)



df = pd.DataFrame(data)
df.plot(x='date', y=WORD)
plt.show()
