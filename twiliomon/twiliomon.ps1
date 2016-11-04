$python="C:\Python27\python.exe"
$path = Split-Path $MyInvocation.MyCommand.Path
$MyPythonScript= $path + "\twiliomon.py"
$m = & $python $MyPythonScript
$m