# <i> Creating .exe file from .py file.</i>

- <i>STEP 1</i> : install pyinstaller module by <i><b>pip install pyinstaller</b></i>

- <i>STEP 2</i> : run <b>pyinstaller <i><Main_FileName></i>.py </b>

- <i><Main_FileName></i>  REPRESENTS THE NAME OF THE MAIN PYTHON FILE WHICH WILL EXECUTE THE PROGRAM. App.py IN THIS CASE

- Two folders named <b><i>build</i></b> and <b><i>dist</i></b> are created along with a file <b><i><Main_FileName></i>.spec</b>

- run the executable in <i><b>dist/<Main_FileName>/</b></i> folder...labeled as <b><i><Main_FileName></i>.exe.</b>

- NOTE THAT FOR <i>static</i> FOLDER,  WE HAVE PROVIDED PATH RELATIVE TO OUR MAIN APP AND SO WE NEED TO COPY/MOVE THE FOLDER IN THE SAME LOCATION AS <i>App.exe</i>.