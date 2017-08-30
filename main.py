#_*_ coding:utf-8 _*_

from dataProcessing import *
from webLogin.configForm.fieldProcessing import *
import sys
import cx_freeze


if __name__ == '__main__':

	# Initializing inputs from SQLite3 server
	# (*) Means if the user did not fill the field, the input value goes default 
	fields = Fields()
	for i in range(3): # If sqlite is emplty, ask the user to fill it by filling the form field (3 tries) 
		fld = fields.extractDB() # Calls fieldProcessing
		if fld:
			
			if selectLastField(fld,1) and selectLastField(fld,2) and selectLastField(fld,3): 
				CLIENT_ID  =  selectLastField(fld,1)
				CLIENT_SECRET = selectLastField(fld,2)
				PLAYLISTSURI = selectLastField(fld,3).split("\r\n")
				api = selectLastField(fld,4) # Choose an API to test
				hints = selectLastField(fld,5) # Hints / no hints 
				alt = selectLastField(fld,6) # Alternatives / no alternatives
				focus = selectLastField(fld,7) # Choose if you want to test speech APIs on Artists, Albums or Tracks 
				if selectLastField(fld,8) : # (*) [200]
					maxPlaylist = selectLastField(fld,8) 
				else : maxPlaylist = 200
				if selectLastField(fld,9): # (*) [100]
					maxSample = selectLastField(fld,9)
				else : maxSample = 100
				break # continue to next step when all the required info are stocked in the SQLite3 server
			else : print('\nSpotify ID, Secrets and your Spotify Playlist URI must be filled. Connect to http://127.O.0.1:5000 \n') 
		else : print('\nYou need to input parameters in the form field on your browser. Connect to http://127.O.0.1:5000\n')

	# Extract music data from Spotify - calls dataProcessing
	dataList = DataFromSpotify(client_id= CLIENT_ID,client_secret=CLIENT_SECRET, playlistsURI=PLAYLISTSURI,maxSample=maxSample,maxPlaylist=maxPlaylist)
	
	# Delete redundancies
	listsToClean = CleaningDB() 
	spotifyDB = list(getCleanedSpDB(dataList,listsToClean,focus))


	print('\n Hooray ! You extracted {} {} name from Spotify !!'.format(len(spotifyDB),focus))
	# TODO make it easy to choose if we want to see lists size or not , for now fonctions return only lists with no size

	#Speech API testing
	recognized , unrecognized =  recognitionTest(text=spotifyDB,focus=focus,alt=alt,api=api,hints=hints)
	# output score to csv local files
	score(spotifyDB,recognized, unrecognized, focus, api,alt=alt,hints=hints)
