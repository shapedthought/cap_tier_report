## Capacity Tier Reporter (AWS)

Experimental tool that provides a report on the differences in restore point quantities between on-premises and cloud with Veeam Capacity Tier. 

It achives this by scanning the local Veeam vbm files (metadata) and comparing them with cloud versions of the same files.

It is currently designed to be used with copy-only mode. 

It will produce three files:
- cloud_results.json
- local_results.json
- Analysis.txt

<br>
The json files contains the following for each job:

- Job Name
- Quantity of restore points
- Total Backedup Capacity in MB

<br>
The Analysis file provides:

- Job Name
- Difference in restore point quantity 
- Difference in capacity MB

<hr>

The tool requires the following packages:

    pip install boto3 xmltodict tqdm

Please refer to the boto3 documentation on how to set up the credentials file.

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

The tools requires access to the local repository. 

I do not believe there is any charge for using Boto3 as it is a wrapper for the AWS CLI, however, please consult your AWS specialist before progressing.

I accept NO responsibility for issues that may arise from using this tool. See MIT licence.