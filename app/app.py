from flask import Flask ,render_template ,request,session,flash,redirect, url_for
# import redis
from flask_sqlalchemy import SQLAlchemy
from model import Record,User,db
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_apscheduler import APScheduler
from MYSMTP import MyMail
# scheduler = BlockingScheduler()
app = Flask(__name__)
app.secret_key ='secret...secret'
scheduler=BackgroundScheduler()



import pymysql
# 打开数据库连接
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='schedule', port=3306,charset='utf8mb4')
#mysql数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/schedule?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app)# db对象是 SQLAlchemy 类的实例
#redis 数据库
# r=redis.StrictRedis(host="localhost",port=6379, db=0)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # login and validate the user...
#         login_user(user)
#         flash("Logged in successfully.")
#         return redirect(request.args.get("next") or url_for("show"))
#     return render_template("login.html", form=form)
@app.route("/")
def init():
    # return  render_template("login.html")
	return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'],
                                    password=request.form['password']).first()
        if user:
            print('if user')
            session.get('user')
            session['username']=request.form['username']
            # flash('login successfully!')
            print('go to show')
            # return redirect(url_for('show'))
            return redirect(url_for('show'))
        else:
            print('return ....')
            return render_template('login.html', isback=1)

@app.route("/show",methods=["GET"])
def show():
    if 'username' in session:
        print('show ...')
        scheduler.print_jobs()
        print(session['username'])
        sql = 'select * from record where username = \''+session['username']+'\''
        print(sql)
        cur = conn.cursor()  # 使用cursor()方法获取操作游标
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()
            conn.commit()
        except:
            print("Error: unable to fecth data")
        return render_template("main.html",username=session['username'],RecordList=results)
    else:
        print('logined is false')
        return render_template("login.html")

@app.route('/delete/<int:id>')
def deleteRecord(id):
    print('I will delete No.%s record' %id)
    db.session.query(Record).filter_by(id=id).delete(synchronize_session=False)
    db.session.commit()
    db.session.flush()
    return redirect(url_for('show'))


# @app.before_first_request
# def initialize():
#     apsched = Scheduler()
#     apsched.start()
#
#     apsched.add_interval_job(checkFirstAPI, seconds=5)
#     apsched.add_interval_job(checkSecondAPI, seconds=5)
#     apsched.add_interval_job(checkThirdAPI, seconds=5)

# scheduler.start()

def doJob(to_list, content):
    print("send....")
    MyMail.send_mail([to_list], content)

@app.route('/add',methods=['POST'])
def addRecord():
    if 'username' in session:
        print('I will add record in '+session['username'])
        theDatetime=request.form['theDatetime']
        content=request.form['content']
        #生成待插入记录的对象并进行插入
        record=Record(username=session['username'],content=content,state=0,timing=theDatetime)
        db.session.add(record)
        db.session.commit()
        #获取datetime进行格式化
        print(theDatetime)
        d=datetime.strptime(theDatetime,"%Y-%m-%dT%H:%M")
        print(d)
        scheduler.add_job(doJob,'date',run_date=d,args=[session['username'],content])
    return redirect(url_for('show'))

@app.route('/gotoregist',methods=['GET'])
def gotoregist():
    return render_template("regist.html")

@app.route('/regist',methods=['POST'])
def regist():
    print('I will add a user ')
    u=request.form['rUsername']
    p=request.form['rPassword']
    #生成待插入记录的对象并进行插入
    user=User(username=u,password=p)
    db.session.add(user)
    db.session.commit()
    print('注册成功！')
    print(url_for('login'))
    # return redirect(url_for('login'))
    return render_template("login.html")
#插入记录
# record=Record('1209217462@qq.com','起床',0,'2017-06-03 22:00:00')
# db.session.add(record)
# db.session.commit()

# ti=datetime(2017,6,4,17,8,0)
# scheduler.add_job(doJob, 'date', run_date=ti, args=['1209217462@qq.com','吃饭啦。。。。'])

# try:
#     scheduler.start()
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

if __name__ == '__main__':
    #flask默认关闭多线程模式，通过 threaded=True 开启，大幅提高访问速度
    app.run(host='localhost', port=5000, debug=False,threaded=True)
    print('app is run ....................................')


