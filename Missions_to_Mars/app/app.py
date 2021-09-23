from os import write
from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
from numpy import save
from scrape_mars import scrape

app = Flask(__name__)

app.config['FLASK_APP']='main'
app.config['FLASK_ENV']='development'
app.config['MONGO_URI']='mongodb://localhost:27017/mars_app'

mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    mars_data = db.mars_data
    mars_dict = mars_data.find_one()
    return render_template("index.html",mars_dict=mars_dict)

@app.route("/scrape")
def htmlscrape():
    mars_data = db.mars_data
    mars_scrape= scrape()
    mars_data.update_one({},{"$set": mars_scrape},upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)