from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import pickle

df = pd.read_table('modified_aze_link_sentences.tsv')
lst = df.iloc[:, 0].tolist()[320:340]
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


with open("./data/translation_datas.pickle", "wb") as fp:
    pickle.dump(list_json, fp)
    fp.close()

# with open('sample_data/300_translation_datas.pickle', 'rb') as fp:
#   new_list_json = pickle.load(fp)  
   
# new_list_json     
