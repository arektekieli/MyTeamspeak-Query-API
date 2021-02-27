from TeamspeakAbstract import TeamspeakAbstract
from TeamspeakResult import TeamspeakResult
import select
import socket
import re
from time import sleep, time

class Teamspeak(TeamspeakAbstract):
    def __init__(self, host, port, username, password, nick='ArasBot'):
        super().__init__()
        self.host = host                
        self.port = port
        self.username = username
        self.password = password
        self.nick = nick
        self.lastErrorId = 0
        self.lastErrorMsg = ''
        self.nextAvaibleQuery = 0
        self.queryInterval = 800
        self.connection = False
        self.clid = None

    def connect(self):
        # Create socket object
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.host, self.port))

    def authenticate(self):
        # Login to Teamspeak server as a query client
        self.query('login {} {}'.format(self.username, self.password))
        if self.lastErrorId != 0:
            return False

        return True

    def query(self, query):
        # Returns teamspeak format data

        # Check if conection is established
        if self.connection == False:
            return False

        # Wait until we can send a query
        while time() * 1000 < self.nextAvaibleQuery:
            sleep(0.001)
        
        # Set next avaible query time in miliseconds
        # This preventing flood ban in case we have query limits on server
        self.nextAvaibleQuery = int(time() * 1000 + self.queryInterval)

        # Send query to teamspeak server
        print('=======> ', query)
        self.connection.send('{}\n'.format(query).encode('utf-8'))
        
        # Receive data until error message occurs
        return TeamspeakResult(self.receiveUntilError())

    '''def recvUntil(self, text, data=b''):
        # Receive data from socket until specific pattern occurs
        while text not in data[(len(text) * -1):]:
            d = self.connection.recv(1024)
            if len(d) == 0:
                return False
            
            data += d.decode('ascii', 'ignore')
        return data'''

    def receiveNotifyTextMessage(self):
        data = ""
        while True:
            socket_list = [self.connection]
            r, w, e = select.select(socket_list, [], [], 60)
            for sock in r:
                if sock == self.connection:
                    data = data + sock.recv(4096).decode("utf-8")
                    if "\n\r" in data:
                        return TeamspeakResult(data).toList()[0]

            return None

    def receiveUntilError(self):
        data = ''
        # Receive data from socket until error message occurs then read until \n\r
        while len(re.findall('error id=[0-9]{1,5} msg=.{1,999999}\n\r', data)) == 0:
            d = self.connection.recv(1024)
            if len(d) == 0:
                return False
            
            data += d.decode('ascii', 'ignore')
        self.setError(data)
        return data

    


        
