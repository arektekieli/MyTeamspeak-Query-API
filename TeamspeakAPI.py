from Teamspeak import Teamspeak
from TeamspeakClient import TeamspeakClient

class TeamspeakAPI(Teamspeak):
    def __init__(self, host, port, sid, login, password, nick='ArasBot'):
        super().__init__(host, port, sid, login, password, nick)

    def safeQuery(self, query):
        result = self.query(query)

        if self.lastErrorId != 0:
            return False

        return result 

    def clientinfo(self, client):
        # Returns TeamspeakResultItem object
        # client must be clid or TeamspeakClient class
        try:
            if isinstance(client, TeamspeakClient):
                return self.safeQuery('clientinfo clid={}'.format(client.clid)).items[0]
            else:
                return self.safeQuery('clientinfo clid={}'.format(client)).items[0]
        except:
            return False

    def clientlist(self):
        # Returns list of TeamspeakClient objects
        result = self.safeQuery('clientlist')
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result.fetch()]
        
        
