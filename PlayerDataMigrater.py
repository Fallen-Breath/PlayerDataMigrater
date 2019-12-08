# -*- coding: utf-8 -*-
import urllib2
import os
import shutil
import json

version = '1.0'
PlayerDataFolders = \
[
	('advancements', 'json'),
	('playerdata', 'dat'),
	('stats', 'json')
]

def name_to_uuid_fromAPI(name):
	url = 'http://tools.glowingmines.eu/convertor/nick/' + name
	response = urllib2.urlopen(url)
	data = response.read()
	js = json.loads(str(data))
	return js['offlinesplitteduuid']


print('''Migrate player data after player renamed
Put me inside the world folder
''')
oldName = raw_input("Old Name = ")
newName = raw_input("New Name = ")
doOverwrite = input("Overwrite existed file? (0 / 1) = ") == 1
doDelete = input("Delete old file? (0 / 1) = ") == 1

print('Getting offline UUIDs')
oldUUID = name_to_uuid_fromAPI(oldName)
newUUID = name_to_uuid_fromAPI(newName)

print('Old offline UUID = ' + oldUUID)
print('New offline UUID = ' + newUUID)

for folder in PlayerDataFolders:
	path = folder[0]
	extension = folder[1]
	oldFile = path + '/' + oldUUID + '.' + extension
	newFile = path + '/' + newUUID + '.' + extension
	if not os.path.isfile(oldFile):
		print(oldFile + ' not found, pass')
		continue
	if os.path.isfile(newFile):
		if not doOverwrite:
			print(newFile + ' exists, not overwrite, pass')
			continue
		else:
			print(newFile + ' exists, overwrite')
	print('Moving ' + oldFile + ' to ' + newFile)
	shutil.copy(oldFile, newFile)
	if doDelete:
		print('Deleting ' + oldFile)
		os.remove(oldFile)

raw_input("Finished")