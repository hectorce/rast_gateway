use IO::Socket::INET;

$| = 1;

my $socket = new IO::Socket::INET (
	LocalHost => 0.0.0.0,
	LocalPort => 9000,
	Proto => tcp,
	Listen => 5,
	Reuse => 1
);

die "Cannot create socket $!\n" unless $socket;
print "server waiting for client connection on port 9000\n";

while(1) {
	my $client_socket = $socket->accept();
	my $client_address = $client_socket->peershot();
	my $client_port = $client_socket->peerport();
	print "connection fron $client_address:$client_port\n";

	my data = "";
	$client_socket->recv($data, 1024);
	print "received data: $data\n";

	$data = "ok";
	$client_socket->send($data);

	shutdown($client_socket, 1);
}

$socket->close();

