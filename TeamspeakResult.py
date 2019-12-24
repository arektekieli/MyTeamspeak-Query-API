from TeamspeakAbstract import TeamspeakAbstract
from TeamspeakResultItem import TeamspeakResultItem

class TeamspeakResult(TeamspeakAbstract):
    def __init__(self, txt):
        super().__init__()
        self.txt = txt
        self.items = []
        self.parse()

    def parse(self):
        # Converts server response format to TeamspeakResult class
        data = self.txt.split('\n\r')[0]
        self.items = []
        for el in data.split('|'):
            attributes = []
            for attr in el.split(' '):
                a = attr.split('=', 1)
                if len(a) > 1:
                    attributes.append({a[0]: a[1]})
                else:
                    attributes.append({a[0]: None})
            self.items.append(TeamspeakResultItem(attributes))
        self.setError(self.txt)

    def fetch(self):
        for item in self.items:
            yield item