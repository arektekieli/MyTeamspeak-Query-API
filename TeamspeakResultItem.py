from TeamspeakAbstract import TeamspeakAbstract

class TeamspeakResultItem(TeamspeakAbstract):
    def __init__(self, attrs):
        super().__init__()
        self.attrs = attrs
        for arg in attrs:
            for key, val in arg.items():
                setattr(self, key, val)

    def toList(self):
        return [attr for attr in self.attrs]

    def toDict(self):
        res = {}
        for attr in self.attrs:
            res.update(attr)
            
        return res
        