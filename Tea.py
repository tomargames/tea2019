#!/Users/tomar/Anaconda3/python.exe
"""
Created on Sun Jan 22 20:26:57 2017 by tomar
#!/usr/bin/python3
#!/ProgramData/Anaconda3/python.exe
#!/Users/tomar/Anaconda3/python.exe
"""
import json
import sys
import os
from operator import itemgetter
try:
	import utils
except:
	sys.path.append("..")
	import utils
import Users

class Tea(object):
	def __init__(self):
		'''
			Dates:
				Fields coming in are H and L, date is the key
				explodeTeas will populate P with ids of people who were there
			People:
				Fields coming in are F, L, S, and T, and G if there's a gId
				explodeTeas will  populate B with ids of people bridged to, and D with tea dates, and H
		'''
		with open("teas.json") as dData:
			self.dates = json.load(dData)
		with open("people.json") as pData:
			self.people = json.load(pData)
		for d in self.dates:
			self.dates[d]["P"] = []
		for p in self.people:
			self.explodeTeas(p)
		# initialize users
		self.users = Users.Users()

	def explodeTeas(self, p):
		'''
			input: pointer to self.people record, "T" is base32 representation of teas
					 pointer to self.dates
			output: add "D" to self.people record, teaList
					add "B" to self.people record, people who they were a bridge to
					add "H" to self.people record, teas they hosted
					add "P" to self.dates record for teas attended
		'''
		in32 = self.people[p]["T"]
		binaryOut = ""
		self.people[p]["B"] = []
		self.people[p]["H"] = []
		self.people[p]["D"] = []
		binaryOut = self.makeTeaString(in32)
		for n, d in enumerate(sorted(self.dates, reverse=True)):
			if binaryOut[n] == "1":
				self.people[p]["D"].append(d)
				self.dates[d]["P"].append(p)
			if self.dates[d]["H"] == p:
				self.people[p]["H"].append(d)
		for i in self.people:
			if self.people[i]["S"] == p:
				self.people[p]["B"].append(i)

	def jsFunctions(self, perm):
		''' perm is 1 for admin, otherwise 0
		'''
		returnHtml = ''
		returnHtml += '''
<table border=0><tr><td width=50%>		
<input type="text" id="searchBox" list="searchList" onClick="javascript:doSearch();" style="font-size:24px; width:400px; color: darkgreen; background-color: lightgreen;" placeHolder="search">
<input type="button" style="font-size:24px; color:lightgreen; background-color:darkgreen" value="Search" onClick="javascript:doSearch();">
<input type="button" style="font-size:24px; color:azure; background-color:cornflowerblue;" value="Clear" onClick="javascript:doClear();">
</td>
'''
		if perm == '1':				#admin rights
			returnHtml += '''
<td style="text-align: right;"><a href="javascript:addPerson();">Add person</a></td>
<td style="text-align: center;"><a href="javascript:addTea();">Add Tea</a></td>
'''
		returnHtml += '</tr></table>'
		returnHtml += self.dataList(perm)
		returnHtml += '''
<script>
function goTo(x)
{
	gForm.action = x;
	gForm.submit();
}
function doClear()
{
	document.getElementById("searchBox").value = '';
	document.getElementById("searchBox").focus();
}
function toggleDiv(id)
{
	var div = document.getElementById(id);
	if(div.style.display != 'none')
	{
		div.style.display = 'none';
	}
	else
	{
		div.style.display = 'block'
	}
}
function doSearch(tag)
{
	//alert("in search with tag=" + tag);
	if (typeof(tag) == "undefined")
	{
		tag = document.getElementById("searchBox").value;
	}
	if (tag > '')
	{
		var xhttp = new XMLHttpRequest();
  		xhttp.onreadystatechange = function() 
		{
    		if (this.readyState == 4 && this.status == 200) 
			{
     			document.getElementById("searchResults").innerHTML = this.responseText;
				doClear();	 
    		}
 		};
	 	xhttp.open("POST", "srchResults.py?q=" + tag, true);
 		xhttp.send();
	}
}
function addPerson()
{
	editPerson('add');
}	
function addTea()
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() 
	{
    	if (this.readyState == 4 && this.status == 200) 
		{
     		document.getElementById("searchResults").innerHTML = this.responseText;
			doClear();
		}	 
 	};
	document.getElementById("oper").value = 'tea';
	xhttp.open("POST", "editTea.py", true);
 	xhttp.send();
}

function editPerson(x)
{
	if (x > '')
	{
		var xhttp = new XMLHttpRequest();
  		xhttp.onreadystatechange = function() 
		{
    		if (this.readyState == 4 && this.status == 200) 
			{
     			document.getElementById("searchResults").innerHTML = this.responseText;
				doClear();	 
    		}
 		};
		document.getElementById("oper").value = x;
	 	xhttp.open("POST", "editPerson.py?q=" + x, true);
 		xhttp.send();
	}
}
'''
		returnHtml += '''
document.getElementById("searchBox").focus();
</script>
<div id="searchResults">
</div>
'''
		return returnHtml

	def dataList(self, perm):
		returnHtml = '<datalist id="searchList">'
		letters = []
		years = []
		for p in sorted(self.people):
			returnHtml += '''<option value="P{}{}">{}</option>'''.format(perm, p, self.personName(p)) 
			letters.append(self.people[p]["L"][0])
		for d in sorted(self.dates):
			returnHtml += '''<option value="D{}{}">{}</option>'''.format(perm, d, self.dateDisplay(d))
			years.append(d[0:4])
		letters = list(dict.fromkeys(letters))			#eliminate dupes
		years = list(dict.fromkeys(years))				#eliminate dupes
		for l in sorted(letters):
			returnHtml += '<option value="G{}{}">People: {}</option>'.format(perm, l, l)
		for y in sorted(years):
			returnHtml += '<option value="Y{}{}">Year: {}</option>'.format(perm, y, y)
		returnHtml += "</datalist>"
		return returnHtml

	def personName(self, id):
		return '{} {}'.format(self.people[id]["F"],self.people[id]["L"])

	def dateDisplay(self, d):
		return '{}-{}-{}'.format(d[5:7], d[8:], d[0:4])

	def sortPeopleList(self, L):
		'''
			L is a list of people records, will be sorted by last name, first name, key will be [0] of each record in return list
		'''
		sorter = []
		for p in L:
			sorter.append((p, self.people[p]["L"] + " " + self.people[p]["F"]))
		return sorted(sorter, key=itemgetter(1))

	def dateLink(self, d, perm):
		return '''<a href=javascript:doSearch("D{}{}")>{}</a>'''.format(perm, d, d)

	def peopleLink(self, t, L, perm):
		returnHtml = '''
<a href="javascript:;" onClick=javascript:toggleDiv("divP{}")>{}</a>
<div id="divP{}" style="display:none;";>'''.format(t, len(L), t)
		returnHtml += '<table>'
		for k in tea.sortPeopleList(L):
			returnHtml += '<tr><td>{}</td></tr>'.format(tea.personLink(k[0], perm))
		returnHtml += '</table>'
		return returnHtml

	def datesLink(self, k, L, perm):
		returnHtml = '''
<a href="javascript:;" onClick=javascript:toggleDiv("divD{}")>{}</a>
<div id="divD{}" style="display:none;";>'''.format(k, len(L), k)
		returnHtml += '<table>'
		for d in tea.people[k]["D"]:
			hoster = ""
			if d in tea.people[k]["H"]:
				hoster = " (host)"
			returnHtml += '<tr><td>{}{}</td></tr>'.format(tea.dateLink(d, perm), hoster)
		returnHtml +=  '</table></div>'
		return returnHtml

	def personLink(self, p, perm):
		returnHtml = '''<a href=javascript:doSearch("P{}{}")>{}</a>'''.format(perm, p, 
			tea.personName(p))
		return returnHtml

	def displayPerson(self, pId):
		returnHtml = 'ID: {}'.format(pId)
		returnHtml += '''<input type="submit" value="Save File"> <br>'''
		returnHtml += '<input type="hidden" name="id" value="{}">'.format(pId)
		returnHtml += 'FirstName: <input type="text" name="first" required value="{}"><br>'.format(self.people[pId]["F"])
		returnHtml += 'LastName: <input type="text" name="last" required value="{}"><br>'.format(self.people[pId]["L"])
		returnHtml += 'SourceID: <input type="text" name="src" required value="{}"><br>'.format(self.people[pId]["S"])
		if "G" in self.people[pId]:
			returnHtml += 'GoogleID: <input type="text" name="ggl" value="{}"><br>'.format(self.people[pId]["G"])
		else:
			returnHtml += 'GoogleID: <input type="text" name="ggl"><br>'
		for t in sorted(self.dates, reverse=True):
			returnHtml += '{}: <input type="checkbox" name="c{}" '.format(t, t)
			if t in self.people[pId]["D"]:
				returnHtml += 'checked'
			returnHtml += '><br>'
		return returnHtml

	def savePeople(self):
		for p in self.people:
			del self.people[p]["B"]
			del self.people[p]["D"]
			del self.people[p]["H"]
		os.rename("people.json", "people{}.json".format(utils.timeStamp()))
		outfile = open('people.json', 'w')
		json.dump(self.people, outfile)
		outfile.close()
	
	def addNewPerson(self):
		'''
			id will be len(self.people) as a string
		'''
		pId = utils.formatNumber(len(self.people), 3)
		returnHtml = 'ID: {}'.format(pId)
		returnHtml += '<input type="submit" value="Save"> <br>'
		returnHtml += '<input type="hidden" name="id" value="{}">'.format(pId)
		returnHtml += 'FirstName: <input type="text" name="first" required><br>'
		returnHtml += 'LastName: <input type="text" name="last" required><br>'
		returnHtml += 'SourceID: <input type="text" name="src" required><br>'
		returnHtml += 'GoogleID: <input type="text" name="gid"><br>'
		for t in sorted(self.dates, reverse=True):
			returnHtml += '{}: <input type="checkbox" name="c{}"><br>'.format(t, t)
		return returnHtml

	def addTea(self):
		'''
			id will be date string (YYYY-MM-DD)
		'''
		returnHtml = 'Date: <input type="text" name="dt" required><br>'
		returnHtml += 'Host: <input type="text" name="hs" required><br>'
		returnHtml += 'Address: <input type="text" name="ad" required><br>'
		returnHtml += '<input type="submit" value="Save">'
		return returnHtml

	def updatePerson(self, pid, first, last, src, teaString, ggl):
		self.people[pid]["F"] = first
		self.people[pid]["L"] = last
		self.people[pid]["S"] = src
		if ggl > "":
			self.people[pid]["G"] = ggl
		self.people[pid]["T"] = self.compressTeas(teaString)
		self.savePeople()
		return 'good'

	def saveTeas(self, dt, hs, addr):
		print(''' in saveTeas, dt is {}, hs is {}, addr is {}'''.format(dt, hs, addr))
		if dt > '' and hs > '' and addr > '':
			self.dates[dt] = {}
			self.dates[dt]["L"] = addr
			self.dates[dt]["H"] = hs
			os.rename("teas.json", "teas{}.json".format(utils.timeStamp()))
			outfile = open('teas.json', 'w')
			json.dump(self.dates, outfile)
			outfile.close()
			return 'good'
		else:
			return "ERROR SAVING RECORD: {}, {}, {}",format(dt, hs, addr)

	def compressTeas(self, binaryIn):
		if len(binaryIn) < 6:
			return utils.make32(binaryIn)
		else:
			return self.compressTeas(binaryIn[0:-5]) + utils.make32(binaryIn[-5:])

	def makeTeaString(self, in32):
		binaryOut = ''
		for c in in32:
			binaryOut += utils.makeBinary(c)
		#binaryOut should have same length as number of teas, so pad with 0000
		while (len(binaryOut) < len(self.dates)):
			binaryOut = "0" + binaryOut
		return binaryOut[-len(self.dates):]

tea = Tea()
#tea.saveTeas('2019-11-30', '003', '17 Locust Street, Lancaster')
