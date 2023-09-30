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

def search_data(search_query):
  with open('./data/data.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    next(data, None)  # skip the headers
    results = []
    for row in data:
      # concat title, desc and company for regex match
      # lower to ignore capitalisation
      concat_text = ' '.join([row[1], row[2], row[3]]).lower()
      match = re.search(search_query, concat_text)
      if match:
        results.append({
        "web_idx": row[0],
        "title": row[1],
        "description": row[2],
        "company": row[3],
        "category": row[4]
      })
  return results

      
      