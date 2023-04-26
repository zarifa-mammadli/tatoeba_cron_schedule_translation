from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from github import Github
import os

# ------------------------------------------------------------------------------
access_token = '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'

repo_name = 'tatoeba_cron_schedule_translation'

username = 'zarifa-mammadli'

folder_name = 'data'

# Create a Github instance using your access token
g = Github(access_token)

# Get the repository
repo = g.get_user(username).get_repo(repo_name)

# Check if the folder already exists
try:
    contents = repo.get_contents(folder_name)
    print(f"{folder_name} folder already exists")
except:
    # If the folder does not exist, create it
    print(f"{folder_name} folder does not exist")
    repo.create_file(f"{folder_name}/00.txt", "Initial commit", "")
    print(f"{folder_name} folder created")
    
# ------------------------------------------------------------------------------    

df = pd.read_table('modified_aze_link_sentences.tsv')
lst = df.iloc[:, 0].tolist()[300:]
url = 'https://github.com/zarifa-mammadli/tatoeba_cron_schedule_translation/tree/main/data'
response = requests.get(url)

list_json = []


for url in lst:
    vstr = requests.get(url).content
    soup = BeautifulSoup(vstr, features="html.parser")

    rows = soup.findAll('div', {"class":"sentence-and-translations md-whiteframe-1dp"})

    for row in rows:
        data = '[' + row['ng-init'][11:-1] + ']'
        new_data = str(data).replace("'und'", '"und"')
        new_data = json.loads(new_data)
        list_json.append(new_data)

list_json

import pickle

with open("./data/translation_datas.pickle", "wb") as fp:
    pickle.dump(list_json, fp)
    fp.close()

# with open('sample_data/300_translation_datas.pickle', 'rb') as fp:
#   new_list_json = pickle.load(fp)  
   
# new_list_json     
