## Capacity Tier Reporter (AWS)

Experimental tool that provides a report on the differences in restore point quantities between on-premises and cloud with Veeam Capacity Tier. 

It achives this by ether scanning the local repository for vbm files or you can use a PowerShell script to get the same info, then comparing that data against vbm files pulled from AWS.

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

## How to use:

With PowerShell

- Run localData.ps1 on VBR server, this will produced a local_data.json file
- Put this file in the same directory as the cap_tier_report_no_local_scan.py
- Run the above python script via powershell ./cap_ter...

With local repo scan:

- Update capacity_tier_report.py with the correct directory to scan (os.walk("f:/"):)
- Run the script in powershell ./capacity_tier_report.py

<hr>

## Requirements

The tool requires the following packages:

    pip install boto3 xmltodict tqdm

Please refer to the boto3 documentation on how to set up the credentials file.

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

The tools requires access to the local repository. 

Running this tool will incur AWS charges, please consult the your AWS specialist stating that the List_Objects_v2 CLI command is being used with pagination up to the maximum of 1000 objects per-run.

Note this is NOT a Veeam tool and has no association with Veeam.

I accept NO responsibility for issues that may arise from using this tool. See MIT licence.
