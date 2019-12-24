from Teamspeak import Teamspeak
from TeamspeakClient import TeamspeakClient

class TeamspeakAPI(Teamspeak):
    def __init__(self, host, port, sid, login, password, nick='ArasBot'):
        super().__init__(host, port, sid, login, password, nick)

    def getClientList(self):
        result = self.query('clientlist')
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result.fetch()]
