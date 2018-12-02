from os import path

# We are assuming the script is run from the top level directory (unibrowser source repo root)
ETC = path.realpath('./etc')

DATABASE_CONFIG = {
    'host': 'mongo-test-db',
    'dbname': 'unibrowser',
    'port': 27017
}

PROFESSOR_CONFIG = {
    'structure': path.join(ETC, 'prof_input_structure.json'),
    'db_collection': 'professor'
}

FAQ_CONFIG = {
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
    'username': ["@eatfreeOSU"],
    'max_tweets': 199,
    'date_select': {
        'today_list': ['noon', 'morning', 'today', 'tonight', 'this evening'],
        'tomorrow_list': ['tomorrow', 'next day']
    }
}

EVENT_CONFIG = {
    'db_collection': 'events'
}

SPORTS_CONFIG = {
    'links': path.join(ETC, 'sport-links.txt')
}

BUS_CONFIG = {
    'db_collection': 'locations',
    'config_file': path.join(ETC, 'bus-config.json'),
    'lat_lng_info_file': path.join(ETC, 'lat-lng-info.json')
}
