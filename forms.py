from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    link = StringField("Link", validators=[DataRequired()])
    submit = SubmitField("Save Changes")


class AboutForm(FlaskForm):
    about_text = TextAreaField("About Text", validators=[DataRequired()])


class StatusForm(FlaskForm):
    status_text = TextAreaField("Status Message", validators=[DataRequired()])
