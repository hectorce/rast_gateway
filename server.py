import socket
import sys
import datetime
import time
import MySQLdb

# Connection database
#db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                     user="root", # your username
#                     passwd="12345678", # your password
#                      db="db_rast") # name of the data base

# Open database connection
db = MySQLdb.connect("localhost", "root", "12345678", "db_rast" )

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# -------

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create a UDP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
#server_address = ('localhost', 9000)
server_address = ('gwce.dyndns.org', 9000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
	data_con = datetime.datetime.now().strftime("%d/%m/%y")
	hora_con = datetime.datetime.now().strftime("%H:%M:%S")
	fdata = datetime.datetime.now().strftime("%y-%m-%d")
        print >>sys.stderr, hora_con + ' connection from: ' + data_con , client_address

        # Receive the data in small chunks and retransmit it
        while True:

            data = connection.recv(1024)

	    hora_con = datetime.datetime.now().strftime("%H:%M:%S")
	    print >>sys.stderr, hora_con + ' received: "%s"' % data
            if data:
                print >>sys.stderr, hora_con + ' sending data back to the client'
                connection.sendall(data)

		#save table
#		sql = "insert into tb_dados (data_recebe, data_grava, linha)
#			 values ('+ data_con +' '+hora_con+', 'datetime', '+data+')"
#		sql = 

		if data.find('##'):

		  cur.execute ("insert into tb_dados (data_recebe, data_grava, linha) values (%s, %s, %s)" , (fdata +' '+ hora_con, time.strftime('%Y-%m-%d %H:%M:%S'), data))

		  #cur.execute(sql)
		  #print >>sys.stderr, sql
		  print >>sys.stderr, 'saved!'
		else:
		  print >>sys.stderr, 'no saved!'

            else:
                print >>sys.stderr, hora_con + ' no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()
	#cur.close()
