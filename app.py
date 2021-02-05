### import section ######################################################################################
import re , bcrypt
from typing import Tuple
from flask import Flask, redirect, url_for, render_template,request,flash
from flask.globals import session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from codes import pw_maker,how_strong
###########################################################################################################



## app configratins #######################################################################################
app = Flask(__name__)
app.secret_key="3Eg!hS_24vwvEWF34@!r"
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
        fristname= request.form["input_fristname"]
        lastname= request.form["input_lastname"]
        username= request.form["input_username"]
        email= request.form["input_email"]
        password1= request.form["input_password1"]
        password2= request.form["input_password2"]

        if re.search(r'\d', fristname):
            flash(" fits name must be letters only")
            allgood=False
            
        if re.search(r'\d', lastname):
            flash(" last name must be letters only")
            allgood=False

            
        if re.search(r'[^a-zA-Z0-9]', username):
            flash("username  must be letters and numbers only")
            allgood=False
            
        if re.search(r'\d'  , email):
            flash("email must be letters only")
            allgood=False

      
        if password1 != password2:
            flash("passowrs dont match")
            allgood=False

        if how_strong.how_strong(password1) < 3000:
            flash("passowr are too weak ")
            allgood=False
            
        if allgood:


            return redirect(url_for("home"))
        return render_template("signup.html")
    else:
        return render_template("signup.html")



### pwget function ########################################################################################
@app.route("/pwgen",methods=["POST","GET"] )
def pwgen():
    
    if request.method == "POST":
        
        input_gen_numbers = request.form["input_gen_numbers"]
        input_gen_text = request.form["input_gen_text"]
        if pw_maker.passwordgenerator.conventer_to_list(input_gen_text) < 8:
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
        session["username"]=request.form["login_username"]
        password=request.form["login_password"].encode("utf-8")
        session["passowrd"]=bcrypt.hashpw(password,bcrypt.gensalt())
        return redirect(url_for("home") )

    else:
        return render_template("login.html")
###########################################################################################################




### home function ########################################################################################
@app.route("/home")
def home():
    try:
        if session["username"]:
            return render_template("home.html",usr=session["username"] , pw=session["passowrd"])
        else:
            flash("login first .")
            return redirect(url_for("login"))
    except:
            flash("login first .")
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
    app.run(debug=True)