from os import path

FILE_DIRECTORY = dir_path = path.dirname(path.realpath(__file__))

FAQ_LINKS = 'faq_links.txt'
COLLECTION_NAME = 'faq'
# ENABLE_CUSTOM_QUESTIONS_FILTER = "enable_custom_questions_filter"
ENABLE_CUSTOM_QUESTIONS_FILTER = True
CONFIG_FILE_NAME = "faq_scrapping_config.txt"
LINK = 'link'
TAGS = 'tags'
TITLE = 'title'
ANSWER = "a"
QUESTION_BLACK_LIST = path.join(FILE_DIRECTORY, "QuestionBlackList.txt")
