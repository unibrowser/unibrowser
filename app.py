# app.py
from flask import Flask, request, url_for, send_from_directory, render_template
from scraping.faqscraperutil import convertToJsonList, saveToMongo
import re

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/feedqa', methods=['GET', 'POST'])
    def feedQA():
        if request.method == 'GET':
            return render_template("feedqa.html")
        elif request.method == 'POST':
            link=""; questions=[]; answers=[]
            link = request.form["link"]
            isQuestion = re.compile(r"questions")
            isAnswer = re.compile(r"answers")
            for key, value in request.form.items():
                print(key, value)
                if isQuestion.match(key) is not None: questions = value.split(",")
                if isAnswer.match(key) is not None: answers = value.split(",")
            jsonList = convertToJsonList(link, questions, answers)
            saveToMongo(jsonList, "faq")
            return render_template("feedqa.html")
    return app

    @app.route('/success')
    def showSuccess():
        return "Success!"






if __name__ == '__main__':
    app = create_app()
