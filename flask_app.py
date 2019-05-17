from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")
db = mongo.db

@app.route('/')
def index():
    mars_data = db.mars_scrape.find_one()
    return render_template('index.html', mars_data=mars_data)


@app.route('/scrape')
def scrape():
    mars_stuff = mongo.db.mars_scrape
    data = scrape_mars.scrape()
    mars_stuff.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)