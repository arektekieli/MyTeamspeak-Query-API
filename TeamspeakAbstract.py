import re

class TeamspeakAbstract():
    def __init__(self):
        self.lastErrorId = -1
        self.lastErrorMsg = 'No error has been already set'

    def setError(self, txt):
        # Sets last error Id and last error message
        txt = re.findall('error id=[0-9]{1,5} msg=.{1,999999}\n\r', txt)
        if len(txt) == 0:
            return False
        
        arr = txt[0].split(' ')
        self.lastErrorId = int(arr[1].split('=')[1])
        self.lastErrorMsg = self.decode(arr[2].split('=')[1].strip())
    
    def decode(self, txt):
        # Decoding teamspeak format espace characters
        txt = txt.replace("{}{}".format(chr(92), chr(92)), chr(92))
        txt = txt.replace("{}/".format(chr(92)), chr(47))
        txt = txt.replace("{}s".format(chr(92)), chr(32))
        txt = txt.replace("{}p".format(chr(92)), chr(124))
        txt = txt.replace("{}a".format(chr(92)), chr(7))
        txt = txt.replace("{}b".format(chr(92)), chr(8))
        txt = txt.replace("{}f".format(chr(92)), chr(12))
        txt = txt.replace("{}n".format(chr(92)), chr(10))
        txt = txt.replace("{}r".format(chr(92)), chr(13))
        txt = txt.replace("{}t".format(chr(92)), chr(9))
        txt = txt.replace("{}v".format(chr(92)), chr(11))
        return txt

    def encode(self, txt):
        # Encoding teamspeak format espace characters
        txt = txt.replace(chr(92), "{}{}".format(chr(92), chr(92)))
        txt = txt.replace(chr(47), "{}/".format(chr(92)))
        txt = txt.replace(chr(32), "{}s".format(chr(92)))
        txt = txt.replace(chr(124), "{}p".format(chr(92)))
        txt = txt.replace(chr(7), "{}a".format(chr(92)))
        txt = txt.replace(chr(8), "{}b".format(chr(92)))
        txt = txt.replace(chr(12), "{}f".format(chr(92)))
        txt = txt.replace(chr(10), "{}n".format(chr(92)))
        txt = txt.replace(chr(13), "{}r".format(chr(92)))
        txt = txt.replace(chr(9), "{}t".format(chr(92)))
        txt = txt.replace(chr(11), "{}v".format(chr(92)))
        return txt

    def updateAttributes(self, resultItem):
        for attr in self.attributes:
            if hasattr(resultItem, attr):
                setattr(self, attr, getattr(resultItem, attr))

    

    