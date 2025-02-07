from flask import Flask, render_template, request, redirect, jsonify,url_for
import os
from dotenv import load_dotenv
from database import db, Department, Worker, ClockRecord

app = Flask(__name__)

load_dotenv()

#数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#安全配置
app.secret_key = os.getenv('SECRET_KEY' , 'dev-key-123')

#初始化数据库
db.init_app(app)

#创建数据库表（如果不存在）
with app.app_context():
    db.create_all()
    #手调初始化数据
    if not Department.query.first():
        departments = ['技术部', '营销部', '人事部']
        workers = [
            ('Zhangsan', '技术部'),
            ('Lisi', '营销部'),
            ('Wangwu', '技术部'),
            ('Zhaoliu', '人事部')
        ]
        for name in departments:
            db.session.add(Department(name=name))
        for name, dept_name in workers:
            department = Department.query.filter_by(name=dept_name).first()
            db.session.add(Worker(name=name, department=department))
        db.session.commit()

#存储打卡记录
clock_in_records = []

#初始化测试数据
'''
@app.before_first_request
def init_data():
    if not Department.query.first():
        departments = ['技术部', '营销部', '人事部']
        workers = [
            ('Zhangsan','技术部'),
            ('Lisi','营销部'),
            ('Wangwu','技术部'),
            ('Zhaoliu','人事部')
        ]
        for name in departments:
            db.session.add(Department(name=name))
        for name, dept_name in workers:
            department = Department.query.filter_by(name=dept_name).first()
            db.session.add(Worker(name=name,department=department))

        db.session.commit()
'''

#主页
@app.route('/')
def index():
    workers = Worker.query.all()
    records = ClockRecord.query.order_by(ClockRecord.timestamp.desc()).all()
    return render_template('index.html', workers=workers, records=records, departments=Department.query.all())


@app.route('/clock_in',methods=['POST'])
def clock_in():
    worker_id = request.form.get('worker_id')
    if worker_id:
        record = ClockRecord(worker_id=worker_id)
        db.session.add(record)
        db.session.commit()
    return redirect(url_for('index'))

#API:获取部门人员
@app.route('/api/workers')
def get_workers():
    departments = Department.query.all()
    return jsonify({
        dept.name: [w.name for w in dept.workers]
        for dept in departments

    })


