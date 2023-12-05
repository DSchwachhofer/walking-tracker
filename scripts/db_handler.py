from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WalkLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date=db.Column(db.String(250), nullable=False)
  distance=db.Column(db.Float, nullable=False)
  time=db.Column(db.Integer, nullable=False)

class Db_Handler():
  def __init__(self):
    pass

  def create_new_log(self, data):
    date = data["date"]
    distance = float(data["distance"])
    time = int(data["time"])
    new_log = WalkLog(date=date, distance=distance, time=time)
    db.session.add(new_log)
    db.session.commit()

  def get_all_logs(self):
    logs = WalkLog.query.all()
    return logs