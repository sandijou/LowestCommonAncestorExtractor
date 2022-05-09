import json

from src.HierarchyExtractor.Block import Block
from src.HierarchyExtractor.BlockNode import BlockNode



class Section:

    def __init__(self, title, text, subs):
        self.subsections = subs
        self.text = text
        self.title = title

    def getExtraction(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


# Parse hierarchy tree into sections.
# Attributes: tree = node of hierarchy tree
def parseToSections(tree):
    text = ''
    for child in tree.children:
        if isinstance(child, Block):
            text += ('\n' + child.text)

    subs = []
    for child in tree.children:
        if isinstance(child, BlockNode):
            subs.append(parseToSections(child))

    if tree.headline is not None:
        toReturn = Section(tree.headline.text, text[1:], subs)
    else:
        toReturn = Section('', text[1:], subs)
    return toReturn
