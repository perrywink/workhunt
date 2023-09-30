from flask import Flask, render_template, request, redirect, url_for
import csv
from utils import read_data, search_data

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
  return render_template('home.html', jobads=read_data())

@app.route('/search', methods=["post"])
def search_jobs():
  search_query = request.form['search-query']
  jobads = search_data(search_query)
  return render_template('home.html', jobads=jobads)

@app.route('/jobad/<webidx>')
def jobad(webidx):
  jobads = read_data()
  result = {}
  for jobad in jobads:
    if (webidx == jobad['web_idx']):
      result = jobad
      break
  return render_template('jobad.html', jobad=result)

if __name__ == '__main__':
    app.run(debug=True)