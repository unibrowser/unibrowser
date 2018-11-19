import unittest
from scraping.faqscraperutil import stripExtra, getTags, convertToFaqList, saveToMongo
import api.faqs as faq_api

faq = faq_api.Faq(
    title="I am the parent of a student coming to Oregon State. Can I apply for housing for them?",
    link="https://uhds.oregonstate.edu/faq",
    answer="All residents must apply for housing themselves, unless they require assistance in the process. Since they will be the ones living with us, we encourage students to complete their own housing application and roommate profile.",
    tags=['I', 'parent', 'student', 'coming', 'Oregon', 'State', 'Can', 'I', 'apply', 'housing']
)


class testingscraping(unittest.TestCase):

    def test_strip_extra(self):
        text = "When can I seek \nadmission?\t\t"
        self.assertTrue(stripExtra(text) == "When can I seek admission?")

    def test_get_tags(self):
        text = "When can I seek admission?"
        self.assertTrue(getTags(text) == ['When', 'I', 'seek', 'admission'])

    def test_convert_to_json_list(self):
        link = "https://uhds.oregonstate.edu/faq"
        questionList = ["I am the parent of a student coming to Oregon State. Can I apply for housing for them?"]
        answerList = ["All residents must apply for housing themselves, unless they require assistance in the process. Since they will be the ones living with us, we encourage students to complete their own housing application and roommate profile."]
        # attrs = vars(faq)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        self.assertTrue(convertToFaqList(
            link, questionList, answerList)[0].link == faq.link and convertToFaqList(
            link, questionList, answerList)[0].answer == faq.answer and convertToFaqList(
            link, questionList, answerList)[0].title == faq.title and convertToFaqList(
            link, questionList, answerList)[0].tags == faq.tags)

    def test_save_to_mongo(self):
        self.assertEqual(saveToMongo([faq]), 1)


if __name__ == '__main__':
    unittest.main()
