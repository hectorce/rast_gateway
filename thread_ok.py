from socket import *
import thread
# ------------------
#import socket
#import sys
import datetime
import time
import MySQLdb

class WebRast:

	db = ''
	cur = ''
  
	def rastDB(self):
		# Connection database
		#db = MySQLdb.connect(host="localhost", # your host, usually localhost
		#                     user="root", # your username
		#                     passwd="12345678", # your password
		#                      db="db_rast") # name of the data base

		# Open database connection
		self.db = MySQLdb.connect("localhost", "root", "12345678", "db_rast" )

		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		self.cur = self.db.cursor() 

	def saveData(self, data1, data2, args):
		mydata = args.split(",")

		emei = mydata[0]
		tipo = mydata[1]
		data_trans = mydata[2]
		usu_admin = mydata[3]
		op1 = mydata[4]
		altitude = mydata[5]
		op2 = mydata[6]
		latitude = mydata[7]
		op3 = mydata[8]
		longitude = mydata[9]
		op4 = mydata[10]
		velocidade = mydata[11]
		naosei = mydata[12]
		naosei2 = mydata[13]

		sql = """ insert into tb_transmissao (data_recebe, data_grava, emei, tipo, data_trans,
		usu_admin, op1, altitude, op2, latitude, op3, longitude, op4, velocidade, naosei, naosei2)
		values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ) """
		params = (data1, data2, emei, tipo, data_trans, usu_admin, op1, altitude, op2, latitude, op3, longitude, op4, velocidade, naosei, naosei2)
		#params = (fdata + ' ' + hora_con, time.strftime('%y-%m-%d %H:%M:%S'), mydata)

		self.cur.execute(sql, params)
		#print str(sql + params)

	        return 'data saved in database!'


# call class
#rast = WebRast()

# ------------------------------------------------------------------------
 
def handler(clientsocket, clientaddr):

	# call class
	rast = WebRast()
	rast.rastDB()

	data_con = datetime.datetime.now().strftime("%d/%m/%y")
	hora_con = datetime.datetime.now().strftime("%H:%M:%S")
	fdata = datetime.datetime.now().strftime("%y-%m-%d")
	print hora_con + ' Accepted connection from: ' + data_con , clientaddr
 
	while 1:
		data = clientsocket.recv(1024)
		
		hora_con = datetime.datetime.now().strftime("%H:%M:%S")
		print hora_con + ' received: "%s"' % data

		if data:
			print hora_con + ' sending data back to the client'
			clientsocket.sendall(data)

			if data.find('##'):
				mntData = fdata + ' ' + hora_con
				dtAtual = time.strftime('%y-%m-%d %H:%M:%S')
				print rast.saveData(mntData, dtAtual, data)
				#print 'data saved!'
			else:
				print 'data no saved!'

		else:
			print hora_con + ' no more data from: ', clientaddr
			break

	print hora_con + ' close client connection: ' , clientaddr
	clientsocket.close()
 
if __name__ == "__main__":
 
   #host = 'gwce.dyndns.org'
   #port = 50000
   #buf = 1024
   #server_address = ('gwce.dyndns.org', 50000)
   server_address = ('fernandodesigner.com', 50000)

   serversocket = socket(AF_INET, SOCK_STREAM)
   serversocket.bind(server_address)
   serversocket.listen(2)
 
   while 1:
      print 'Starting up on %s port %s' % server_address
      print "Server is listening for connections\n"
      clientsocket, clientaddr = serversocket.accept()
      thread.start_new_thread(handler, (clientsocket, clientaddr))
   serversocket.close()

