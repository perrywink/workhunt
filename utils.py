import csv
import re

def read_data():
  with open('./data/data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # skip the headers
    jobads = []
    for row in data:
      jobads.append({
        "web_idx": row[0],
        "title": row[1],
        "description": row[2],
        "company": row[3],
        "category": row[4]
      })
  return jobads

def find_ad(web_idx):
  with open('./data/data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # skip the headers
    for row in data:
      if web_idx == row[0]:
        return ({
          "web_idx": row[0],
          "title": row[1],
          "description": row[2],
          "company": row[3],
          "category": row[4]
        })
  return {}


def appendRowToResult(results, row):
  results.append({
          "web_idx": row[0],
          "title": row[1],
          "description": row[2],
          "company": row[3],
          "category": row[4]
        }) 

def search_data(search_query, category_query):
  with open('./data/data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # skip the headers
    results = []
    for row in data:
      # concat title, desc and company for regex match
      # lower to ignore capitalisation
      concat_text = ' '.join([row[1], row[2], row[3]]).lower()
      search_match = re.search(search_query.lower(), concat_text)

      # if no category specified
      if category_query == "" and search_match:
        appendRowToResult(results, row)
        continue 

      category_match = (category_query != "") and (category_query == row[4])
      if search_match and category_match:
        appendRowToResult(results, row)
  return results

      
      