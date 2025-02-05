from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)

@app.route('/')
def index():
  return redirect('/signup')

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/login')
def login():
  pass

@app.route('/logout')
def logout():
  pass

if __name__ == '__main__':
  app.run()