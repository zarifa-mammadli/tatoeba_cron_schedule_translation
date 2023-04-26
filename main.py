
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import pickle

df = pd.read_table('modified_aze_link_sentences.tsv')

# Get the length of the DataFrame and divide it by 300
# to get the total number of iterations
num_iterations = len(df) // 300

for i in range(num_iterations):
    start_index = i * 10
    end_index = (i + 1) * 10
    lst = df.iloc[:, 0].tolist()[start_index:end_index]
    
    list_json = []
    try:
      for url in lst:
        vstr = requests.get(url).content
        soup = BeautifulSoup(vstr, features="html.parser")
    
        rows = soup.findAll('div', {"class":"sentence-and-translations md-whiteframe-1dp"})
    
        for row in rows:
            data = '[' + row['ng-init'][11:-1] + ']'
            new_data = str(data).replace("'und'", '"und"')
            new_data = json.loads(new_data)
            list_json.append(new_data)
    except:
        lst.append('ERROR')  
    
    
    with open(f"./data/{start_index}_{end_index}_translation_data.pickle", "ab") as fp:
        pickle.dump(list_json, fp)
        fp.close()

#     with open(f"./data/{start_index}_{end_index}_translation_data.pickle", 'rb') as fp:
#         new_list_json = pickle.load(fp)  
   
# new_list_json     
