from TeamspeakAbstract import TeamspeakAbstract

class TeamspeakResultItem(TeamspeakAbstract):
    def __init__(self, args):
        super().__init__()
        tmp = []
        for arg in args:
            for key, val in arg.items():
                tmp.append(key)
                setattr(self, key, val)
        print(tmp)
        