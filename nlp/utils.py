"""
utils.py
Contains all the utility functions for our NLP tasks
"""
# for system path
import sys
import os

import spacy

# Sets the execution path
sys.path.insert(0, os.path.realpath('./'))

# Download: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


def get_word_clusters(lemmas, threshold):
    """
    Returns word clusters for the given lemmas.
    :param lemmas: map containing lemma and array of all the corresponding words pair
    :param threshold: similarity threshold based on which we have to merge the slots
    :return: lemma to slot map and word clusters map
    """
    lemma_to_slot_map = {}
    word_clusters = {}
    slot_count = 0
    for i1, lemma1_key in enumerate(lemmas):
        for i2, lemma2_key in enumerate(lemmas):
            if i1 < i2:
                if nlp(lemma1_key).similarity(nlp(lemma2_key)) > threshold:
                    if lemma1_key in lemma_to_slot_map:
                        if lemma2_key in lemma_to_slot_map:
                            word_clusters[lemma_to_slot_map[lemma1_key]]\
                                .append(word_clusters[lemma_to_slot_map[lemma2_key]])
                        else:
                            word_clusters[lemma_to_slot_map[lemma1_key]].extend(lemmas[lemma2_key])
                        lemma_to_slot_map[lemma2_key] = lemma_to_slot_map[lemma1_key]
                    elif lemma2_key in lemma_to_slot_map:
                        word_clusters[lemma_to_slot_map[lemma2_key]].extend(lemmas[lemma1_key])
                        lemma_to_slot_map[lemma1_key] = lemma_to_slot_map[lemma2_key]
                    else:
                        slot_name = "slot%d" % slot_count
                        lemma_to_slot_map[lemma1_key] = slot_name
                        lemma_to_slot_map[lemma2_key] = slot_name
                        word_clusters[slot_name] = lemmas[lemma1_key]
                        word_clusters[slot_name].extend(lemmas[lemma2_key])
                        slot_count += 1
    return lemma_to_slot_map, word_clusters


if __name__ == '__main__':
    """
    dry run doing basic testing the defined functions
    """
    thres = 0.5
    lemma_dict = \
        {
            'cat': ['cats', 'cat'],
            'dog': ['dogs', 'dog']
        }
    lemma_slot, clusters = get_word_clusters(lemma_dict, thres)
    print('lemma_slot_map:', lemma_slot)
    print('word_clusters:', clusters)
