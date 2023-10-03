from flask import Flask, render_template, request, redirect, url_for, session
from utils import find_ad, search_data
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(16)

@app.route('/')
def index():
  search_query = request.args.get("search")
  category_query = request.args.get("category")

  if search_query is None:
    search_query = "." # if not search than get everything
  if category_query is None:
    category_query = ""

  jobads = search_data(search_query, category_query)

  return render_template('home.html', jobads=jobads, search=search_query, category=category_query)

@app.route('/login', methods=['GET','POST'])
def login():
  if 'username' in session:
    return redirect('/new-jobad')
  else:
    if request.method == "POST":
      if (request.form['username'] == 'employee') and (request.form['password'] == 'qweasd'):
        session['username'] = request.form['username']
        return redirect('/new-jobad')
      else:
        return render_template('login.html', login_message='Username of password is invalid.')
  return render_template('login.html')

@app.route('/logout')
def logout():
  session.pop("username", None)
  return redirect('/')

@app.route('/jobad/<webidx>')
def jobad(webidx):
  # jobads = read_data()
  # result = {}
  # for jobad in jobads:
  #   if (webidx == jobad['web_idx']):
  #     result = jobad
  #     break
  return render_template('jobad.html', jobad=find_ad(webidx))

@app.route('/new-jobad', methods=['GET','POST'])
def new_jobad():
  return render_template('new-jobad.html')

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)