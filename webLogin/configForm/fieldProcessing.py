import sqlite3
import os 
import sys
'''
1st function 
When the user will connect, the first thing main would call is this function to check whether or not VALID parameters have been already entered 

2nd function 
Once the user enter its parameter this function will check if the user entered a new Spotify ID and Spotify Secrets 
- if not, it will 

This is the part where we call app :
- 1st check if sqlite table, first case 'spotifyID' is empty 
	- if empty -> app -> sign up 
		- return form and inpack it here
		- handle errors & wrong inputs 
	if not empty -> message consol (the tester is already configurated, do you want to make som modifications ?)
		if yes -> login (everything is optional, only change what you need)
			- try to display the already existing
/|\ WARNING !! problem to solve !! -> if the user want to modify the contenant he should be able to modify the already registered array
keep the same secrets and ID and be able to modify one field apon the others. 

-> selectfield -> default display (Choose)

'''

class Fields():

	def __init__(self):
		self.dataBase = 'webLogin/configForm/database4.db'

	def extractDB(self)	:

		conn = sqlite3.connect(self.dataBase)
		c = conn.cursor()
		# c.execute('mode line select * from user')
		c.execute("select * from user")
		sqliteDB = c.fetchall()
		# for row in sqliteDB:
		    # print(row)
		# c.close()

		if not sqliteDB :
			print('\n You have not configure Speech API Tester yet. connect to the link below in your browser to configure it \n')
			os.system('python webLogin/configForm/app.py empty')
		else :
			print("\n You have already configure Speech API Tester, do you want to add some changes ? you won't need to reconfigure it all from scratch, just the fields you need to change \n")
			if sys.version_info[0] < 3:
			    response = raw_input("\n Answer Yes or [No]: ").lower()
			else :
				response = input("\n Answer Yes or [No]: ").lower()


			# the user write yes or no .lower()  -- Answer default [No]
			if response in ['yes','y','yep', 'yeah'] :
				 print('Connect to the the link below and fill the form \n') 
				 os.system('python webLogin/configForm/app.py full') #/login 
			else :
				pass

		return sqliteDB


def selectLastField(sqliteDB,i):

	'''
		output the last field the user filled
		arg : SQLite database and index of field 
		returns : last filled field 
	'''

	for row in reversed(sqliteDB):
		if row[i] != '':
			return row[i]