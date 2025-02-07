from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy
print("Loading database module...")
db = SQLAlchemy()
class Department(db.Model):
    '部门模型'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    #定义与worker一对多的关系
    workers = db.relationship('Worker', backref='department',lazy=True)

class Worker(db.Model):
    '工人模型'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class ClockRecord(db.Model):
    '打卡记录模型'
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

    #定义与worker多对一的关系
    worker = db.relationship('Worker', backref='records')