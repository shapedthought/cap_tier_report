# Add below if not v11
# Add-PSSnapin VeeamPSSnapin

$backups = Get-VBRBackup | Where-Object { $_.TypeToString -ne "Backup Copy" }

$results = @()

foreach ($backup in $backups) {
    $storages = $backup.GetAllStorages()
    $TotalBackupSizeMB = 0
    $files = @()
    foreach ($item in $storages) {
        $TotalBackupSizeMB += $item.Stats.BackupSize / 1MB
        if ([string]$item.FilePath -like "*\\*") {
            $bu_only = $item.FilePath.ToString().Split('\\')[-1]
            $files += $bu_only
        }
        elseif ([string]$item.FilePath -like "*/*") {
            $bu_only = $item.FilePath.ToString().Split('/')[-1]
            $files += $bu_only
        }
        else {
            $files += $item.FilePath
        }

    }
    $Job = $backup.JobName
    $Type = $backup.TypeToString
    $allPoints = 0
    $Points = ($backup.GetPoints()).length
    foreach ($point in $Points) {
        $allPoints += [int]$point
    }
    if ($allPoints -gt 0) {
        $object = [PSCustomObject]@{
            Job               = $Job
            Type              = $Type
            Points            = $allPoints
            TotalBackupSizMB = $TotalBackupSizeMB
            Files             = $files
        }
        $results += $object
    
    }

}

$results | ConvertTo-Json | Out-File -FilePath .\local_data.json

