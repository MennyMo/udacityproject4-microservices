from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField

class PredictionForm(FlaskForm):
    CHAS = FloatField('CHAS')
    RM = FloatField('RM')
    TAX = FloatField('TAX')
    PTRATIO = FloatField('PTRATIO')
    B = FloatField('B')
    LSTAT = FloatField('LSTAT')
    submit = SubmitField('submit')