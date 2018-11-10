import unittest
from scraping.faqscrapper import cleanQuestions, getLastAnswer, cleanAnswer, getAnswers, getFaqOfLink 

class testingscraping(unittest.TestCase):
    def test_instance_working(self):
        #This particular faq page has 8 question & answers
        url = "https://engineering.oregonstate.edu/frequently-asked-questions"
        
        # unit test cleanQuestions()
        question = "   When can I seek \nadmission"
        questionList = []
        questionList.append(question)
        self.assertTrue(cleanQuestions(questionList)[0] == "When can I seek admission")
        
        # unit test for cleanAnswer()
        answer = "Admissions start on the 12th of December.        </div>   "
        questionList.append(question)
        self.assertTrue(cleanAnswer(answer) == "Admissions start on the 12th of December.")  
        
        # unit test for getFaqOfLink(), getAnswers(), getLastAnswer()
        questions, answerList = getFaqOfLink(url)
        self.assertTrue(len(questions) == 8 and len(answerList) == 8)  
        
if __name__ == '__main__':
    unittest.main()