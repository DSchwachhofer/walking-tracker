from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user

from scripts.forms import LoginForm, LogWalkForm
from scripts.db_handler import db, Db_Handler
from scripts.utility import get_daily_logs, reverse_all_logs, get_total_distance

from datetime import date, datetime
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

db_handler = Db_Handler()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///walkinglogs.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
  def __init__(self, id, username):
    self.id = id
    self.username = username

@login_manager.user_loader
def load_user(user_id):
  return User(user_id, "DSchwachhofer")

# creating database
# with app.app_context():
#   db.create_all()

# add a current year variable which will be accessed from all sites.
@app.context_processor
def inject_current_year():
  return {"current_year": date.today().year}

@app.route("/", methods=["GET", "POST"])
def home():
  all_logs = db_handler.get_all_logs()
  daily_logs = get_daily_logs(all_logs)
  total_distance = round(get_total_distance(all_logs), 2)
  if not current_user.is_authenticated:
    title = "Welcome"
  else:
    title = f"You Walked {total_distance}km"
  if not current_user.is_authenticated:
    subtitle = "please log in"
  else:
    subtitle = "keep up the good work"
  return render_template("index.html", page="home", title=title,subtitle=subtitle, total_distance=total_distance, logged_in=current_user.is_authenticated, daily_logs=daily_logs)

@app.route("/login", methods=["GET", "POST"])
def login():
  title = request.args.get("new_title", "")
  if not title:
    title = "Welcome"
  subtitle = request.args.get("new_subtitle", "")
  if not subtitle:
    subtitle = "please log in"
  form = LoginForm()
  if form.validate_on_submit():
    emailIsCorrect = form.data["email"] == os.getenv("USER_EMAIL")
    passwordIsCorrect = form.data["password"] == os.getenv("USER_PASSWORD")
    if not emailIsCorrect:
      return redirect(url_for("login", new_title="Unknown Email", new_subtitle="please try again"))
    if not passwordIsCorrect:
      return redirect(url_for("login", new_title="Wrong Password", new_subtitle="please try again"))
    user = User(1, "DSchwachhofer")
    login_user(user)
    return redirect(url_for("home"))
    
  return render_template("login.html", page="login", title=title, subtitle=subtitle, form=form, logged_in=current_user.is_authenticated)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("home"))

@app.route("/logwalk", methods=["GET", "POST"])
def logwalk():
  form = LogWalkForm()
  if form.validate_on_submit():
    print(form.data)
    db_handler.create_new_log(form.data)
    return redirect(url_for("home"))

  return render_template("logwalk.html", page="logwalk", title="Congratulations!", subtitle="please log your walk", form=form, cancel_url="home", logged_in=current_user.is_authenticated)

@app.route("/editlogs")
def edit_logs():
  title = request.args.get("new_title", "")
  if not title:
    title = "Made A Mistake?"
  subtitle = request.args.get("new_subtitle", "")
  if not subtitle:
    subtitle = "edit or remove your logs"

  all_logs = db_handler.get_all_logs()
  logs_reversed = reverse_all_logs(all_logs)

  return render_template("editlogs.html", title=title, subtitle=subtitle, page="editlogs", all_logs=logs_reversed, logged_in=current_user.is_authenticated)

@app.route("/editlog/<log_id>", methods=["GET", "POST"])
def edit_log(log_id):
  log = db_handler.get_log_from_id(log_id)
  form = LogWalkForm()
  if form.validate_on_submit():
    with app.app_context():
      db_handler.edit_log(form.data, log_id)
    return redirect(url_for("edit_logs", new_title="Success", new_subtitle=f"post from {log.date} successfully edited."))    

  form.date.data = datetime.strptime(log.date, "%Y-%m-%d").date()
  form.distance.data = log.distance
  form.time.data = log.time
  form.submit.label.text = "Save Edit"

  return render_template("logwalk.html", title="Edit Log", subtitle=f"from {log.date}", form=form, cancel_url="edit_logs", logged_in=current_user.is_authenticated)

@app.route("/deletelog/<log_id>")
def delete_log(log_id):
  log = db_handler.get_log_from_id(log_id)
  with app.app_context():
    db_handler.delete_log(log_id)
  return redirect(url_for("edit_logs", new_title="Success", new_subtitle=f"post from {log.date} successfully deleted."))

if __name__ == "__main__":
  app.run()