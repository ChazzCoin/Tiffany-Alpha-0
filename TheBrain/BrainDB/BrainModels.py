from F import DATE
from FM.QueryHelper import O

"""
1. Words Analyzed
2. Webpages Analyzed
3. Stop Words Analyzed
4. Sentences Analyzed
5. Words Analyzed by Date
"""

CONTENT_MODEL = lambda content, date: {"content": content, "date": date}
ANALYZED_WEBPAGE_MODEL = lambda webpage_id, webpage_date: { "_id": O.OBJECT_ID(webpage_id), "webpage_date": webpage_date, "updatedDate": DATE.TODAY}
GLOBAL_STATISTICS_MODEL = lambda word_count, highest_counted_word, highest_count, lowest_counted_word, lowest_count: { "word_count":word_count,
                                                                                                                "highest_counted_word":highest_counted_word,
                                                                                                                "highest_count":highest_count,
                                                                                                                "lowest_counted_word": lowest_counted_word,
                                                                                                                "lowest_count": lowest_count }

ANALYZED_WORDS_MODEL = lambda word, count: {"word": word, "count": count, "updatedDate": DATE.TODAY}
ANALYZED_STOP_WORDS_MODEL = lambda word, count: {"word": word, "count": count, "updatedDate": DATE.TODAY}
ANALYZED_SENTENCES_MODEL = lambda sentence, sentence_date: {"sentence": sentence, "sentence_date": sentence_date, "updatedDate": DATE.TODAY}
ANALYZED_WORDS_BY_DATE = lambda webpage_date, word_counts, words_counted: {"date": webpage_date, "word_counts": word_counts, "words_counted": words_counted, "updatedDate": DATE.TODAY}
