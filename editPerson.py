#!/Users/tomar/Anaconda3/python.exe
"""
Created on Sat Nov 25 16:34:21 2017 by tomar
#!/usr/bin/python3
#!C:\ProgramData\Anaconda3\python.exe#!/Users/tomar/Anaconda3/python.exe
"""
import cgi
import Tea

form = cgi.FieldStorage() # instantiate only once!
q = form.getvalue('q', 'add')	#remove default
tea = Tea.Tea()
print("Content-type: text/html \n")
if q == 'add':
    print(tea.addNewPerson())
else:
    print(tea.displayPerson(q))
