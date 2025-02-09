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
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda:datetime.now(timezone.utc)) #/clock-in/clock-out

    #定义与worker多对一的关系
    worker = db.relationship('Worker', backref='record')

class Attendance_rule(db.Model):
    '打卡规则模型'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), unique=True)
    work_start = db.Column(db.Time, default='09:00') #上班时间
    work_end = db.Column(db.Time, default='18:00') #下班时间
    late_tolerance = db.Column(db.Integer, default=30) #迟到容忍分钟
    early_tolerance = db.Column(db.Integer, default=30) #早退容忍分钟

class AttendanceRecord(db.Model):
    '考勤记录'
    id = db.Column(db.Integer, primary_key=True)
    check_date = db.Column(db.Date) #检查日期
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))
    status = db.Column(db.String(20)) #状态：正常/迟到/早退/缺卡
    clock_in = db.Column(db.DateTime) #实际打卡时间
    work_start = db.Column(db.DateTime) #应上班时间
    worker = db.relationship('Worker', backref='attendance_record')