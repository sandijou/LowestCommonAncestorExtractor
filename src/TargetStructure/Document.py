from src.TargetStructure.Section import Section
import json
import datetime

class Document:

    def __init__(self, title, source):
        now = datetime.datetime.now()
        self.extractionDate = (now.microsecond, now.second, now.minute, now.hour, now.day, now.month, now.year)
        self.source = source
        self.title = title
        self.content = None
        self.id = abs(int(hash(self.extractionDate) ^ hash(self.source)))


    def getExtraction(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)



