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
import pymongo
from pymongo import MongoClient
# from config.prod import DATABASE_CONFIG

# Download: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

client = MongoClient('mongodb://localhost:27017')
db = client['unibrowser']

def get_question_data(collection_name):
    questions = []
    answers = []
    collection = db[collection_name]
    for entry in collection.find():
        questions.append(entry['title'])
        answers.append(entry['answer'])
    return questions, answers

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

	
def lemmatize_text(noun_phrases):
    """
    Returns lemmatized text for the passed noun phrases.
    :noun phrase: list of noun phrases 
    :return: lemmatized text
    """
    lemmatize_text_dict = {}
    for each_noun_phrase in noun_phrases:
        lemma_val = []
        doc = nlp(each_noun_phrase) 

        for chunk in doc.noun_chunks:
            key = chunk.root.text
            if key in lemmatize_text_dict:
                lemma_val=lemmatize_text_dict[key]
            lemma_val.append(chunk)        
            lemmatize_text_dict[chunk.root.text] = lemma_val      
    return lemmatize_text_dict


if __name__ == '__main__':
    """
    dry run doing basic testing the defined functions
    """
    question, answer = get_question_data('faq')

    noun_phrases = \
        ["smelly cats","pink cats","funny dogs","natural language processing","computer processing"]
    lemma_text_dict = lemmatize_text(noun_phrases)
    print(lemma_text_dict)
    
    thres = 0.5
    lemma_dict = \
        {
            'cat': ['cats', 'cat'],
            'dog': ['dogs', 'dog']
        }
    lemma_slot, clusters = get_word_clusters(lemma_dict, thres)
    print('lemma_slot_map:', lemma_slot)
    print('word_clusters:', clusters)

