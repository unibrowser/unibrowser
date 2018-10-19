import re
import json
import nltk
import codecs
from nltk.corpus import stopwords
from database.mongoclientclass import MongoClientClass


# def readFile(fileName):
#     with open(fileName, 'r') as myfile:
#         return myfile.read()
    
def stripExtra(text):
    rep = {"\t": "", "\n": ""} # define desired replacements here
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text

def getTags(textList):
    is_noun = lambda pos: pos[:2] == 'NN'
    sw = stopwords.words('english')
    tagsList = []
    for text in textList:
        tokenized = nltk.word_tokenize(text)
        tokens = [t for t in tokenized if t not in sw]
        tagsList.append(tokens)
    return  tagsList

def convertToJsonList(link, questions, answerList):
    jsonDataList = []
    tagsList = getTags(questions)
    for i in range(0, len(questions)):
        data = {}
        question = questions[i]
        answer = answerList[i]
        nouns = getTags(question)
        data['link'] = link
        data['tags'] = tagsList[i]
        data['title'] = question
        data['a'] = answer
        print(data)
        jsonDataList.append(data)
    return jsonDataList

def saveToMongo(jsonList, collectionName):
    try: 
        mongo_client_instance = MongoClientClass(host='localhost', port=27017, db = 'unibrowser')
        mongo_client_instance.insert(collection = collectionName, documents = jsonList)
    except Exception as e:
        print(e)
        print("inside save_prof_data: 0 (exception)")
        return 0
    print("inside save_prof_data: 1 (success)")
    return 1

# def saveJsonToFile(jsonDataList, fileName):
#     with codecs.open(fileName, 'ab', encoding='utf-8') as f:
#         for data in jsonDataList:
#             json.dump(data, f, ensure_ascii=False)           
#         f.close()