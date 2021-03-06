# -*- coding: UTF-8 -*-
from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired
import sys
import os
import re
path = '/home/project-01/PUG/project-1/webapp/WebApp'
sys.path.append(os.path.abspath('../../algo/parse_sentence_end'))
if path not in sys.path:
   sys.path.insert(0, path)
from EndParser import parse_sentence_end, parse_sentence_init
parse_sentence_init()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
CsrfProtect(app)
from app import app as application

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
    #parse_sentence_init()
    app.run(host='0.0.0.0', port=8790, debug=True)
