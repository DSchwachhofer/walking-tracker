from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Bootstrap(app)

@app.route("/")
def home():
  return render_template("index.html", page="home", title="Welcome",subtitle="please log a walk", image_url=url_for('static', filename='images/treadmill.jpg'))