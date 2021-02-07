from flask import Flask,render_template,request,redirect,url_for,flash,abort
import sqlite3 as sql
from datetime import datetime,timedelta
import time as t
from threading import Thread
import requests
import RPi.GPIO as m

m.setmode(m.BCM)
m.setup(17,m.OUT)
m.setwarnings(False)
m.output(17,0)
def longbell():
    m.output(17,1)
    t.sleep(6)
    m.output(17,0)

def shortbell():
    m.output(17,1)
    t.sleep(2)
    m.output(17,0)
    t.sleep(1)
app=Flask(__name__)
app.secret_key = 'PBSAasdertyuiop2020'
user_pass = {0:"user",1:"password"}

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title = '404'), 404
@app.route('/')
def login():
    user_pass[0]="user"
    user_pass[1]="password"
    return render_template('login.html')
@app.route('/loginvalidation',methods = ["POST"])
def loginvalid():
    username = request.form['username']
    password = request.form['password']
    if username=="admin" and password=="asdf":
        user_pass[0] = username
        user_pass[1] = password
        return render_template('selection2.html')
    else:
        return render_template('login.html')

di = {0:"decision"}
def total(act,start,end):
    a = datetime.strptime(start,"%Y-%m-%d")
    b = datetime.strptime(end,"%Y-%m-%d")
    delta = b-a
    print(act)
    #print("Total number of days: ",delta.days)
    print("Scheduled for the following days: ")
    di[0] = act
    dates = {}
    for i in range(0,delta.days):
        day = a + timedelta(days=i)
        if day.weekday() != 6:
            dates[str(day)[0:10]] = i+1
            print(str(day)[0:10])
    #print("Total dates dictionary:",dates)
    q = 0
    s = {}
    c = {}
    s_k = list(s.keys())
    l = {}
    if(act == "normaldays"):
        s = {"07:55:00":2,"08:00:00":3,"08:50:00":4,"09:40:00":5,"10:30:00":6,"10:45:00":7,"11:35:00":8,"12:25:00":9,"13:15:00":10,"14:05:00":11,"14:55:00":12,"15:10:00":13,"16:00:00":14,"16:50:00":15,"17:40:00":16}
        c = {"07:55:00":2,"08:00:00":3,"08:50:00":1,"09:40:00":2,"10:30:00":3,"10:45:00":1,"11:35:00":4,"12:25:00":5,"13:15:00":1,"14:05:00":2,"14:55:00":3,"15:10:00":1,"16:00:00":4,"16:50:00":5,"17:40:00":6}
        s_k = list(s.keys())
        l = {"07:45:00":1}
    elif(act=="internal"):
        s = {"08:50:00":2,"08:55:00":3,"09:00:00":4,"09:30:00":5,"10:00:00":6,"10:25:00":7,"10:50:00":10,"10:55:00":11,"11:00:00":12,"11:30:00":13,"12:00:00":14,"12:25:00":15,"13:20:00":18,"13:25:00":19,"13:30:00":20,"14:00:00":21,"14:30:00":22,"14:55:00":23,"15:20:00":26,"15:25:00":27,"15:30:00":28,"16:00:00":29,"16:30:00":30,"16:55:00":31}
        l = {"08:45:00":1,"10:30:00":8,"10:45:00":9,"12:30:00":16,"13:15:00":17,"15:00:00":24,"15:15:00":25,"17:00:00":32}
        c = {"08:50:00":1,"08:55:00":2,"09:00:00":3,"09:30:00":1,"10:00:00":2,"10:25:00":1,"10:50:00":1,"10:55:00":2,"11:00:00":3,"11:30:00":1,"12:00:00":2,"12:25:00":1,"13:20:00":1,"13:25:00":2,"13:30:00":3,"14:00:00":1,"14:30:00":2,"14:55:00":1,"15:20:00":1,"15:25:00":2,"15:30:00":3,"16:00:00":1,"16:30:00":2,"16:55:00":1}
        s_k = list(s.keys())
    elif(act=="semester"):
        s = {"08:50:00":2,"08:55:00":3,"09:00:00":4,"09:30:00":5,"10:00:00":6,"10:30:00":7,"11:00:00":8,"11:30:00":9,"11:45:00":10,"13:50:00":13,"13:55:00":14,"14:00:00":15,"14:30:00":16,"15:00:00":17,"15:30:00":18,"16:00:00":19,"16:30:00":20,"16:45:00":21}
        l = {"08:45:00":1,"12:00:00":11,"13:45:00":12,"17:00:00":22}
        c = {"08:50:00":1,"08:55:00":2,"09:00:00":3,"09:30:00":1,"10:00:00":2,"10:30:00":3,"11:00:00":4,"11:30:00":5,"11:45:00":1,"13:50:00":1,"13:55:00":2,"14:00:00":3,"14:30:00":1,"15:00:00":2,"15:30:00":3,"16:00:00":4,"16:30:00":5,"16:45:00":1}
        s_k = list(s.keys())
    elif(act=="stop"):
        s = {}
        l = {}
        c = {}
        s_k = list(s.keys())
    while q<len(dates) and act== di.get(0):
        p = 0
        while p < len(s)+len(l) and act == di.get(0):
            date = t.strftime("%Y-%m-%d")
            m = t.strftime("%H:%M:%S")
            if m in l and date in dates:
                p = 1 if l.get(m) is None else l.get(m)
                #print("p = ",p)
                q = len(dates) if dates.get(date) is None else dates.get(date)
                #print("q = ",q)
                print("long bell")
                longbell()
                #t.sleep(1)
            elif m in s and date in dates:
                p = 1 if s.get(m) is None else s.get(m)
                #print("p = ", p)
                q = len(dates) if dates.get(date) is None else dates.get(date)
                #print("q = ", q)
                r = c.get(m)
                print("The bell should ring", r," times")
                for i in range(r):
                    print("bell rings")
                    shortbell()
                    #t.sleep(1)

def new(start,end,d_s,d_l,c,act):
    dates = {}
    if len(start)!=0 and len(end)!=0:
        a = datetime.strptime(start,"%Y-%m-%d")
        b = datetime.strptime(end,"%Y-%m-%d")
        delta = b-a
        #print(act)
        #print("Total number of days: ",delta.days)
        print("The following dates are scheduled: ")
        di[0] = act
        #print(di)
        dates = {}
        for i in range(0,delta.days):
            day = a + timedelta(days=i)
            dates[str(day)[0:10]] = i+1
            print(str(day)[0:10])
        #print("Total dates dictionary:",dates)
        q = 0
        s_k = list(d_s.keys())
        while q< len(dates) and act== di.get(0):
            p = 0 
            while p < len(d_s)+len(d_l) and act==di.get(0):
                date = t.strftime("%Y-%m-%d")
                m = t.strftime("%H:%M:%S")
                if m in d_l and date in dates:
                    print(m)
                    p = 1 if d_l.get(m) is None else d_l.get(m)
                    #print("p = ",p)
                    q = len(dates) if dates.get(date) is None else dates.get(date)
                    #print("q = ",q)
                    print("long bell")
                    longbell()
                    #t.sleep(1)
                elif m in d_s and date in dates:
                    print(m)
                    p = 1 if d_s.get(m) is None else d_s.get(m)
                    #print("p = ",p)
                    q = len(dates) if dates.get(date) is None else dates.get(date)
                    #print("q = ",q)
                    r = c.get(m)
                    print("The bell should ring", r," times")
                    for i in range(r):
                        print("bell rings")
                        shortbell()
                        #t.sleep(1)

def EMERGENCY():
    print("longbell")
    longbell()
    date = t.strftime("%Y-%m-%d")
    a = datetime.strptime(date,"%Y-%m-%d")
    b = a + timedelta(days=1)
    s_d = str(a)[0:10]
    e_d = str(b)[0:10]
    thr = Thread(target = total, args=["stop",s_d,e_d])
    thr.start()
    thr = Thread(target = decision, args=["stop",s_d,e_d])
    thr.start()

@app.route('/classify',methods = ["GET","POST"])
def classify():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        action = request.form['regular']
        if action == 'regular':
            return render_template('selection1.html')
        elif action == 'emergency':
            thr = Thread(target = EMERGENCY)
            thr.start()
            return redirect(url_for('login'))
        elif action == 'create':
            return redirect(url_for('create'))
        elif action == 'logout':
            return redirect(url_for('login'))
        return render_template('selction2.html')
    else:
        abort(404)
def decision(action,start,end):
    con = sql.connect("real2.db") 
    cur = con.cursor()
    cursor = con.execute("SELECT name from sqlite_master WHERE type = 'table' AND name = 'Decision';")
    result = cursor.fetchone()
    cur.execute("DROP TABLE IF EXISTS Decision")
    cur.execute('''CREATE TABLE IF NOT EXISTS Decision(SNO INTEGER PRIMARY KEY AUTOINCREMENT
        ,DAY TEXT NOT NULL,Start_date TEXT NOT NULL,End_date TEXT NOT NULL)''')
    cur.execute("INSERT INTO Decision(DAY,Start_date,End_date) VALUES (?,?,?)",(action,start,end,))
    con.commit()
    con.close()

def back_up():
    try:
        di[0] = "decision"
        con = sql.connect("real2.db") 
        con.row_factory = sql.Row
        cur = con.cursor()
        cursor = con.execute("SELECT name from sqlite_master WHERE type = 'table' AND name = 'Decision';")
        cursor =con.execute("select * from Decision")
        for row in cursor:
            decision = row[1]
            start = row[2]
            end = row[3]
        #print(decision)
        if decision == "create":
            con = sql.connect("real.db") 
            cur = con.cursor()
            cursor = con.execute("select * from SchoolBells")
            d_s = {}
            d_l = {}
            c = {}
            for row in cursor:
                if row[2] == "short bell":
                    d_s[row[1]] = row[0]
                    c[row[1]] = row[3]
                elif row[2] == "long bell":
                    d_l[row[1]] = row[0]
            #print(d_s,d_l,c)
            thr  =Thread(target = new, args = [start,end,d_s,d_l,c,decision])
            thr.start()
        else:
            thr = Thread(target = total, args = [decision,start,end])
            thr.start()
    except:
        flash("no values")

@app.route('/exam',methods=["POST","GET"])
def exam():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        a = request.form
        con = sql.connect("real1.db") 
        cur = con.cursor()
        cursor = con.execute("SELECT name from sqlite_master WHERE type = 'table' AND name = 'DATE';")
        result = cursor.fetchone()
        cur.execute("DROP TABLE IF EXISTS DATA")
        #print("table droped successfully")
        cur.execute('''CREATE TABLE IF NOT EXISTS DATA(SNO INTEGER PRIMARY KEY AUTOINCREMENT,DAY TEXT NOT NULL,STARTDATE TEXT NOT NULL,ENDDATE TEXT NOT NULL)''')
        cur.execute("INSERT INTO DATA(DAY,STARTDATE,ENDDATE) VALUES (?,?,?)",(str(a['internal']),str(a['startDate']),str(a['endDate']),))
        con.commit()
        #con.close()
        #print("database saved")
        flash("Successfully Saved")
        cursor =con.execute("select DAY,STARTDATE,ENDDATE from DATA")
        action = request.form['internal']
        for row in cursor:
            act = row[0]
            s_d = row[1]
            e_d = row[2]
        di[0] = "decision"
        thr = Thread(target = total, args = [act,s_d,e_d])
        thr.start()
        th = Thread(target = decision, args = [act,s_d,e_d])
        th.start()
        return render_template('selection1.html')
    else:
        abort(404)


@app.route('/create',methods=["GET","POST"])
def create():
    time = []
    text = []
    bell = []
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        if request.method=="POST":
            if request.form.get("external")=="submit":
                data = request.form.to_dict(flat=False)
                start_date = data['start_Date'][0]
                end_date = data['End_Date'][0]
                total = len(data)+1
                t = int(total/3)
                for i in range(0,t-1):
                    ti=data['time'+str(i)]
                    te=data['text'+str(i)]
                    be=data['select'+str(i)]
                    time.append(ti)
                    text.append(te)
                    bell.append(be)
                con = sql.connect("real.db") 
                cur = con.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS SchoolBells(SNO INTEGER PRIMARY KEY AUTOINCREMENT,TIME TEXT NOT NULL,BELLS TEXT NOT NULL,COUNT INT NOT NULL)''')
                for i in range(0,len(time)):
                    if len(str(time[i][0]))!= 0 and len(str(text[i][0]))!=0:
                        cur.execute("INSERT INTO SchoolBells(TIME,COUNT,BELLS) VALUES (?,?,?)",(str(time[i][0]),str(text[i][0]),str(bell[i][0]),))
                con.commit()
                con.close()
                #print("database saved")
                flash("Successfully Saved")
                di[0] = "decision"
                act = "create"
                d_s = {}
                d_l = {}
                c = {}
                for i in range(0,t-1):
                    if bell[i][0] == 'short bell':
                        d_s[time[i][0]] = i+1
                        c[time[i][0]]=int(text[i][0])
                    if bell[i][0] == 'long bell':
                        d_l[time[i][0]] = i+1
                thr = Thread(target= new, args=[start_date,end_date,d_s,d_l,c,act])
                thr.start()
                th = Thread(target = decision, args = [act,start_date,end_date])
                th.start()

                return redirect(url_for('create'))
            elif request.form.get("external")=="display":
                return redirect(url_for('alarmschedule'))
            elif request.form.get("external")=="clear":
                return redirect(url_for('clear'))
            elif request.form.get("external")=="logout":
                return redirect(url_for('login'))
            return render_template('create.html')
        else:
            flash("Server Error")
            return render_template("create.html")
    else:
        abort(404)

@app.route('/clear',methods=["GET","POST"])
def clear():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        try:
            con = sql.connect("real.db") 
            cur = con.cursor()
            cur.execute("DROP TABLE SchoolBells")
            con.commit()
            con.close()
            #print("table dropped successfully")
            flash("Successfully Cleared the Database")
            return redirect(url_for('create'))
        except:
            return "<h1>Error, Table is already deleted</<h1>"
    else:
        abort(404)

@app.route("/alarmschedule",methods=["GET","POST"])
def alarmschedule():
    if user_pass[0]=="admin" and user_pass[1]=="asdf":
        if request.method=="POST":
            if request.form.get("external")=="submit":
                return redirect(url_for('create'))
            elif request.form.get("external")=="clear":
                return redirect(url_for('clear'))
            elif request.form.get("external")=="display":
                return redirect(url_for('alarmschedule'))

        try:
            con = sql.connect("real.db")
            con.row_factory = sql.Row 
            cur = con.cursor()
            cur.execute("SELECT SNO,TIME,BELLS,COUNT FROM SchoolBells")
            rows = cur.fetchall()
            return render_template('scheduledisplayer.html',items= rows)
        except:
            return "<h1>Error , create a table</h1>"
    else:
        abort(404)


thr = Thread(target = back_up)
thr.start()

if __name__=='__main__':
    #app.run(debug = True)
    app.run(host='0.0.0.0',port=8080,debug=True,use_reloader=False) 
