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
        self.lastErrorMsg = arr[2].split('=')[1].strip()
    
    def decode(self, txt):
        # Decoding teamspeak format espace characters
        return txt

    def encode(self, txt):
        # Encoding teamspeak format espace characters
        return txt

    def updateAttributes(self, resultItem):
        for attr in self.attributes:
            if hasattr(resultItem, attr):
                setattr(self, attr, getattr(resultItem, attr))

    

    