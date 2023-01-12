from F import LIST, DICT, DATE
from F.LOG import Log


#
def add_word_frequency_counts(brain_scores:list, new_scores:dict) -> list:
    """ Add two dicts of word counts together
    brain_scores: [{"word":, "count":}, {"word":, "count":}]
    new_scores: { "word":, "count": }
    """
    result = []

    """ Part 1. Preparing... """
    # All New Scored Words
    new_score_words = []
    for word in new_scores.keys():
        new_score_words.append(word)

    # All Brain Words
    brain_score_words = []
    if brain_scores:
        for item in brain_scores:
            brain_word = DICT.get("word", item, None)
            brain_score_words.append(brain_word)

    new_words = []
    for new_scored_word in new_score_words:
        if new_scored_word in brain_score_words:
            continue
        new_words.append(new_scored_word)

    """ Part 2. Merging with Brain... """
    if brain_scores:
        for brain_item in Log.ProgressBarYielder(brain_scores, "Calculating brain counts..."):
            brain_word = DICT.get("word", brain_item, None)
            brain_count = DICT.get("count", brain_item, None)
            if new_scores.__contains__(brain_word):
                ns = int(new_scores[brain_word])
                new_score = int(brain_count) + ns
                brain_item["count"] = new_score
                brain_item["updatedDate"] = DATE.TODAY
                result.append(brain_item)
                continue
            result.append(brain_item)

    """ Part 3. If new words, add them to brain... """
    if new_words:
        for new_word in Log.ProgressBarYielder(new_words, "Adding new words to brain..."):
            new_item = {"word": new_word, "count": new_scores[new_word], "updatedDate": DATE.TODAY}
            result.append(new_item)

    return result


def add_word_counts(scores_one:dict, scores_two:dict) -> dict:
    """ Add two dicts of word counts together
    brain_scores: {"word":, "count":}
    new_scores: { "word":, "count": }
    """
    result = {}

    """ Part 1. Preparing... """
    # All New Scored Words
    scores_one_list = []
    for word in scores_one.keys():
        scores_one_list.append(word)

    scores_two_list = []
    for word in scores_two.keys():
        scores_two_list.append(word)

    new_words = []
    for new_scored_word in scores_two_list:
        if new_scored_word in scores_one_list:
            continue
        new_words.append(new_scored_word)

    """ Part 2. Merging with Brain... """
    if scores_one_list:
        for scores_one_word in Log.ProgressBarYielder(scores_one, "Calculating brain counts..."):
            scores_one_count = DICT.get(scores_one_word, scores_one, None)
            if scores_two.__contains__(scores_one_word):
                scores_two_count = DICT.get(scores_one_word, scores_two, None)
                new_score = int(scores_one_count) + int(scores_two_count)
                result[scores_one_word] = new_score
                continue
            result[scores_one_word] = scores_one_count

    """ Part 3. If new words, add them to brain... """
    if new_words:
        for new_word in Log.ProgressBarYielder(new_words, "Adding new words to brain..."):
            result[new_word] = scores_two[new_word]

    return result