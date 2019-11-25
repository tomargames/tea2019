#!/Users/tomar/Anaconda3/python.exe
"""
Created on Monday Oct 14 20:26:57 2019 by tomar
#!/usr/bin/python3
#!/ProgramData/Anaconda3/python.exe
#!/Users/tomar/Anaconda3/python.exe
"""
import cgi
import Tea
import Users
from operator import itemgetter

def printDateRow(t):
	print('<tr valign=top><td>{}</td><td>{}</td><td>{}</td><td>'.format(tea.dateLink(t, perm), 
		tea.personLink(tea.dates[t]["H"], perm), tea.dates[t]["L"]))
	print('{}</td></tr>'.format(tea.peopleLink(t, tea.dates[t]["P"], perm)))

def printPersonRow(k):
	if "G" in tea.people[k]:
		img = '<img width={} height={} src={}>'.format(wdth, wdth, tea.users.userImage(tea.people[k]["G"]))
	else:
		img = ""
	# open tr, print image, then name, then name of bridge person
	print('''<tr valign=top><td>{}</td><td>{}</td><td>{}</td>
		'''.format(img, tea.personLink(k, perm), tea.personLink(tea.people[k]["S"], perm)))
	# number of teas, toggles to dates
	print('<td>{}</td>'.format(tea.datesLink(k, tea.people[k]["D"], perm)))
	# number of people, toggles to names
	print('<td>{}</td>'.format(tea.peopleLink(k, tea.people[k]["B"], perm)))
	if perm == '1':				#admin rights
		editHtml = '<td><a href=javascript:editPerson("{}")>edit</a></td></tr>'.format(k)
	else:
		editHtml = '</tr>'
	print(editHtml)

form = cgi.FieldStorage() # instantiate only once!
#q = form.getvalue('q', 'Y12010')	#remove default
#q = form.getvalue('q', 'P1003')	#remove default
#q = form.getvalue('q', 'G1B')	#remove default
#q = form.getvalue('q', 'D12011-04-30')	#remove default
q = form.getvalue('q', 'G1B')	#remove default
tea = Tea.Tea()
print("Content-type: text/html \n")
print("Search results for <b>{}</b></>".format(q))
print("<table border=1 width=100%>")
qt = q[0]
perm = q[1]
inp = q[2:]
if qt in ['D', 'Y']:                    #date query
	print('<tr><th>Date</th><th>Host</th><th>Address</th><th>People</th></tr>')	#header row
	if qt == 'Y':
		for t in sorted(tea.dates):
			if t[0:4] == inp:           #year of date == year being searched
				printDateRow(t)
	else:
			printDateRow(inp)
elif qt in ['P', 'G']:                                   # person query
	''' perm coming in is '1' for admin, otherwise '0' 
		initial appears as a link, table is hidden in div 
	'''
	wdth = 50
	print('<tr><th width={}>*</th>'.format(wdth))
	print('<th>Name</th><th>Bridge</th><th>Teas</th><th>People</th>')
	if perm == '1':			#admin rights for edit
		print('<th>Edit</th>')
	print('</tr>')
	if qt == 'G':			#all names starting with inp
		for k in tea.sortPeopleList(tea.people):
			letter = tea.people[k[0]]["L"][0]
			if (letter == inp):
				printPersonRow(k[0])
	else:
		printPersonRow(inp)
print('</table>')

