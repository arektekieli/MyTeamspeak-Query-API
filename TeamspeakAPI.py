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
            key = arg.lower()
            if kwargs[arg] == True and type(kwargs[arg]) is bool:
                response.append(self.encode('-{}'.format(key)))
            elif type(kwargs[arg]) is list:
                if type(kwargs[arg][0]) is dict:
                    response.append('|'.join([self.makeParams(x) for x in kwargs[arg]]))
                else:
                    response.append('|'.join(['{}={}'.format(self.encode(key), self.encode(str(x))) for x in kwargs[arg]]))
            else:
                response.append(self.encode('{}={}'.format(key, kwargs[arg])))
         
        return ' '.join(response)

    def bindinglist(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('bindinglist {}'.format(params))
    
    def channeladdperm(self, cid, permissions):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'cid': cid, 'permissions': permissions})
        return self.safeQuery('channeladdperm {}'.format(params), True)
    
    def channelclientaddperm(self, cid, cldbid, permissions):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'cid': cid, 'cldbid': cldbid, 'permissions': permissions})
        return self.safeQuery('channelclientaddperm {}'.format(params), True)
    
    def channelclientdelperm(self, cid, cldbid, **kwargs):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'cid': cid})
        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelclientdelperm {}'.format(params), True)
    
    def channelclientpermlist(self, cid, cldbid, **kwargs):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        kwargs.update({'cid': cid})
        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelclientpermlist {}'.format(params))
    
    def channelcreate(self, channel_name, **kwargs):
        # flags must be integers not booleans
        kwargs.update({'channel_name': channel_name})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelcreate {}'.format(params), True)

    def channeldelete(self, cid, force=0):
        # flags must be integers not booleans
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        params = self.makeParams({'cid': cid, 'force': force})
        return self.safeQuery('channeldelete {}'.format(params), True)

    def channeldelperm(self, cid, **kwargs):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'cid': cid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channeldelperm {}'.format(params), True)
    
    def channeledit(self, cid, **kwargs):
        # flags must be integers not booleans
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        kwargs.update({'cid': cid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channeledit {}'.format(params), True)
    
    def channelfind(self, pattern):
        params = self.makeParams({'pattern': pattern})
        result = self.safeQuery('channelfind {}'.format(params))
        if result == False:
            return False

        return [TeamspeakChannel(self, x) for x in result]

    def channelgroupadd(self, name, **kwargs):
        kwargs.update({'name': name})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelgroupadd {}'.format(params), True)

    def channelgroupaddperm(self, cgid, permissions):
        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'cgid': cgid, 'permissions': permissions})
        return self.safeQuery('channelgroupaddperm {}'.format(params), True)

    def channelgroupclientlist(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('channelgroupclientlist {}'.format(params))
    
    def channelgroupcopy(self, scgid, tsgid, name='', _type=1):
        params = self.makeParams({'scgid': scgid, 'tsgid': tsgid, 'name': name, 'type': _type})
        return self.safeQuery('channelgroupcopy', True)

    def channelgroupdel(self, cgid, force=0):
        params = self.makeParams({'cgid': cgid, 'force': force})
        return self.safeQuery('channelgroupdel {}'.format(params), True)

    def channelgroupdelperm(self, cgid, **kwargs):
        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'cgid': cgid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelgroupdelperm {}'.format(params), True)
    
    def channelgrouplist(self):
        return self.safeQuery('channelgrouplist')

    def channelgrouppermlist(self, cgid, **kwargs):
        kwargs.update({'cgid': cgid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelgrouppermlist {}'.format(params))
    
    def channelgrouprename(self, cgid, name):
        params = self.makeParams({'cgid': cgid, 'name': name})
        return self.safeQuery('channelgrouprename {}'.format(params), True)

    def channelinfo(self, cid):
        # Returns TeamspeakResultItem object
        # channel must be cid or TeamspeakChannel class
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        params = self.makeParams({'cid': cid})
        return self.safeQuery('channelinfo {}'.format(params), True)
    
    def channellist(self):
        # Returns list of TeamspeakClient objects
        result = self.safeQuery('channellist')
        if result == False:
            return False
        
        return [TeamspeakChannel(self, x) for x in result]

    def channelpermlist(self, cid, **kwargs):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid
        
        kwargs.update({'cid': cid})
        params = self.makeParams(kwargs)
        return self.safeQuery('channelpermlist {}'.format(params))

    def clientaddperm(self, cldbid, permissions):
        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'cldbid': cldbid, 'permissions': permissions})
        return self.safeQuery('clientaddperm {}'.format(params), True)
    
    def clientdbdelete(self, cldbid):
        params = self.makeParams({'cldbid': cldbid})
        return self.safeQuery('clientdbdelete {}'.format(params), True)

    def clientdbedit(self, cldbid, **kwargs):
        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientdbedit {}'.format(params), True)
    
    def clientdbfind(self, pattern, **kwargs):
        kwargs.update({'pattern': pattern})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientdbfind {}'.format(params))

    def clientdbinfo(self, cldbid):
        params = self.makeParams({'cldbid': cldbid})
        result = self.safeQuery('clientdbinfo {}'.format(params))
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result]
    
    def clientdblist(self, **kwargs):
        params = self.makeParams(kwargs)
        result = self.safeQuery('clientdblist {}'.format(params))
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result]
    
    def clientdelperm(self, cldbid, **kwargs):
        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientdelperm {}'.format(params), True)
    
    def clientedit(self, clid, **kwargs):
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid

        kwargs.update({'clid': clid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientedit {}'.format(params), True)
    
    def clientfind(self, pattern):
        params = self.makeParams({'pattern': pattern})
        result = self.safeQuery('clientfind {}'.format(params))
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result]
    
    def clientgetdbidfromuid(self, cluid):
        params = self.makeParams({'cluid': cluid})
        return self.safeQuery('clientgetdbidfromuid {}'.format(params))

    def clientgetids(self, cluid):
        params = self.makeParams({'cluid': cluid})
        result = self.safeQuery('clientgetids {}'.format(params))
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result]

    def clientgetnamefromdbid(self, cldbid):
        params = self.makeParams({'cldbid': cldbid})
        return self.safeQuery('clientgetnamefromdbid {}'.format(params))
    
    def clientgetnamefromuid(self, cluid):
        params = self.makeParams({'cluid': cluid})
        return self.safeQuery('clientgetnamefromuid {}'.format(params))

    def clientgetuidfromclid(self, clid):
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid

        params = self.makeParams({'clid': clid})
        return self.safeQuery('clientgetuidfromclid {}'.format(params))
    
    def clientinfo(self, clid):
        # Returns TeamspeakResultItem object
        # client must be clid or TeamspeakClient class
        if isinstance(clid, TeamspeakClient):
            clid = clid.clid
        
        params = self.makeParams({'clid': clid})
        return self.safeQuery('clientinfo {}'.format(params), True)

    def clientkick(self, clid, reasonid, **kwargs):
        # Works only on sigle client
        if type(clid) is not list:
            clid = [clid]

        clid = [c.clid if isinstance(c, TeamspeakClient) else c for c in clid]
        
        kwargs.update({'clid': clid})
        kwargs.update({'reasonid': reasonid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientkick {}'.format(params), True)
    
    def clientlist(self, **kwargs):
        # Returns list of TeamspeakClient objects
        params = self.makeParams(kwargs)
        result = self.safeQuery('clientlist {}'.format(params))
        if result == False:
            return False
        
        return [TeamspeakClient(self, x) for x in result]

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

    def clientpermlist(self, cldbid, **kwargs):
        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('clientpermlist {}'.format(params))
    
    def clientpoke(self, clid, msg):
        if type(clid) is not list:
            clid = [clid]

        clid = [c.clid if isinstance(c, TeamspeakClient) else c for c in clid]
        
        params = self.makeParams({'msg': msg, 'clid': clid})
        return self.safeQuery('clientpoke {}'.format(params), True)

    def clientsetserverquerylogin(self, client_login_name):
        params = self.makeParams({'client_login_name': client_login_name})
        return self.safeQuery('clientsetserverquerylogin {}'.format(params), True)

    def clientupdate(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('clientupdate {}'.format(params), True)

    def gm(self, msg):
        params = self.makeParams({'msg': msg})
        return self.safeQuery('gm {}'.format(params), True)
    
    def help(self, param):
        return self.safeQuery('help {}'.format(self.encode(param)), True)

    def hostinfo(self):
        return self.safeQuery('hostinfo', True)

    def instanceedit(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('instanceedit {}'.format(params), True)
    
    def instanceinfo(self):
        return self.safeQuery('instanceinfo', True)

    def logadd(self, loglevel, logmsg):
        params = self.makeParams({'loglevel': loglevel, 'logmsg': logmsg})
        return self.safeQuery('logadd {}'.format(params), True)
    
    def login(self, username, password=''):
        return self.safeQuery('login {} {}'.format(self.encode(username), self.encode(password)), True)

    def logout(self):
        return self.safeQuery('logout', True)

    def logview(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('logview {}'.format(params))

    def permget(self, **kwargs):
        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        params = self.makeParams(kwargs)
        return self.safeQuery('permget {}'.format(params))
    
    def permidgetbyname(self, permsid):
        if type(permsid) is not list:
            permsid = [permsid]

        params = self.makeParams({'permsid': permsid})
        return self.safeQuery('permidgetbyname {}'.format(params))
    
    def permissionlist(self):
        return self.safeQuery('permissionlist')

    def permoverview(self, cid, cldbid, **kwargs):
        if isinstance(cid, TeamspeakChannel):
            cid = cid.cid

        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'cid': cid})
        kwargs.update({'cldbid': cldbid})
        params = self.makeParams(kwargs)
        return self.safeQuery('permoverview {}'.format(params))
    
    def quit(self):
        return self.safeQuery('quit', True)
        
    def sendtextmessage(self, targetmode, target, msg):
        if isinstance(target, TeamspeakClient):
            target = target.clid

        params = self.makeParams({'targetmode': targetmode, 'target': target, 'msg': msg})
        return self.safeQuery('sendtextmessage {}'.format(params), True)

    def servercreate(self, virtualserver_name, **kwargs):
        kwargs.update({'virtualserver_name': virtualserver_name})
        params = self.makeParams(kwargs)
        return self.safeQuery('servercreate {}'.format(params), True)

    def serverdelete(self, sid):
        params = self.makeParams({'sid': sid})
        return self.safeQuery('serverdelete {}'.format(params), True)
    
    def serveredit(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('serveredit {}'.format(params))
    
    def servergroupadd(self, name, **kwargs):
        kwargs.update({'name': name})
        params = self.makeParams(kwargs)
        return self.safeQuery('servergroupadd {}'.format(params))

    def servergroupaddclient(self, sgid, cldbid):
        params = self.makeParams({'sgid': sgid, 'cldbid': cldbid})
        return self.safeQuery('servergroupaddclient {}'.format(params), True)

    def servergroupaddperm(self, sgid, permissions):
        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'sgid': sgid, 'permissions': permissions})
        return self.safeQuery('servergroupaddperm {}'.format(params), True)

    def servergroupautoaddperm(self, sgtype, permissions):
        if type(permissions) is not list:
            raise Exception('Parameter permissions must be list of dicts.')

        for el in permissions:
            if type(el) is not dict:
                raise Exception('Parameter permissions must be list of dicts.')
        
        params = self.makeParams({'sgtype': sgtype, 'permissions': permissions})
        return self.safeQuery('servergroupautoaddperm {}'.format(params), True)

    def servergroupautodelperm(self, sgtype, **kwargs):
        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'sgtype': sgtype})
        params = self.makeParams(kwargs)
        return self.safeQuery('servergroupautodelperm {}'.format(params), True)

    def servergroupclientlist(self, sgid, **kwargs):
        kwargs.update({'sgid': sgid})
        params = self.makeParams(kwargs)
        return self.safeQuery('servergroupclientlist {}'.format(params))
    
    def servergroupcopy(self, ssgid, tsgid, name='', _type=1):
        params = self.makeParams({'ssgid': ssgid, 'tsgid': tsgid, 'name': name, 'type': _type})
        return self.safeQuery('servergroupcopy {}'.format(params), True)

    def servergroupdel(self, sgid, force=0):
        params = self.makeParams({'sgid': sgid, 'force': force})
        return self.safeQuery('servergroupdel {}'.format(params), True)

    def servergroupdelclient(self, sgid, cldbid):
        params = self.makeParams({'sgid': sgid, 'cldbid': cldbid})
        return self.safeQuery('servergroupdelclient {}'.format(params), True)

    def servergroupdelperm(self, sgid, **kwargs):
        if 'permid' in kwargs:
            if type(kwargs['permid']) is not list:
                kwargs['permid'] = [kwargs['permid']]

            kwargs.update({'permid': kwargs['permid']})

        if 'permsid' in kwargs:
            if type(kwargs['permsid']) is not list:
                kwargs['permsid'] = [kwargs['permsid']]

            kwargs.update({'permsid': kwargs['permsid']})

        kwargs.update({'sgid': sgid})
        params = self.makeParams(kwargs)
        return self.safeQuery('servergroupdelperm {}'.format(params), True)

    def servergrouppermlist(self, sgid, **kwargs):
        kwargs.update({'sgid': sgid})
        params = self.makeParams(kwargs)
        return self.safeQuery('servergrouppermlist {}'.format(params))
    
    def servergrouprename(self, sgid, name):
        params = self.makeParams({'sgid': sgid, 'name': name})
        return self.safeQuery('servergrouprename {}'.format(params), True)

    def serveridgetbyport(self, virtualserver_port):
        params = self.makeParams({'virtualserver_port': virtualserver_port})
        return self.safeQuery('serveridgetbyport {}'.format(params))
    
    def servergrouplist(self):
        return self.safeQuery('servergrouplist')

    def servergroupsbyclientid(self, cldbid):
        params = self.makeParams({'cldbid': cldbid})
        return self.safeQuery('servergroupsbyclientid {}'.format(params))

    def serverlist(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('serverlist {}'.format(params))

    def servernotifyregister(self, event, **kwargs):
        kwargs.update({'event': event})
        params = self.makeParams(kwargs)
        return self.safeQuery('servernotifyregister {}'.format(params), True)

    def servernotifyunregister(self):
        return self.safeQuery('servernotifyunregister', True)

    def serverprocessstop(self):
        return self.safeQuery('serverprocessstop', True)

    def serverrequestconnectioninfo(self):
        return self.safeQuery('serverrequestconnectioninfo', True)

    def serversnapshotcreate(self):
        return self.safeQuery('serversnapshotcreate')
    
    def serverstart(self, sid):
        params = self.makeParams({'sid': sid})
        return self.safeQuery('serverstart {}'.format(params), True)

    def serverstop(self, sid):
        params = self.makeParams({'sid': sid})
        return self.safeQuery('serverstop {}'.format(params), True)

    def servertemppasswordadd(self, pw, desc, duration, tcid=0, tcpw=''):
        params = self.makeParams({'pw': pw, 'desc': desc, 'duration': duration, 'tcid': tcid, 'tcpw': tcpw})
        return self.safeQuery('servertemppasswordadd {}'.format(params), True)

    def servertemppassworddel(self, pw):
        params = self.makeParams({'pw': pw})
        return self.safeQuery('servertemppassworddel {}'.format(params), True)

    def servertemppasswordlist(self):
        return self.safeQuery('servertemppasswordlist')

    def setclientchannelgroup(self, cgid, cid, cldbid):
        params = self.makeParams({'cgid': cgid, 'cid': cid, 'cldbid': cldbid})
        return self.safeQuery('setclientchannelgroup {}'.format(params), True)
    
    def tokenadd(self, tokentype, tokenid1, tokenid2, **kwargs):
        kwargs.update({'tokentype': tokentype})
        kwargs.update({'tokenid1': tokenid1})
        kwargs.update({'tokenid2': tokenid2})
        params = self.makeParams(kwargs)
        return self.safeQuery('tokenadd {}'.format(params), True)

    def tokendelete(self, token):
        params = self.makeParams({'token': token})
        return self.safeQuery('tokendelete {}'.format(params), True)

    def tokenlist(self):
        return self.safeQuery('tokenlist')

    def tokenuse(self, token):
        params = self.makeParams({'token': token})
        return self.safeQuery('tokenuse {}'.format(params), True)
    
    def use(self, **kwargs):
        params = self.makeParams(kwargs)
        return self.safeQuery('use {}'.format(params), True)
    
    def version(self):
        return self.safeQuery('version', True)
    
    def whoami(self):
        return self.safeQuery('whoami', True)


    

    
        
