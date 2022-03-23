from distutils.debug import DEBUG
from typing import List
from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecretkey"

debug = DebugToolbarExtension(app)

survey = surveys['satisfaction']


@app.route('/')
def survey_start_page():
    """Bring user to start survey page"""
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html', title=title, instructions=instructions)


@app.route('/setup', methods=["POST"])
def survery_setup():
    """Setup session storage for responses"""
    session['responses'] = list()
    return redirect('/questions/0')


@app.route('/questions/<num>')
def survey_questions(num):
    """Handles logic for Get requests"""
    responses = session['responses']
    if len(responses) == int(num):
        question_obj = survey.questions[int(num)]
        question = question_obj.question
        choices = question_obj.choices
        return render_template('questions.html', num=num, question=question, choices=choices)
    elif len(responses) == len(survey.questions):
        return render_template('thankyou.html')
    else:
        flash("You can't access that question. Please answer the questions in order!")
        return redirect(f'/questions/{len(responses)}')


@app.route('/answer', methods=["POST"])
def survey_question_save():
    """Handles logic for Post requests"""
    responses = session['responses']
    answer = request.form['answer']
    responses.append(answer)
    session['responses'] = responses
    num = len(responses)
    if num < len(survey.questions):
        return redirect(f'/questions/{num}')
    else:
        return render_template('thankyou.html')
