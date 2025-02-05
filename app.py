from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = "qwertyuiop"

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username

@app.route('/')
def index():
  if "username" in session:
    return render_template('home.html', user = session['username'])
  else:
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == "GET":
    return render_template("signup.html")
  else:
    un = request.form.get('username')
    pw = request.form.get('password')
    cpw = request.form.get('confirm-password')

    if pw != cpw:
      return render_template("signup.html")
    else:
      # actually create the user!
      user = User.query.filter_by(username=un).first()
      if user:
        return render_template("signup.html")
      else:
        new_user = User(username=un, password=pw)
    
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # the "sign in thing"
        session['username'] = un
        return redirect("/")

  

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    un = request.form.get('username')
    pw = request.form.get('password')
    
    user = User.query.filter_by(username=un).first()
    if user and (pw == user.password):
      # the "sign in thing"
      session['username'] = un
      return redirect("/")
    else:
      return render_template("login.html")

@app.route('/logout')
def logout():
  # remove the username from the session if it's there
  session.pop('username', None)
  return render_template("login.html")

with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run()