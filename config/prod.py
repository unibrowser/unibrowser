from os import path

# We are assuming the script is run from the top level directory (unibrowser source repo root)
ETC = path.realpath('./etc')

DATABASE_CONFIG = {
    'host': 'mongo-db',
    'dbname': 'unibrowser',
    'port': 27017
}

PROFESSOR_CONFIG = {
    'structure': path.join(ETC, 'prof_input_structure.json')
}

FAQ_CONFIG = {
    'db_collection': 'faq',
    'enable_custom_questions': True,
    'links': path.join(ETC, 'faq_links.txt'),
    'black_list': path.join(ETC, "QuestionBlackList.txt")
}

TWITTER_CONFIG = {
    'consumer_key': "",
    'consumer_secret': "",
    'access_key': "",
    'access_secret': ""
}

FREE_FOOD_CONFIG = {
    'username': "@okstatefood",
    'max_tweets': 199,
    'date_select': {
        'today_list': ['noon', 'morning', 'today', 'tonight', 'this evening'],
        'tomorrow_list': ['tomorrow', 'next day']
    }
}
