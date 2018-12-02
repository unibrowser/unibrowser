"""
utils.py
Contains all the utility functions for our NLP tasks
"""
# for system path
import sys
import os
# Sets the execution path
sys.path.insert(0, os.path.realpath('./'))

import spacy
from pymongo import MongoClient
import datetime
import random

# Download: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

client = MongoClient('mongodb://localhost:27017')
db = client['unibrowser']


def get_faq_data(collection_name):
    """Get faq data from db"""
    data = []
    collection = db[collection_name]
    for entry in collection.find():
        data.append(entry['title'])
        data.append(entry['answer'])
    return data


def get_lemmatize_dict(sentences):
    """
    Finds noun phrases from the data, generates lemmas and returns a lemma to word cluster map.
    """
    lemmatize_text_dict = {}
    lemma_set = {}
    for sentence in sentences:
        # function to test if something is a noun
        doc = nlp(sentence)
        for chunk in doc.noun_chunks:
            if chunk.root.text not in lemma_set:
                lemma_set[chunk.root.text] = set()
            lemma_set[chunk.root.text].add(chunk.text)
    for lemma, phrases in lemma_set.items():
        if len(phrases) > 10:
            lemmatize_text_dict[lemma] = random.sample(list(phrases), 10)
    return lemmatize_text_dict


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
                        word_clusters[lemma_to_slot_map[lemma1_key]] = \
                            random.sample(word_clusters[lemma_to_slot_map[lemma1_key]], 10)
                        lemma_to_slot_map[lemma2_key] = lemma_to_slot_map[lemma1_key]
                    elif lemma2_key in lemma_to_slot_map:
                        word_clusters[lemma_to_slot_map[lemma2_key]].extend(lemmas[lemma1_key])
                        word_clusters[lemma_to_slot_map[lemma2_key]] = \
                            random.sample(word_clusters[lemma_to_slot_map[lemma2_key]], 10)
                        lemma_to_slot_map[lemma1_key] = lemma_to_slot_map[lemma2_key]
                    else:
                        slot_name = "slot%d" % slot_count
                        lemma_to_slot_map[lemma1_key] = slot_name
                        lemma_to_slot_map[lemma2_key] = slot_name
                        word_clusters[slot_name] = lemmas[lemma1_key]
                        word_clusters[slot_name].extend(lemmas[lemma2_key])
                        word_clusters[slot_name] = random.sample(word_clusters[slot_name], 10)
                        slot_count += 1
                else:
                    if lemma1_key not in lemma_to_slot_map:
                        slot_name = "slot%d" % slot_count
                        slot_count += 1
                        word_clusters[slot_name] = []
                        lemma_to_slot_map[lemma1_key] = slot_name
                    word_clusters[lemma_to_slot_map[lemma1_key]].extend(lemmas[lemma1_key])
                    word_clusters[lemma_to_slot_map[lemma1_key]] = \
                            random.sample(word_clusters[lemma_to_slot_map[lemma1_key]], 10)
                    if lemma2_key not in lemma_to_slot_map:
                        slot_name = "slot%d" % slot_count
                        slot_count += 1
                        word_clusters[slot_name] = []
                        lemma_to_slot_map[lemma2_key] = slot_name
                    word_clusters[lemma_to_slot_map[lemma2_key]].extend(lemmas[lemma2_key])
                    word_clusters[lemma_to_slot_map[lemma2_key]] = \
                        random.sample(word_clusters[lemma_to_slot_map[lemma2_key]], 10)
    return lemma_to_slot_map, word_clusters


def save_faq_slots(lemma_slot, word_clusters):
    """
    save faq slot and word clusters in db
    :param lemma_slot: lemma to slot map
    :param word_clusters: slot-name to list of words
    :return: 1 when it is able to save the results.
    """
    lemmas = [{'lemma_name': lemma_name, 'slot_name': slot_name} for lemma_name, slot_name in lemma_slot.items()]
    clusters = [{'slot_name': slot_name, 'words': words} for slot_name, words in word_clusters.items()]
    db['faq-word-clusters'].insert_many(clusters)
    db['faq-lemmas-slots'].insert_many(lemmas)
    return 1


if __name__ == '__main__':
    """
    dry run doing basic testing the defined functions
    """
    faqs = get_faq_data('faq')
    print('faqs:', faqs)
    lemma_text_dict = get_lemmatize_dict(faqs)
    print('lemmas:', lemma_text_dict)
    thres = 0.8
    print(datetime.datetime.now())
    lemma_slot, clusters = get_word_clusters(lemma_text_dict, thres)
    print('lemma_slot_map:', lemma_slot)
    print('word_clusters:', clusters)
    save_faq_slots(lemma_slot, clusters)
