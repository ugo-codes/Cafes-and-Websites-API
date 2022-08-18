from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AddCafeForm(FlaskForm):
    cafe = StringField(label="Cafe Name", validators=[DataRequired()])
    map_url = StringField(label="Map URL", validators=[DataRequired()])
    img_url = StringField(label="Image URL", validators=[DataRequired()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_sockets = SelectField(label="Has Sockets", validators=[DataRequired()], choices=[True, False])
    has_toilet = SelectField(label="Has Sockets", validators=[DataRequired()], choices=[True, False])
    has_wifi = SelectField(label="Has Sockets", validators=[DataRequired()], choices=[True, False])
    can_take_calls = SelectField(label="Has Sockets", validators=[DataRequired()], choices=[True, False])
    seats = StringField(label="Seats", validators=[DataRequired()])
    coffee_price = StringField(label="Coffee Price", validators=[DataRequired()])
    submit = SubmitField(label="Submit Record")


