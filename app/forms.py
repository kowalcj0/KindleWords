from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired

class WordsForm(FlaskForm):
    placeholder =  "Enter a list of comma-separated english words, e.g.: bird, kindle, candles"
    words = TextAreaField(
        'words',
        validators=[DataRequired()],
        render_kw={"placeholder": placeholder})
