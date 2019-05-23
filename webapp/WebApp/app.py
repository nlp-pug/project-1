# -*- coding: UTF-8 -*-
from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired
import sys
import os
import re

sys.path.append(os.path.abspath('../../algo/parse_sentence_end'))
from EndParser import parse_sentence_end

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
CsrfProtect(app)

# Externally Visible Server
# flask run --host=0.0.0.0

# for test:
# def parse_sentence_end(text):
#     if text:
#         sampledata = [{'author': 'Lucy', 'content': 'Hahaha'}, {'author': 'Author2', 'content': 'Sample2'},
#                       {'author': 'Author3', 'content': 'Sample3'}, {'author': 'Author4', 'content': 'Sample4'}]
#         return sampledata

# sf = SimluationFunc()
parse_result = None


@app.route('/', methods=['GET', 'POST'])
def input_form():
    form2 = InputForm()
    if form2.validate_on_submit():
        if form2.clear.data:
            form2.content.data = None
        elif form2.submit.data:
            # get output data from parse_end

            split_sentences = form2.content.data.replace("\r", "")
            split_sentences = split_sentences.replace("\n", "")
            split_sentences = re.split('。|！|？', split_sentences)


            print(form2.content.data)
            # sf.inputtext(text=form2.content.data)
            global parse_result
            parse_result = parse_sentence_end(text=form2.content.data)

            return redirect('/result')
    return render_template('input_pages.html', form2=form2)


@app.route('/result')
def post_words():

    # views = sf.outputresult()
    views = parse_result

    numbers = len(views)
    print(len(views), views)

    # From the File
    # with open("./static/FakeData.json") as load_f:
    #     views = json.load(load_f)
    #     numbers = len(views[u'views'])
    return render_template('submit_pages.html', views_items=zip(range(numbers), views))


class InputForm(FlaskForm):
    content = TextAreaField('Text Input', validators=[DataRequired()])
    submit = SubmitField('submit')
    clear = SubmitField('clear')


class RadioForm(FlaskForm):
    example = RadioField('Label', choices=[('sample_input', 'Sample1'), ('sample_input', 'Sample2'),
                                           ('sample_input', 'Sample3'), ('sample_input', 'Sample4'),
                                           ('sample_input', 'Sample5')])


if __name__ == '__main__':
    app.run()
