### import section ######################################################################################
import re , bcrypt
from flask import Flask , redirect, url_for, render_template,request,flash
from flask.globals import session
from datetime import datetime, timedelta , date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from codes import pw_maker,how_strong
###########################################################################################################



## app configratins #######################################################################################
app = Flask(__name__)
app.secret_key="3Eg!hS_24vwvEWF34@!r"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database/users.sqlite3'
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
app.permanent_session_lifetime = timedelta(days=1)
###########################################################################################################




### db configratins ######################################################################################
db = SQLAlchemy(app)

class users(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(100),nullable=False)
    user_bday = db.Column(db.DateTime,nullable=False)
    user_password = db.Column(db.String(100),nullable=False)
    signup_time = db.Column(db.DateTime)

    def __init__(self,first_name,last_name,username,user_email,user_bday,user_password,signup_time):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.user_email=user_email
        self.user_bday=user_bday
        self.user_password=user_password
        self.signup_time=signup_time

###########################################################################################################



### main function ########################################################################################
@app.route("/")
def main():
    return render_template("index.html")
###########################################################################################################



### signup function #######################################################################################
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        allgood= True
        session["firstname"]= request.form["input_firstname"]
        session["lastname"]= request.form["input_lastname"]
        session["username"]= request.form["input_username"]
        session["useremail"]= request.form["input_email"]
        session["birthdate"]=datetime.strptime(request.form["input_birthdate"],'%Y-%m-%d')
        password1= request.form["input_password1"]
        password2= request.form["input_password2"]
        today=to_integer(date.today())
        birthdate=to_integer(session["birthdate"])
        age=today-birthdate
        tempuser= users.query.filter_by(username=session["username"]).first()
        
        if tempuser:
            flash("username alrady existe, try another one.")
            allgood= False


        if re.search(r'\d', session["firstname"]):
            flash(" fits name must be letters only")
            allgood=False
            
        if re.search(r'\d', session["lastname"]):
            flash(" last name must be letters only")
            allgood=False

            
        if re.search(r'[^a-zA-Z0-9]', session["username"]):
            flash("username  must be letters and numbers only")
            allgood=False
        
        if age < 180000:
            flash("to yuong 2 die")
            allgood=False

        if password1 != password2:
            flash("passowrs dont match")
            allgood=False

        if how_strong.how_strong(password1) < 500:
            flash("passowr are too weak ")
            allgood=False
        
        if allgood:
            password=password1.encode("utf-8")
            session["password"]=bcrypt.hashpw(password,bcrypt.gensalt())
            
            newuser=users(session["firstname"],session["lastname"],session["username"],session["useremail"],session["birthdate"],session["password"],datetime.now())
            db.session.add(newuser)
            db.session.commit()
            
            return redirect(url_for("home"))
        return render_template("signup.html")
    else:
        return render_template("signup.html")

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


### pwget function ########################################################################################
@app.route("/pwgen",methods=["POST","GET"] )
def pwgen():
    
    if request.method == "POST":
        
        input_gen_numbers = request.form["input_gen_numbers"]
        input_gen_text = request.form["input_gen_text"]
        if pw_maker.passwordgenerator.conventer_to_list(input_gen_text) < 8:
            flash("enter al lest 8 words")
            return redirect(url_for('pwgen'))
        elif pw_maker.passwordgenerator.conventer_to_list(input_gen_text) > 7:
            gen_password = pw_maker.passwordgenerator.password_maker(input_gen_numbers,input_gen_text)
            return render_template("pwgen.html",gen_password=gen_password) 
            

    return render_template("pwgen.html")
###########################################################################################################





### login function #######################################################################################
@app.route("/login",methods=["POST","GET"])
def login():

    if request.method=="POST":
        session["username"]=request.form["username"]
        session["password"]=request.form["password"].encode("utf-8")

        usr = users.query.filter_by(username=session["username"]).first()
        if usr:
            if bcrypt.checkpw(session["password"],usr.user_password):
                return redirect(url_for("home") )
            else:
                flash("login faild.")
        else:
            flash("login faild.")
            
        flash("wrong username or password.")
    return render_template("login.html")
    
###########################################################################################################




### home function ########################################################################################
@app.route("/home")
def home():
    try:
        if session["username"]:
            usr = users.query.filter_by(username=session["username"]).first()
            return render_template("home.html",usr=session["username"] , pw= usr.user_password)
        else:
            flash("login first.")
            return redirect(url_for("login"))
    except:
            flash("login first.")
            return redirect(url_for("login"))
###########################################################################################################


### logout function #######################################################################################
@app.route("/logout")
def logout():
    session.clear()
    flash("you just loged out")
    return redirect(url_for("login"))
###########################################################################################################


### code runner function ###################################################################################
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)