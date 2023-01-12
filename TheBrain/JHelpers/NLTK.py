import re
import F.LIST
from FNLP.Language import Sentences, Words
import FairResources
from F.LOG import Log
from FA.Categories import Topics

Log = Log("Engine.NLTK")

stop_words = FairResources.get_stopwords()
WEIGHTED_TERMS = Topics.ALL_CATEGORIES().get_all_weighted_terms()

def get_content_sentiment(content) -> {}:
    """ Sentiment of Content. """
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    vader = SentimentIntensityAnalyzer()
    all_weighted_terms = WEIGHTED_TERMS
    vader.lexicon.update(all_weighted_terms)
    score = vader.polarity_scores(content)
    Log.v("get_content_sentiment:", score)
    return score

def split_words(text):
    """ ALTERNATIVE: Split a string into array of words. """
    try:
        text = re.sub(r'[^\w ]', '', text)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        return None

"""
- Check for Nouns or Capital letters to better score sentences
- Check for "but" as it would imply a counter argument.
- 
"""

SUMMARY = lambda first, middle, last: f"{first} {middle} {last}"

# -> master summarizer!
def summarize_v2(content='', max_sents=5):
    if not content or max_sents <= 0:
        return []
    keepList = []
    # Pre. -> Convert raw string of text into a List of Sentences.
    sentences = Sentences.to_sentences(content)
    # sentences = tokenize_content_into_sentences(content)
    # test = Language.__compare(sent_test, sentences)
    if not sentences:
        return False
    # 1. -> If only 6 or less sentences to start, return now
    if len(sentences) <= 6:
        return Words.combine_words(sentences)
    # 2. -> Always use the first and last sentence
    firstSentence = F.LIST.get(0, sentences, False)
    if not firstSentence:
        return False
    lastIndex = len(keepList) - 1
    lastSentence = F.LIST.get(lastIndex, sentences, False)
    if len(lastSentence) <= 50:
        lastSentence = F.LIST.get(lastIndex - 1, sentences, False)
    # 3. -> Remove First and Last Sentence
    without_first = F.LIST.remove_index(0, sentences)
    without_first_and_last = without_first[:-1]
    # 4. -> Filter out by length
    for sen in without_first_and_last:
        l = len(sen)
        if 50 < l > 400:
            continue
        keepList.append(sen)
    # 5. -> Section off list into three parts.
    #           - Beginning, Middle, End.
    base_count = int(len(keepList) / 3)
    middle_count = base_count * 2
    first = keepList[:base_count]
    middle = keepList[base_count:middle_count]
    last = keepList[middle_count:]
    # 6. -> Score each Section
    first_scored = Topics.ALL_CATEGORIES().score_categorizer(first)
    middle_scored = Topics.ALL_CATEGORIES().score_categorizer(middle)
    last_scored = Topics.ALL_CATEGORIES().score_categorizer(last)
    # 7. -> Filter/Select highest scored sentences from each Section.
    first_summary = form_summary_v3(first_scored, 1)
    middle_summary = form_summary_v3(middle_scored, 1)
    last_summary = form_summary_v3(last_scored, 1)
    # 8. -> Combine all 3 Sections into 1 Single Body of Text.
    combined_summary = Words.combine_words(first_summary, middle_summary, last_summary)
    # 9. -> Combine the first sentence, the middle body and the last sentence to form "The_Summary"
    The_Summary = SUMMARY(firstSentence, combined_summary, lastSentence)
    return The_Summary

def form_summary_v3(scored_sentences: [], max_sent=5):
    final_list = []
    total_count = len(scored_sentences) - 1
    current_index = 0
    sorted_scored_sentences = sorted(scored_sentences, key=lambda lst: lst[0], reverse=True)
    while current_index <= total_count:
        if len(final_list) >= max_sent:
            break
        raw_sent = F.LIST.get(current_index, sorted_scored_sentences)
        sent = F.LIST.get(1, raw_sent)
        # - Finish up
        final_list.append(sent)
        current_index += 1
    the_summary = Words.combine_words(final_list)
    return the_summary

def keywords(content):
    """Get the top 10 keywords and their frequency scores ignores blacklisted
    words in stopwords, counts the number of occurrences of each word, and
    sorts them in reverse natural order (so descending) by number of
    occurrences.
    """
    NUM_KEYWORDS = 10
    content = split_words(content)
    # of words before removing blacklist words
    if content:
        num_words = len(content)
        content = [x for x in content if x not in stop_words]
        freq = {}
        for word in content:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1

        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)
        for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()

if __name__ == '__main__':
    test = "Mr. John Johnson Jr. was born in the U.S.A but earned his Ph.D. in Israel before joining Nike Inc. as an engineer. He also worked at craigslist.org as a business analyst."
    summary = summarize_v2(test, 2)
    print(summary)