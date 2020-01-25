from Teamspeak import Teamspeak
from TeamspeakClient import TeamspeakClient
from TeamspeakChannel import TeamspeakChannel

class TeamspeakAPI(Teamspeak):
    def __init__(self, host, port, username, password, nick='ArasBot'):
        super().__init__(host, port, username, password, nick)

    def safeQuery(self, query, fetchOne = False):
        result = self.query(query)

        if self.lastErrorId != 0:
            return False
        
        if fetchOne == True:
            try:
                return result.fetchAll()[0]
            except:
                return False
        
        return result

    def makeParams(self, kwargs):
        response = []
        for arg in kwargs:
            if kwargs[arg] == True and type(kwargs[arg]) is bool:
                response.append(self.encode('-{}'.format(arg)))
            elif type(kwargs[arg]) is list:
                response.append('|'.join(['{}={}'.format(self.encode(arg), self.encode(str(x))) for x in kwargs[arg]]))
            else:
                response.append(self.encode('{}={}'.format(arg, kwargs[arg])))
         
        return ' '.join(response)

    def switchChannel(self, cid, cpw=''):
        # TODO
        pass

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

    def clientedit(self, clid, **kwargs):
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid

        kwargs.update({'clid': clid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientedit {}'.format(params), True)
    
    def clientinfo(self, clid):
        # Returns TeamspeakResultItem object
        # client must be clid or TeamspeakClient class
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid
        
        return self.safeQuery('clientinfo clid={}'.format(clid)).items[0]

    def clientlist(self):
        # Returns list of TeamspeakClient objects
        result = self.safeQuery('clientlist')
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result.fetchAll()]

    def clientmove(self, clid, cid, **kwargs):
        if type(clid) is not list:
            clid = [clid]

        clid = [c.clid if isinstance(c, TeamspeakClient) else c for c in clid]
    
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        kwargs.update({'clid': clid})
        kwargs.update({'cid': cid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientmove {}'.format(params), True)

    def help(self, param):
        return self.safeQuery('help {}'.format(param), True)

    def hostinfo(self):
        return self.safeQuery('hostinfo', True)

    def instanceinfo(self):
        return self.safeQuery('instanceinfo', True)

    def login(self, username, password=''):
        return self.safeQuery('login {} {}'.format(username, password), True)

    def logout(self):
        return self.safeQuery('logout', True)

    def logview(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('logview {}'.format(params))

    def quit(self):
        return self.safeQuery('quit', True)
        
    def sendtextmessage(self, msg, targetmode, target=False):
        # Sends message to channel or client
        # targetmode: 1 -> client 2 -> channel 3 -> global message
        if isinstance(target, TeamspeakClient):
            target = target.clid

        return self.safeQuery('sendtextmessage targetmode={} target={} msg={}'.format(targetmode, target, msg))

    def use(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('use {}'.format(params), True)
    
    def version(self):
        return self.safeQuery('version', True)
    
    def whoami(self):
        return self.safeQuery('whoami', True)


    

    
        
