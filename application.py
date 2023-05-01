from flask import Flask, session
from flask_session import Session
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json

app = Flask(__name__)

engine = create_engine('postgresql://gzpdseeqgilgmc:f8612aed7a618933700c870247c15f70961b0a366796095091c46b8be75790b8@ec2-107-21-99-237.compute-1.amazonaws.com:5432/dasmon190o3648', echo = True)
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop('user_field', None)
    session.pop('user_mob', None)
    session.pop('sys_otp', None)
    return render_template("index.html")


# EXTERNAL PAGE LINKING      
@app.route('/equipment')
def equipment():
    return render_template("external-page/equipment.html")

@app.route('/selection')
def selection():
    return render_template("external-page/selection.html")

@app.route("/onlinecoaching")
def onlinecoaching():
    return render_template("external-page/onlinecoaching.html")

@app.route('/academy')
def academy():
    return render_template("external-page/academy.html")

@app.route('/job')
def job():
    return render_template("external-page/job.html")

@app.route('/injury_recovery')
def injury_recovery():
    return render_template("external-page/injury_recover.html")

@app.route('/portfolio')
def portfolio():
    return render_template("external-page/portfolio.html")

@app.route('/injury_remedies')
def injury_remedies():
    return render_template("external-page/injuries.html")

@app.route('/tournament')
def tournament():
    return render_template("external-page/localt.html")


@app.route('/sportcategory')
def sportcategory():
    return render_template("external-page/sportswise.html")

# MACHINE LEARNING injury_recovery LINKING      
import pandas as pd
@app.route("/submit_data", methods=["POST"])
def submit_data():
    if request.method == 'POST':
        injury = int(request.form.get('injury'))
        
        age = int(request.form.get('age'))
        calorie = int(request.form.get('calorie'))
        
        gender = int(request.form.get('gender'))
        weight = int(request.form.get('weight'))
        type1 = int(request.form.get('type'))

        temp_var = age/10 + weight/10 + gender + type1 + 10000/calorie
        X_test=[calorie,age,weight,0.5,gender,type1]
        for i in range(0,8):
            rem=injury%10
            X_test.insert(5,rem)
            injury=injury/10
        
        df = pd.read_csv("injury1.csv")



        dummies = pd.get_dummies(df.Injury)
        df_dummies= pd.concat([df,dummies],axis='columns')

        df_dummies.drop('Injury',axis='columns',inplace=True)
        df_dummies.drop('Ankle Injury',axis='columns',inplace=True)

        dummies_gender = pd.get_dummies(df.Gender)
        df_dummies= pd.concat([df_dummies,dummies_gender],axis='columns')

        df_dummies.drop('M',axis='columns',inplace=True)

        df_dummies.drop('Gender',axis='columns',inplace=True)

        dummies_type = pd.get_dummies(df.Type)
        df_dummies= pd.concat([df_dummies,dummies_type],axis='columns')

        df_dummies.drop('major',axis='columns',inplace=True)

        df_dummies.drop('Type',axis='columns',inplace=True)



        X=df_dummies.drop('Recovery_Period', axis='columns',inplace=True)
        X=df_dummies
        y=df.Recovery_Period
        

        from sklearn.ensemble import RandomForestRegressor
        regressor = RandomForestRegressor()
        regressor.fit(X,y)
        y_pred = regressor.predict([X_test])
        ans =int(round(y_pred[0]))

        import numpy as np
        import matplotlib.pyplot as plt

        return render_template("external-page/injury_recover.html", data=int(temp_var))
        

@app.route('/certificate')
def certificate():
    return "your certificate"

# CATEGORY WISE SPORT PAGE LINKING     
@app.route('/hockey')
def hockey():
    return render_template('external-page/sportcategory/fieldhockey1.html')


# EQUIPMENT PAGE LINKING
@app.route('/kit_cricket')
def kit_cricket():
    return render_template("external-page/kits/cricketkits.html")

@app.route('/kit_hockey')
def kit_hockey():
    return render_template("external-page/kits/hockeykit.html")

@app.route('/kit_football')
def kit_football():
    return render_template("external-page/kits/footballkits.html")

@app.route('/kit_kabaddi')
def kit_kabaddi():
    return render_template("external-page/kits/kabaddikit.html")


# ACADEMY PAGE LINKING     
@app.route('/coach1')
def coach1():
    return render_template("external-page/coach/coach1.html")

# ACADEMY PAGE LINKING 
@app.route('/coaching_cricket')
def coaching_cricket():
    return render_template("external-page/coaching/cricket.html")

@app.route('/coaching_hockey')
def coaching_hockey():
    return render_template("external-page/coaching/hockey.html")

# MAIN FUNCTION       
if __name__ == '__main__':
    app.run(debug=True)
    app.config['SECRET_KEY'] = env_var('FLASK_SECRET_KEY')
