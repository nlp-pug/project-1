# -*- coding: UTF-8 -*-
from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired
import json
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
import sys, os
sys.path.append(os.path.abspath('../parse_sentence_start'))
sys.path.append(os.path.abspath('../parse_sentence_end'))
from core_nlp import NewsParser

from EndParse import parse_sentence_end

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
CsrfProtect(app)

class SimluationFunc:
    def inputtext(self, text):
        if text:
            return

    def outputresult(self):
        sampledata = [{'author': 'Author1', 'content': 'sample1'}, {'author': 'Author2', 'content': 'Sample2'},
                      {'author': 'Author3', 'content': 'Sample3'}, {'author': 'Author4', 'content': 'Sample4'}]
        return sampledata

sf = SimluationFunc()


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

            print(split_sentences, form2.content.data)
            sf.inputtext(text=form2.content.data)
            return redirect('/result')
    return render_template('input_pages.html', form2=form2)


@app.route('/result')
def post_words():
    views = sf.outputresult()
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
