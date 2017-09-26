'this file starts the python-programm NVCLI.py with the python-interpreter included in this package
'the used python-interpreter is portable-python:
'http://www.portablepython.com/

dim current_path
Set fso = CreateObject("Scripting.FileSystemObject")
   current_path = fso.GetParentFolderName(wscript.ScriptFullName)
   
dim python_src_folder, index_py_path, path_python_runtime

python_src_folder = ""
index_py_path = python_src_folder & "\tambi.py"
path_python_runtime = ".\win-run\WinPython-64bit-3.6.1.0Qt5\python-3.6.1.amd64\pythonw.exe"
log_file = current_path & "\log.txt"

run_command = current_path & path_python_runtime
run_argument = current_path & index_py_path
'wscript.Echo run_command
'wscript.Echo run_argument
'run_everything = "%comspec% /c" & run_command & " " & run_argument & " > " & log_file
run_everything = "%comspec% /c" & run_command & " " & run_argument
'wscript.echo run_everything

Set wShell = WScript.CreateObject("WScript.Shell")
	wShell.CurrentDirectory = current_path & python_src_folder
	result = wShell.Run( run_everything, WindowStyle_Hidden)
	'result = wShell.Run( run_everything)
