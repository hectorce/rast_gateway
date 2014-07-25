import socket
import sys
import datetime
import time
import MySQLdb

class WebRast:

  db = ''
  cur = ''

  def __init__(self):

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

    # -------

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a UDP/IP socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    #server_address = ('localhost', 9000)
    server_address = ('gwce.dyndns.org', 50000)
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
	#print hora_con + ' connection from: ' + data_con , client_address

        # Receive the data in small chunks and retransmit it
        while True:

          data = connection.recv(1024)

	  hora_con = datetime.datetime.now().strftime("%H:%M:%S")
	  print >>sys.stderr, hora_con + ' received: "%s"' % data
	  #print hora_con + ' received: "%s"' % data

          if data:
            print >>sys.stderr, hora_con + ' sending data back to the client'
            connection.sendall(data)

	    if data.find('##'):
	      mntData = fdata + ' ' + hora_con
	      dtAtual = time.strftime('%y-%m-%d %H:%M:%S')
              print >>sys.stderr, self.gravaDados(mntData, dtAtual, data)
	      #print >>sys.stderr, 'saved!'
	    else:
	      print >>sys.stderr, 'no saved!'

          else:
             print >>sys.stderr, hora_con + ' no more data from', client_address
	     #print hora_con + ' no more data from', client_address
             break
           
      except:
	hora_con = datetime.datetime.now().strftime("%H:%M:%S")
        print >>sys.stderr, hora_con + ' Error: socket'
	#print hora_con + ' Error: socket'
	#connection.close()
	pass
 
      finally:
        # Clean up the connection
        connection.close()
	#cur.close()

  def gravaDados(self, data1, data2, args):

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

    return 'saved in database!'


# call class
rast = WebRast()



