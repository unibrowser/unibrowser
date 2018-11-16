import re
import httplib2
from bs4 import BeautifulSoup
from scraping.faqscraperutil import stripExtra, removeDuplicates, removeBlackListedQuestions, getBlackListedQuestions, convertToFaqList, saveToMongo
from config import FAQ_CONFIG


def cleanQuestions(questions):
    questionList = []
    for question in questions:
        questionList.append(stripExtra(question.lstrip().rstrip()))

    return removeDuplicates(questionList)


def getLastAnswer(question, bodyText):
    start = bodyText.index(question) + len(question)
    text = bodyText[start: -1].lstrip()
#     print(text.lstrip())
    whitespaceCount = 0
#     print(answerLength)
    for i in range(0, len(text)):
        #         print(answer[i], ' isSpace : ', answer[i].isspace())
        if text[i].isspace():
            whitespaceCount = whitespaceCount + 1
            if whitespaceCount >= 3:
                #                 print(0 + i - 3)
                #                 print(text[0 : 0 + i - 2])
                return text[0: 0 + i - 2]
        else:
            if whitespaceCount != 0:
                whitespaceCount = 0


def cleanAnswer(answer):
    answerLength = len(answer)
    whitespaceCount = 0
#     print(answerLength)
    for i in range(0, answerLength):
        #         print(answer[i], ' isSpace : ', answer[i].isspace())
        if answer[i].isspace():
            whitespaceCount = whitespaceCount + 1
            if whitespaceCount >= 3:
                #                 print(0 + i - 3)
                return answer[0: 0 + i - 2].lstrip()
        else:
            if whitespaceCount != 0:
                whitespaceCount = 0
    return answer.rstrip()


def getAnswers(body, questions):
    bodyText = body.getText()
#     answerTag = getAnswerTag(body, bodyText, questions)
#     print(bodyText)
    questionCount = len(questions)
    answerList = []
    for i in range(0, questionCount):
        print('Q: ', questions[i])
        if i == questionCount - 1:
            # Last element
            answer = getLastAnswer(questions[i], bodyText)
        else:
            start = bodyText.index(questions[i]) + len(questions[i])
            end = bodyText.index(questions[i + 1], start, -1)
            print("Start : ", start, " End : ", end)
            soup1 = BeautifulSoup(bodyText[start: end], 'html.parser')
#             print(soup1)
            answer = soup1.getText().lstrip()

        answer = cleanAnswer(answer)
        answerList.append(answer)
        print('A: ', answer)
    return answerList


def processWithCustomQuestions(questions):
    #     isCustomQuestionsEnabled = checkConfigForFlag(ENABLE_CUSTOM_QUESTIONS_FILTER)
    #     print("isCustomQuestionsEnabled : ", isCustomQuestionsEnabled)
    if FAQ_CONFIG['enable_custom_questions'] == False:
        return
    blackListedQuestions = getBlackListedQuestions()
    removeBlackListedQuestions(questions, blackListedQuestions)
    print(questions)


def getFaqOfLink(link):
    #     print("LINK : ", link)
    http = httplib2.Http()
    status, html = http.request(link)
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    questions = cleanQuestions(soup(text=re.compile(
        r'\s*((?:how|How|Can|can|what|What|where|Where|describe|Describe|Who|who|When|when|Why|why|Should|should|is|Is|I|Do|do|Are|are|Will|will)[^.<>?]*?\s*\?)')))
#     print(questions)
    processWithCustomQuestions(questions)
    answerList = getAnswers(body, questions)
    return questions, answerList

# link = "https://transportation.oregonstate.edu/aabc/frequently-asked-questions"
# questions, answerList = getFaqOfLink(link)


if __name__ == "__main__":
    links = FAQ_CONFIG['links']
    with open(links, 'r') as myfile:
        FAQ_LINKS = myfile.read().split('\n')

    faqJsonList = []
    for i in range(0, len(FAQ_LINKS)):
        link = FAQ_LINKS[i]
        questions, answerList = getFaqOfLink(link)
        jsonList = convertToFaqList(link, questions, answerList)
        faqJsonList.extend(jsonList)

#     saveJsonToFile(faqJsonList, "output.txt")
    saveToMongo(faqJsonList)
