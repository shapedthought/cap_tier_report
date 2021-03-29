import os
import xmltodict
import json
import boto3
from tqdm import tqdm
from collections import Counter
from process_vbm import process_vbm, save_text
import itertools
from functools import reduce
import pprint

# set dictionaries

local_vbm = []
cloud_vbm = []
local_results = []
cloud_results = []


# scan filesystem for vbm files

print('Running')

print('Scanning file system')
for dirpath, dirs, files in os.walk("f:/"):  
            for filename in files:
                        fname = os.path.join(dirpath,filename)
                        if "vbm" in fname:
                            local_vbm.append(fname)
print('Finished')
print("")

with open('local_vbm.txt', 'w') as local_vbm_data:
    local_vbm_data.write(str(local_vbm))

# for each vbm, open and process the result

print('Processing local vbm')
for item in local_vbm:
    with open(item, 'r') as file_data:
        dict_file = xmltodict.parse(file_data.read())
    results_data = process_vbm(dict_file)
    local_results.append(results_data)

print('Finished')
print("")
# scaen the cloud repo for vbm files

print('Scanning cloud')
s3_client = boto3.client('s3')

paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket="veeamv11bucket")

for page in tqdm(pages):
    for obj in page['Contents']:
        if 'vbm' in obj['Key']:
            print(obj['Key'])
            cloud_vbm.append(obj['Key'])

print("Writing paths to cloud vbm files")
for item in cloud_vbm:
    with open('vbm_paths.txt', 'w') as vbm_paths:
        vbm_paths.write(str(cloud_vbm))

print("Finished")
print("")
s3_resource = boto3.resource('s3')

# for each vbm found

print('Processing cloud vbm files')

for item in tqdm(cloud_vbm):
    # get the data from the file
    data = s3_resource.Object('veeamv11bucket', item)
    # read the body
    body = data.get()['Body'].read()
    # make some changes so it can be read as xml
    data = str(body).split('<BackupMeta Version')[1]
    data2 = "<BackupMeta Version" + data[:-1]
    # convert to a dict
    dict_file = xmltodict.parse(data2)
    # send for processing
    results_data = process_vbm(dict_file)
    cloud_results.append(results_data)

# Create new list of jobs, the remove duplicates
cloud_jobs_list = [x['Job'] for x in cloud_results]
cloud_jobs = list(dict.fromkeys(cloud_jobs_list))

updated_cloud_results = []

print(type(cloud_results))

for job in cloud_jobs:
    # filter out each job in turn
    j = list(filter(lambda x: x['Job'] == job, cloud_results))

    # calculate the new total capacity
    new_cap = reduce((lambda x, y: x + y), [x['TotalBackupSizeMB'] for x in j])

    # Create new list of lists with the backups files
    all_files_list = [x['Files'] for x in j]

    # Flatten list using itertools
    flat_list = list(itertools.chain(*all_files_list))

    point_qty = [x['Points'] for x in j]

    # Create new updated object
    new_data = {
        "Job": job,
        "Points": point_qty[0],
        "TotalBackupSizeMB": new_cap,
        "Files": flat_list
    }
    updated_cloud_results.append(new_data)


print("Finished")
print("")
# short term create two json files, one for local and the other for remote

with open('local_results.json', 'w') as json_file:
    json.dump(local_results, json_file)

with open('cloud_results.json', 'w') as json_file:
    json.dump(updated_cloud_results, json_file) # change

local_jobs = [x['Job'] for x in local_results]
cloud_jobs = [x['Job'] for x in updated_cloud_results]

for i in local_results:
    for j in updated_cloud_results:
        if i['Job'] == j['Job']:
            job = i['Job']
            point_diff = j['Points'] - i['Points'] 
            cap_diff = j['TotalBackupSizeMB'] - i['TotalBackupSizeMB']
            points_text = f"Points difference {point_diff}"
            cap_text = f"Cloud capacity difference {cap_diff}"
            # print(i['Job'])
            # print(points_text)
            # print(cap_text)
            save_data = [job, points_text, cap_text]
            for s in save_data:
                save_text(s)


for i in local_jobs:
    if i not in cloud_jobs:
        text = f"{i} not in cloud"
        print(text)
        save_text(text)


