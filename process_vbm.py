
def process_vbm(dict_file):
    job = ''
    file_paths = []
    capacity = []
    storage_qty = 0
    point_qty = 0
    try:
        job = dict_file['BackupMeta']['Backup']['@JobName']
        storages = dict_file['BackupMeta']['BackupMetaInfo']['Storages']['Storage']
        points = dict_file['BackupMeta']['BackupMetaInfo']['Points']['Point']
        if isinstance(points, list) == True:
            point_qty = len(points)
        else:
            point_qty = 1
        
        if isinstance(storages, list) != True:
            file_paths.append(storages['@FilePath'])
            backup_size = int(storages['@Stats'].split('<BackupSize>')[1].split('</BackupSize>')[0]) / 1024**2
            capacity.append(backup_size)
        else:
            for j in storages:
                file_paths.append(j['@FilePath'])
                backup_size = int(j['@Stats'].split('<BackupSize>')[1].split('</BackupSize>')[0]) / 1024**2
                capacity.append(backup_size)
    except:
        # print(f"Issue with {e}")
        pass

    total_cap = sum(capacity)
    return_obj = {
        "Job": job,
        # "Points": storage_qty,
        "Points": point_qty,
        "TotalBackupSizeMB": total_cap,
        "Files": file_paths
    }
    return return_obj


def save_text(text):
    with open('Analysis.txt', 'a+') as text_file:
        text_file.seek(0)
        # If file is not empty then append '\n'
        data = text_file.read(100)
        if len(data) > 0:
            text_file.write("\n")
        # Append text at the end of file
        text_file.write(text)