$python="C:\Python27\python.exe"
$path = Split-Path $MyInvocation.MyCommand.Path
$MyPythonScript= $path + "\etcd_self.py"
$m = & $python $MyPythonScript
$m