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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
CsrfProtect(app)


@app.route('/result')
def post_words():
    with open("./static/FakeData.json") as load_f:
        views = json.load(load_f)
        numbers = len(views[u'views'])
    return render_template('submit_pages.html', views_items=zip(range(numbers), views[u'views']))


@app.route('/', methods=['GET', 'POST'])
def input_form():
    form2 = InputForm()
    if form2.validate_on_submit():
        if form2.clear.data:
            form2.content.data = None
        elif form2.submit.data:
            return redirect('/result')
    return render_template('input_pages.html', form2=form2)


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
