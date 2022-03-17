
import pandas as pd
import json
import glob

files = glob.glob("data/valid_records/*.json")
data = []
for file in files:
    with open(file, encoding='utf-8-sig') as f:
        doc = json.load(f)
        doc['file_name'] = file
        data.append(doc)

df = pd.DataFrame(data)

df.to_csv('processed_data/aggregated_data.csv', index=False)
