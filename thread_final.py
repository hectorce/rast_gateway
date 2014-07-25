import multiprocessing
from socket import *
import thread
# ------------------
#import socket
#import sys
import datetime
import time
import MySQLdb

class WebRast:

	conn = ''
	cur = ''
  
	def rastDB(self):
		# Connection database
		#db = MySQLdb.connect(host="localhost", # your host, usually localhost
		#                     user="root", # your username
		#                     passwd="12345678", # your password
		#                      db="db_rast") # name of the data base

		# Open database connection
		self.conn = MySQLdb.connect("localhost", "root", "12345678", "db_rast" )

		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		self.cur = self.conn.cursor()

	def rastDBClose(self):
                self.cur.close()
                self.conn.close()

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


# ------------------------------------------------------------------------
 
def handler(clientsocket, clientaddr):

	# call class
	rast = WebRast()
	rast.rastDB()

	data_con = datetime.datetime.now().strftime("%d/%m/%y")
	hora_con = datetime.datetime.now().strftime("%H:%M:%S")
	fdata = datetime.datetime.now().strftime("%y-%m-%d")
	print hora_con + ' Accepted connection from: ' + data_con , clientaddr
 
	try:

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

	except socket.error, e:
            # Something else happened, handle error, exit, etc.
            print e
	    pass

	finally:
	    clientsocket.close()
	    print hora_con + ' close client connection: ' , clientaddr
	    rast.rastDBClose()
	    print hora_con + ' close database!'
	    #raise
 
if __name__ == "__main__":
 
   #host = 'gwce.dyndns.org'
   #port = 50000
   #buf = 1024
   #server_address = ('gwce.dyndns.org', 50000)
   server_address = ('fernandodesigner.com', 50000)
   #server_address = ('ceararast.com', 50000)
   #server_address = ('localhost', 50000)

   serversocket = socket(AF_INET, SOCK_STREAM)
   #serversocket.settimeout(30)
   serversocket.bind(server_address)
   serversocket.listen(2)

   try:
       while True:
           print 'Starting up on %s port %s' % server_address
           print "Server is listening for connections\n"

           clientsocket, clientaddr = serversocket.accept()

           #rast_thread = thread.start_new_thread(handler, (clientsocket, clientaddr))
           rast_thread = multiprocessing.Process(target=handler, args=(clientsocket, clientaddr))
           rast_thread.daemon = True
           rast_thread.start()
           print "Started thread: ", rast_thread

   except:
       #logging.exception("Unexpected exception")
       print ("Unexpected exception")   

   finally:
       #logging.info("Shutting down")
       print "Shutting down"
       for rast_thread in multiprocessing.active_children():
           #logging.info("Shutting down process %r", rast_thread)
           print ("Shutting down thread: ", rast_thread)
           rast_thread.terminate()
           rast_thread.join()
