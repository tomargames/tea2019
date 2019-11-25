#!/Users/tomar/Anaconda3/python.exe
"""
Created on Sat May 27 16:34:21 2017 by tomar
#!/usr/bin/python3
#!/ProgramData/Anaconda3/python.exe
#!/Users/tomar/Anaconda3/python.exe
# """
import sys
try:
	import gUtils
	import Users
except:
	sys.path.append("..")
	import gUtils
	import Users
import cgi
import random
import Tea
print("Content-type: text/html \n")
print('''
<html><head><title>Tea</title>
<LINK REL='StyleSheet' HREF='/python/tomar.css?{}'  TYPE='text/css' TITLE='ToMarStyle' MEDIA='screen'>
<link href='//fonts.googleapis.com/css?family=Didact Gothic' rel='stylesheet'>
<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="932688745244-i4vfeap5jgu8id5dagrc49786vvs0qrf.apps.googleusercontent.com">
</head>
<body>
'''.format(random.randrange(9999)))
form = cgi.FieldStorage() # instantiate only once!
gid = form.getvalue('gId', '')	#remove default
name = form.getvalue('gName', '')	#remove default
gMail = form.getvalue('gMail', '')	#remove default
gImg = form.getvalue('gImage', '')	#remove default
oper = form.getvalue('oper','')
#print("oper is {}".format(oper))
#gid = '106932376942135580175'
print('''
<form name="gForm" method="POST" action="#">
<input type="hidden" name="gId" value="{}">
<input type="hidden" name="gName" value="{}">
<input type="hidden" name="gMail" value="{}">
<input type="hidden" name="gImage" value="{}">
<input type="hidden" name="oper" id="oper">
'''.format(gid, name, gMail, gImg))
if gid == '':
	gUtils.googleSignIn()
else:
	users = Users.Users()
	authTea = users.authenticate(gid, name, gMail, gImg, users.TEA)
	authAdm = users.authenticate(gid, name, gMail, gImg, users.ADMIN)
	print(authTea[1])
	if authTea[0] == '1':
		tea = Tea.Tea()
		if oper != '':
			rtn = 'noGood'
			if authAdm[0] == '1':
				if oper == 'tea':
					#print("got here: {}".format(form))
					try:
						dt = form.getvalue('dt')
						hs = form.getvalue('hs')
						ad = form.getvalue('ad')
						if dt > '' and hs > '' and ad > '':
							rtn = tea.saveTeas(dt, hs, ad)
					except Exception as e:
						print('''ERROR: {}'''.format(str(e)))
				else:
					pid = form.getvalue('id', '')
					first = form.getvalue('first', '')
					last = form.getvalue('last', '')
					src = form.getvalue('src', '')
					ggl = form.getvalue('ggl', '')
					teaString = ''
					for t in sorted(tea.dates, reverse=True):
						if form.getvalue('c{}'.format(t), '') == 'on':
							teaString += '1'
						else:
							teaString += '0'
					if oper == 'add':
						tea.people[pid] = {}
						tea.people[pid]["B"] = []
						tea.people[pid]["H"] = []
						tea.people[pid]["D"] = []
					#print('{} {} {} {} {} {}'.format(pid, first, last, src, teaString, ggl))
					rtn = tea.updatePerson(pid, first, last, src, teaString, ggl)
				if rtn == 'good':
					print('<script> document.gForm.submit(); </script>')
				else:
					print(rtn)
			else:
				print("Error: not admin and oper is {}".format(oper))
		else:
			print(tea.jsFunctions(authAdm[0]))
	else:
		print('''
Welcome to ToMarGames Friends and Family!<br><br>It looks like you've landed on a page you don't have permission to access.
				''')
print('</form></body></html>')

'''
		else:
			print(tea.displayTeas())
			print(tea.displayPeople(authAdm[0], users))
			if authAdm[0] == '1':
				print('<br><br><a href=javascript:editPerson("add");>Add a person</a>')
'''
