from flask import Flask, render_template, request, redirect, url_for, session
from utils import find_ad, search_data, docvecsFT, add_jobad
import os
from gensim.models.fasttext import FastText
import pickle
import sklearn
import uuid

app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(16)

@app.route('/')
def index():
  search_query = request.args.get("search")
  category_query = request.args.get("category")

  if search_query is None:
    search_query = "" # if not search than get everything
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
  return render_template('jobad.html', jobad=find_ad(webidx))

@app.route('/new-jobad', methods=['GET','POST'])
def new_jobad():
  if 'username' not in session:
    return redirect('login')
  
  print(request.form, request.args, request.data)
  
  if request.method == "POST":
    if 'classify' in request.form:
      f_title = request.form["title"]
      f_company = request.form["company"]
      f_desc = request.form["description"]

      tk_data = f_desc.split(" ")

      bbcFT = FastText.load("model/bbcFT.model")
      bbcFT_wv = bbcFT.wv

      bbcFT_dvs = docvecsFT(bbcFT_wv, [tk_data])

      with open("model/jobsft_model.pkl", "rb") as f:
        model = pickle.load(f)
      
      y_pred = model.predict(bbcFT_dvs)
      y_pred = y_pred[0]

      return render_template('new-jobad.html', title=f_title, description=f_desc, company=f_company, category=y_pred)
    elif 'main' in request.form:
      f_title = request.form["title"]
      f_company = request.form["company"]
      f_desc = request.form["description"]
      desc = " ".join(line.strip() for line in f_desc.splitlines())

      f_category = request.form["category"]

      add_jobad([uuid.uuid4(), f_title, f_company, desc, f_category])

      return render_template('new-jobad.html', title=f_title, description=f_desc, company=f_company, category=f_category, alert="Job advert successfully added!")

  return render_template('new-jobad.html')


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
  return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)