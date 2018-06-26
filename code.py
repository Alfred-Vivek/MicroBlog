from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
username = ""
password = ""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, unique=True, nullable=False)
    Message = db.Column(db.String, unique=True, nullable=False)
    time_stamp = db.Column(db.String, nullable=False)

db.create_all()

@app.route('/')
def index():
	return render_template("login.html",error="")

@app.route('/show_entries', methods = ['GET','POST'])
def show_entries():	
	global username
	global password
	if(username=='admin' and password=='12345'):
		if(request.method == 'GET'):
			entries = db.session.query(User).order_by(User.id.desc())
			return render_template("user.html",entries=entries)		
		else:
			msg1 = request.form['message_Title']
			msg2 = request.form['message_Text area']
			msg3 = str(datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
			if(len(msg1)>0 and len(msg2)>0):
				new_user = User(Title=msg1,Message=msg2,time_stamp=msg3)
				db.session.add(new_user)
				db.session.commit()
				entries = db.session.query(User).order_by(User.id.desc())
				return render_template("user.html",entries=entries)
			else:
				entries = db.session.query(User).order_by(User.id.desc())
				return render_template("user.html",entries=entries)		
	else:
		return render_template("login.html",error="")

@app.route('/check', methods = ['GET','POST'])
def check():
	global username
	global password
	if(request.method == 'POST'):
		username = request.form['username']
		password = request.form['password']
		if(username=='admin' and password=='12345'):
			entries = db.session.query(User).order_by(User.id.desc())
			return render_template("user.html",entries=entries,err="")
		else:
			return render_template("login.html",error="Invalid Credentials")
	return render_template("login.html",error="")
if (__name__ == "__main__"):
	app.run()