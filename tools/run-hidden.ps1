# Run a console program (git, python, ffmpeg...) in a hidden window and print its output.
# Alex 2026-10-14: commands launched by Claude flashed black console windows on screen.
# usage: pwsh -File tools/run-hidden.ps1 git push origin main
param([Parameter(Mandatory, Position = 0)][string]$Exe, [Parameter(ValueFromRemainingArguments)][string[]]$Rest)
$out = [IO.Path]::GetTempFileName(); $err = [IO.Path]::GetTempFileName()
$quoted = $Rest | ForEach-Object { if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ } }
$p = Start-Process -FilePath $Exe -ArgumentList $quoted -WindowStyle Hidden -Wait -PassThru `
     -WorkingDirectory (Get-Location) -RedirectStandardOutput $out -RedirectStandardError $err
Get-Content $out -Encoding utf8; Get-Content $err -Encoding utf8
Remove-Item $out, $err -ErrorAction SilentlyContinue
exit $p.ExitCode
