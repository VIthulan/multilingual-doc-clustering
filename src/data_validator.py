import pandas as pd
import json
import glob
from datetime import datetime
import re
import shutil

vol = 'Kajaani'
invalid_files = []

FILE_PATH = "data/Data_collection/%s/Tamil/*.json" % vol
files = glob.glob(FILE_PATH)
data = []
for file in files:
    with open(file, encoding='utf-8-sig') as f:
        try:
            doc = json.load(f)
            doc['file_name'] = file
            data.append(doc)
        except Exception as e:
            print('***** Invalid JSON file format - %s' % file)
            invalid_files.append(file)
            print(e)

df = pd.DataFrame(data, dtype='str')

nan_file_name = df[pd.isna(df['file_name'])]
if len(nan_file_name.index):
    print('File name should not be empty/null')


def is_valid_column(content):
    if isinstance(content, float):
        return False
    if isinstance(content, str) and not content or content.isspace():
        return False


valid_categories = ['general', 'crime', 'political', 'business', 'economic', 'sports', 'arts', 'entertainment',
                    'education', 'tech', 'auto', 'legal', 'lifestyle', 'health', 'covid', 'weather']

invalid_title = []
invalid_content = []
invalid_url = []
invalid_date = []
invalid_category = []
for index, row in df.iterrows():
    if is_valid_column(row['title']) == False:
        invalid_title.append(row['file_name'])
        invalid_files.append(row['file_name'])

    if is_valid_column(row['content']) == False:
        invalid_content.append(row['file_name'])
        invalid_files.append(row['file_name'])

    # elif len(row['content']) < 250:
    #     invalid_content.append(row['file_name'])
    #     invalid_files.append(row['file_name'])

    if is_valid_column(row['url']) == False:
        invalid_url.append(row['file_name'])
        invalid_files.append(row['file_name'])

    try:
        if is_valid_column(row['date']) == False:
            invalid_date.append(row['file_name'])
            invalid_files.append(row['file_name'])

        else:
            datetime_object = datetime.strptime(row['date'], '%Y-%m-%d')
    except Exception as e:
        print(e, row['file_name'])
        invalid_date.append(row['file_name'])
        invalid_files.append(row['file_name'])

    if is_valid_column(row['category']) == False:
        invalid_category.append(row['file_name'])
        invalid_files.append(row['file_name'])

    else:
        categories = re.sub(r"\s+", "", row['category'], flags=re.UNICODE)
        categories_arr = categories.split(',')
        cat_check = []
        for category in categories_arr:
            if category not in valid_categories:
                print('invalid category - %s -> %s' % (category, row['file_name']))
                cat_check.append(category)
        if cat_check:
            invalid_category.append(row['file_name'])
            invalid_files.append(row['file_name'])

duplicate_title = df[df.duplicated('title')]
duplicate_content = df[df.duplicated('content')]

print('\n<-------- Validation results ---------->\n')
is_invalid_found = False
if invalid_title:
    is_invalid_found = True
    print('Invalid title field ')
    print(invalid_title)
    print('\n')
if invalid_content:
    is_invalid_found = True
    print('Invalid content field ')
    print(invalid_content)
    print('\n')

if invalid_url:
    is_invalid_found = True
    print('Invalid url field ')
    print(invalid_url)
    print('\n')

if invalid_date:
    is_invalid_found = True
    print('Invalid date field ')
    print(invalid_date)
    print('\n')

if invalid_category:
    is_invalid_found = True
    print('Invalid category field ')
    print(invalid_category)
    print('\n')

if len(duplicate_title.index):
    is_invalid_found = True
    print('** Duplicate title found')
    print(duplicate_title['file_name'])
    print('\n')
if len(duplicate_content.index):
    is_invalid_found = True
    print('** Duplicate content found')
    print(duplicate_title['file_name'])
    print('\n')

if not is_invalid_found:
    print('Good job! No validation error found')

print('Invalid files - ', invalid_files)
print('Moving valid files')

valid_files = []

for file_name in df['file_name']:
    if file_name in invalid_files:
        continue
    else:
        valid_files.append(file_name)

print('Valid files count - ', len(valid_files))
print('Valid files - ', valid_files)

for valid_file in valid_files:
    r_file_n = valid_file.split('/')[-1]
    shutil.copy2(valid_file, 'data/valid_records/%s_%s' % (vol, r_file_n))
