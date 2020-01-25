from TeamspeakAbstract import TeamspeakAbstract
from TeamspeakResultItem import TeamspeakResultItem

class TeamspeakResult(TeamspeakAbstract):
    def __init__(self, txt):
        super().__init__()
        self.txt = txt
        self.items = []
        self.parse()

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.items):
            raise StopIteration
        response = self.items[self.i]
        self.i += 1
        return response

    def parse(self):
        # Converts server response format to TeamspeakResult class
        data = self.txt.split('\n\r')[0]
        self.items = []
        for el in data.split('|'):
            attributes = []
            for attr in el.split(' '):
                a = attr.split('=', 1)
                if len(a) > 1:
                    attributes.append({a[0]: self.decode(a[1])})
                else:
                    attributes.append({a[0]: None})
            self.items.append(TeamspeakResultItem(attributes))
        self.setError(self.txt)

    def fetchAll(self):
        return self.items

    def toList(self):
        return self.fetchAll()