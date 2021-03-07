from flask import Flask, render_template, flash,url_for,redirect,request,session
#import sounddevice as sd 
#from playsound import playsound
from forms import RegistrationForm,LoginForm
#from scipy.io.wavfile import write 
#import wavio as wv 
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from keras.models import load_model
import os
from predict import predict

application = Flask(__name__)


application.config['SECRET_KEY'] = '4d5482dc5b0411eb983b3024a9431551'

application.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:@localhost/audio-recognition'.format(user='root', password='', server='localhost', database='audio-recognition')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'audio-recognition'
mysql = MySQL(application) 
db = SQLAlchemy(application)


class Signup(db.Model):
	username = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	password = db.Column(db.String(120),	nullable=False)


	
@application.route("/")
def home():
    return render_template('index.html')



@application.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		entry = Signup(username=username,email = email,password = password)
		db.session.add(entry)
		db.session.commit()
		flash(f'Account created for {form.email.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		email=request.form.get('email')
		password = request.form.get('password')
		secure_password = sha256_crypt.encrypt(str(password))
		secure_pass = sha256_crypt.verify(password,secure_password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		cursor.execute('SELECT * FROM signup WHERE email = % s AND password = % s', (email, password, ))  
		Signup = cursor.fetchone()  
		if Signup: 
			session['loggedin']=True
			session['id']=Signup['id'] 
			session['email']=Signup['email'] 
			flash('You have been logged in!', 'success')
			return redirect(url_for('analysis')) 
		else: 
			flash('Login Unsuccessful. Please check Email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@application.route("/index1")
def index1():
    return render_template('index1.html')


    
@application.route("/analysis")
def analysis():  
    return render_template('analysis.html')

@application.route("/analysis",methods=['GET', 'POST'])
def upload():
	if request.method=='POST':
		file=request.files["file"]
		file.save(os.path.join("uploads",file.filename))
		type_sound=predict(os.path.join("uploads",file.filename))
		print(type_sound)
		#return "Result:"+type_sound
		return render_template('analysis.html', prediction_text='Sound  is:-{}'.format(type_sound))
	return render_template('analysis.html')

	


			
			
	
if __name__ == '__main__':
	application.debug = True
	application.run()