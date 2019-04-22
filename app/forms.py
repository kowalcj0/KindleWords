# -*- coding: utf-8 -*-
from flask_uploads import TEXT, UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, TextAreaField
from wtforms.validators import DataRequired

from app import app


class WordsForm(FlaskForm):
    placeholder = (
        "Enter a list of comma-separated english words, e.g.: bird, kindle, candles"
    )
    words = TextAreaField(
        "words", validators=[DataRequired()], render_kw={"placeholder": placeholder}
    )


clippings = UploadSet("clippings", TEXT)
configure_uploads(app, (clippings,))


class ClippingsForm(FlaskForm):
    placeholder = "Select you Kindle `clippings.txt` file"
    clippings = FileField(
        "clippings",
        validators=[FileRequired(), FileAllowed(clippings, "*.txt files only!")],
        description=placeholder,
    )
