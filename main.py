import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import AddCafeForm

# initialize the Flask application
app = Flask(__name__)
# set a secret key for use for the flask form
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
# initialize the app to use bootstrap
Bootstrap(app)

# connect to db
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", "sqlite:///Cafe and Wifi Website.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    """
    This class represent the cafe table in the database
    """
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean(), nullable=False)
    has_toilet = db.Column(db.Boolean(), nullable=False)
    has_wifi = db.Column(db.Boolean(), nullable=False)
    can_take_calls = db.Column(db.Boolean(), nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))


# create the database if it does not exist
db.create_all()


# a route to the home page
@app.route("/")
def home():
    """
    This method is called when the home route is loaded on the web browser. It renders the home page
    :return: (str) the web page is rendered
    """
    return render_template("index.html")


# the route to the all-cafes web page
@app.route("/all-cafes")
def all_cafes():
    """
    This method is called when the all-cafes is loaded on the web browser. It renders the all-cafes page
    :return: (str) the web page is rendered
    """
    cafes = Cafe.query.all()
    return render_template("all_cafes.html", all_cafes=cafes)


# the route to the add-cafe web page
@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    """
    This method is called when the add-cafe is loaded on the web browser. It renders the add-cafes page
    :return: (str) the web page is rendered
    """

    # create a form for the user's entry
    form = AddCafeForm(cafe="ddd")

    # if the form is submitted and has been validated
    # create a new cafe then add it to the database
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.cafe.data, map_url=form.map_url.data, img_url=form.img_url.data,
                        location=form.location.data, has_sockets=bool(form.has_sockets.data),
                        has_toilet=bool(form.has_toilet.data), has_wifi=bool(form.has_wifi.data),
                        can_take_calls=bool(form.can_take_calls.data), seats=form.seats.data,
                        coffee_price=f"${form.coffee_price.data}")

        db.session.add(new_cafe)
        db.session.commit()

        # tell the user the form gas been added to the database successfully
        flash("Cafe added successfully")
        # redirect the user to the home page
        return redirect(url_for('home'))

    # render the add-cafe web page
    return render_template("add_cafe.html", form=form)


# the route to the update web page
@app.route("/update/<int:cafe_id>", methods=["GET", "POST"])
def update_cafe(cafe_id):
    """
    This method is called when the update/cafe_id is loaded on the web browser. It renders the update-cafes page
    :param cafe_id: (int) the id of the cafe to be updated
    :return: (str) the web page is rendered

    """

    # get the cafe to be updated
    cafe = Cafe.query.get(cafe_id)

    # show the current cafe values in the form
    form = AddCafeForm(cafe=cafe.name, map_url=cafe.map_url, img_url=cafe.img_url,
                       location=cafe.location, has_sockets=cafe.has_sockets,
                       has_toilet=cafe.has_toilet, has_wifi=cafe.has_wifi,
                       can_take_calls=cafe.can_take_calls, seats=cafe.seats,
                       coffee_price=cafe.coffee_price)

    # if the for is submitted and has been validated, update the cafe in the database
    if form.validate_on_submit():
        cafe.name = form.cafe.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.has_sockets = bool(form.has_sockets.data)
        cafe.has_toilet = bool(form.has_toilet.data)
        cafe.has_wifi = bool(form.has_wifi.data)
        cafe.can_take_calls = bool(form.can_take_calls.data)
        cafe.seats = form.seats.data
        cafe.coffee_price = form.coffee_price.data

        db.session.commit()

        # redirect the user to the all-cafes web page
        return redirect(url_for("all_cafes"))

    return render_template("add_cafe.html", form=form)


# the route to the delete/cafe_id web page
@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    """
    This method is called when the delete/cafe_id is loaded on the web browser.
    :param cafe_id: (int) the cafe id to be deleted
    :return: (str) the web page is rendered
    """

    # get the cafe to be deleted
    # delete the selected cafe
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()

    # redirect the user to the all-cafes home page
    return redirect(url_for("all_cafes"))


# if this is the main class, run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
