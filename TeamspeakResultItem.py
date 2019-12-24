from TeamspeakAbstract import TeamspeakAbstract

class TeamspeakResultItem(TeamspeakAbstract):
    def __init__(self, args):
        super().__init__()
        for arg in args:
            for key, val in arg.items():
                setattr(self, key, val)
        