import csv
import re
import numpy as np

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

def add_jobad(row):
  f = open('data/data.csv', 'a')
  writer = csv.writer(f)
  writer.writerow(row)

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
      search_rgx = "." if search_query == "" else search_query.lower()

      # concat title, desc and company for regex match
      # lower to ignore capitalisation
      concat_text = ' '.join([row[1], row[2], row[3]]).lower()
      search_match = re.search(search_rgx, concat_text)
      # if no category specified
      if category_query == "" and search_match:
        appendRowToResult(results, row)
        continue 

      category_match = (category_query != "") and (category_query == row[4])
      if search_match and category_match:
        appendRowToResult(results, row)
  return results


def docvecsFT(embeddings, docs):
    vecs = np.zeros((len(docs), embeddings.vector_size))
    for i, doc in enumerate(docs):
        embeds = [embeddings[term] for term in doc] # no filtering here
        docvec = np.vstack(embeds)
        docvec = np.sum(docvec, axis=0)
        vecs[i,:] = docvec
    return vecs
      
      