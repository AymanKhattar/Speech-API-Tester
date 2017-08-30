import sqlite3


dataBase = 'database4.db'

conn = sqlite3.connect(dataBase)
c = conn.cursor()
# c.execute('mode line select * from user')
c.execute("select * from user ")
sqliteDB = c.fetchall()
spotId = []
for row in reversed(sqliteDB):
	# print row[0]
	spotId.append(row[5])	    
print(spotId)
c.close()

