from sqlite3.dbapi2 import Cursor, Date, connect
from flask import Flask, render_template,request,redirect
# from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import string
import random
import sqlite3

# from sqlalchemy.sql import text


# def db_connection():
#     con=None
#     try:
#         con=sqlite3.connect("surveydetails.db")
#     except Exception as e:
#         print(str(e))
#     return con
# db_name = 'surveydetails.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# # # initialize DB
# db=SQLAlchemy(app)

# # create database model

# class SurveyDetails(db.Model):
#     id=db.Column(db.String,primary_key=True)
#     name=db.Column(db.String(200),nullable=False)
#     gender=db.Column(db.String(200),nullable=False)
#     age=db.Column(db.String(200),nullable=False)
#     vaccinestat=db.Column(db.String(200),nullable=False)
#     date_of_survey=db.Column(db.DateTime,default=datetime.utcnow)
#     # create a function to return a string when we add something
#     def __repr__(self) -> str:
#         return super().__repr__()


# @app.route('/profile/<name>')
# def profile(name):
#     return render_template("profile.html",name=name)


# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr} </h1>"

app= Flask(__name__)
randomstr=''.join(random.choices(string.ascii_letters+string.digits,k=10))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/bot',methods=["POST"])
def bot():
    print("HELLO*********************************************")
    if request.method=="POST":
        con=sqlite3.connect("surveydetails.db")
        cursor=con.cursor()
        global randomstr
        randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k=10))
        print("Random String inside function is : ",randomstr)
        person_name=request.form['name1']
        person_gender=request.form['agegroup']
        person_age=request.form['gendergroup']
        person_vaccinestat=request.form['vacstatgroup']
        # person_dateofsurvey=int(date('now'))
        try:
            sql="""INSERT INTO Details VALUES(?,?,?,?,?)"""
            # result=cursor.execute(sql)
            result=cursor.execute(sql,(randomstr,person_name,person_gender,person_age,person_vaccinestat))
            
            if result==0:
                print("Error in database")
            else:
                print("Success")
            con.commit()
            cursor.close()
            con.close()
            return render_template('bot.html')
        except Exception as e:
            print(str(e))
            return redirect('/')
       
        # return '<h1> Name is: {} and age is {}</h1>'.format(person_name,person_age)
def sendrandom():
    print("The value received by bot is : ",randomstr)
    return randomstr
    # con=db_connection()
    # cursor=con.cursor()
    # # title="Thank you"


# @app.route("/webhook")
# def webhook():
#     print("*******************************",randomstr)

    # randomstr = ''.join(random.choices(string.ascii_letters+string.digits,10))
    # person_name=request.form['name1']
    # person_gender=request.form['agegroup']
    # person_age=request.form['gendergroup']
    # person_vaccinestat=request.form['vacstatgroup']
    # q="""SELECT DATE('now')"""
    # person_dateofsurvey=cursor.execute(q)
    # cursor.close()
    # con.commit()

    # cursor=con.cursor()
    # d="""INSERT INTO demo VALUES(?,?)"""
    # result=cursor.execute(d,("sree","12"))

    # person_dateofsurvey=DATE('now')
    # sql="""INSERT INTO SurveyDetails VALUES(?,?,?,?,?,?)"""
    # # result=cursor.execute(sql,("randomstr","person_name","person_gender",12,"person_vaccinestat",person_dateofsurvey))
    # result=cursor.execute(sql,(randomstr,person_name,person_gender,person_age,person_vaccinestat,person_dateofsurvey))
    # if result==0:
    #     print("Error in database")
    # else:
    #     print("Success")
    # con.commit()
    # cursor.close()
    # con.close()
    # if request.method=="POST":
        
    # person_new_data=SurveyDetails(id=randomstr,name=person_name,gender=person_gender,age=person_age,vaccinestat=person_vaccinestat)
        # commit to database
    
            # db.session.add(person_new_data)
            # db.session.commit()
            # return redirect('/bot')
    
    # else:   
    #     return render_template("bot.html", name=person_name)

if __name__=="__main__":
    app.run(debug=True)