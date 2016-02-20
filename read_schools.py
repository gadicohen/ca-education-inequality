from __future__ import division
# coding=utf-8
from dbfread import DBF
import sys
#from geopy.geocoders import Nominatim
import numpy as np
import xlrd
import json
from sklearn.cluster import dbscan
from sklearn.preprocessing import StandardScaler



schools_with_locations = {}
book = xlrd.open_workbook('pubschls.xls')
sh = book.sheet_by_index(0)
headings = sh.row(0)
# for i,h in enumerate(headings):
# 	if h.value == 'Latitude':
# 		print i
for rx in range(sh.nrows):
	l = sh.row(rx)
	#print 
	schools_with_locations[l[0].value] = (l[36].value, l[37].value)
	#print l[0].value
	#print l
	#[6:]
#geolocator = Nominatim()
all_schools = {}
class School(object):
	def __init__(self, items):
		#self.id = id
		
		for (name, value) in items:
			setattr(self, name, value)

	def setCoors(self, lat, lon):
		self.long = lon
		self.lat = lat

max = 0

for s in DBF('14avgdb.dbf', recfactory=School, encoding='Cp1252'):
	#print s.sname
	#location = geolocator.geocode(s.sname)
	# if location is not None:
	# 	print location.latitude, location.longitude
	# 	s.setCoors((location.latitude, location.longitude))
	# else:
	if s.cds in schools_with_locations:
		location = schools_with_locations[s.cds]
		#print location[0],location[1]
		s.setCoors(location[0],location[1])
		p = [s.num11, s.num12, s.num13]
		p = [float(x) for x in p if x != '']
		

		avg_s = sum(p) / len(p)
		if avg_s > max:
			max = avg_s
		#print avg_s
		all_schools[s.cds] = (location[0],location[1],s.avg_w, str(avg_s), s.sname) #lat, long

	else:
		print s.sname
print avg_s


# html_insertion = []
# 		#.encode('ascii', 'ignore').decode('ascii')
# for k,v in all_schools.iteritems():
# 	if v[2] < 400:
# 		html_insertion.append('<circle cx="'+v[1]+'" cy="'+v[2]+'" r="2" stroke="black" stroke-width="0" fill="red" />')
# 	elif v[2] < 700:
# 		html_insertion.append('<circle cx="'+v[1]+'" cy="'+v[2]+'" r="2" stroke="black" stroke-width="0" fill="yellow" />')
# 	else:
# 		html_insertion.append('<circle cx="'+v[1]+'" cy="'+v[2]+'" r="2" stroke="black" stroke-width="0" fill="green" />')

#data = StandardScaler().fit_transform(all_schools)
#db = cluster.DBSCAN(min_samples=1).fit(all_schools)
# html_insertion = ''.join(html_insertion)




with open('locations.json', 'w') as f:
	json.dump(all_schools, f)
# x = School()
# class Record(object):
#     def __init__(self, items):
#         for (name, value) in items:
#             setattr(self, name, value)

# for record in DBF('people.dbf', recfactory=Record, lowernames=True):
#     print(record.name, record.birthdate)