from flask_wtf import FlaskForm
from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    SubmitField,
    validators,
)
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class CreateContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")
