from Teamspeak import Teamspeak
from TeamspeakClient import TeamspeakClient
from TeamspeakChannel import TeamspeakChannel

class TeamspeakAPI(Teamspeak):
    def __init__(self, host, port, sid, login, password, nick='ArasBot'):
        super().__init__(host, port, sid, login, password, nick)

    def safeQuery(self, query):
        result = self.query(query)

        if self.lastErrorId != 0:
            return False

        return result

    def switchChannel(self, cid, cpw=''):
        # Switch channel of current teamspeak instance
        return self.clientmove(self.clid, cid, cpw)

    def channelinfo(self, cid):
        # Returns TeamspeakResultItem object
        # channel must be cid or TeamspeakChannel class
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        return self.safeQuery('channelinfo cid={}'.format(cid)).items[0]
    
    def channellist(self):
        # Returns list of TeamspeakClient objects
        result = self.safeQuery('channellist')
        if result == False:
            return False
        
        return [TeamspeakChannel(self, x) for x in result.fetchAll()]

    def clientinfo(self, client):
        # Returns TeamspeakResultItem object
        # client must be clid or TeamspeakClient class
        if isinstance(client, TeamspeakClient):
            client = client.clid
        
        return self.safeQuery('clientinfo clid={}'.format(client)).items[0]

    def clientlist(self):
        # Returns list of TeamspeakClient objects
        result = self.safeQuery('clientlist')
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result.fetchAll()]

    def clientmove(self, clid, cid, cpw=''):
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid

        return self.safeQuery('clientmove clid={} cid={} cpw={}'.format(clid, cid, cpw))
        
    def sendtextmessage(self, msg, targetmode, target=False):
        # Sends message to channel or client
        # targetmode: 1 -> client 2 -> channel 3 -> global message
        if isinstance(target, TeamspeakClient):
            target = target.clid

        return self.safeQuery('sendtextmessage targetmode={} target={} msg={}'.format(targetmode, target, msg))

    def whoami(self):
        return self.safeQuery('whoami').items[0]

    
        
