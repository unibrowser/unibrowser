import json
import re
import nltk
from nltk.corpus import stopwords
from database.mongoclientclass import MongoClientClass
from config import FAQ_CONFIG

LINK = 'link'
TAGS = 'tags'
TITLE = 'title'
ANSWER = "a"


def stripExtra(text):
    rep = {"\t": "", "\n": ""}  # define desired replacements here
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text


def getTags(sentence):
    clean_text = re.sub(r'[^\w\s]', '', sentence)

    sw = stopwords.words('english')
    tagsList = []
    for text in clean_text.split():
        tokenized = nltk.word_tokenize(text)
        tokens = [t for t in tokenized if t not in sw]
        if len(tokens) > 0:
            tagsList.extend(tokens)
    return tagsList

# print(getTags("Hello my name is Anand?"))


def convertToJsonList(link, questions, answerList):
    jsonDataList = []
    tagsList = getTags(questions)
    for i in range(0, len(questions)):
        data = {}
        question = questions[i]
        answer = answerList[i]
        nouns = getTags(question)

        data[LINK] = link
        data[TAGS] = tagsList[i]
        data[TITLE] = question
        data[ANSWER] = answer
        print(data)
        jsonDataList.append(data)
    return jsonDataList


def saveToMongo(jsonList, FAQ):
    try:
        mongo_client_instance = MongoClientClass()
        mongo_client_instance.insert(collection=FAQ, documents=jsonList)
    except Exception as e:
        print(e)
        print("inside save_prof_data: 0 (exception)")
        return 0
    print("inside save_prof_data: 1 (success)")
    return 1

# def checkConfigForFlag(key):
#     with open(CONFIG_FILE_NAME, 'r') as myfile:
#         lines = myfile.read().split("\n")
#
#     for line in lines:
#         if line.find(key) != -1:
#             k, v = line.split('=')
#             return v
#     return False


def getBlackListedQuestions():
    with open(FAQ_CONFIG['black_list'], 'r') as myfile:
        return myfile.read().split("\n")


def removeBlackListedQuestions(questions, blackListedQuestions):
    #     print(questions)
    for blackListedQuestion in blackListedQuestions:
        for i in range(len(questions) - 1, -1, -1):
            question = questions[i]
            if blackListedQuestion == question:
                questions.remove(blackListedQuestion)


def removeDuplicates(questionList):
    seen = set()
    result = []
    for item in questionList:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# def saveJsonToFile(jsonDataList, fileName):
#     with codecs.open(fileName, 'ab', encoding='utf-8') as f:
#         for data in jsonDataList:
#             json.dump(data, f, ensure_ascii=False)
#         f.close()
