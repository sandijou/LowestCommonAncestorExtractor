class DOMNode:
    def __init__(self):
        self.children = []

    # Extract the whole content of all elements in the subtree induced by this DOMNode
    def getWholeContent(self):
        toReturn = []
        for c in self.children:
            if isinstance(c, TreeElement):
                toReturn.append(c.getWholeContent())
            elif isinstance(c, TextElement):
                toReturn.append(c.text)
        return '\n'.join(toReturn)


# TreeElement used as a container to structure DOM-tree.
# TreeElements contain style information aplicaple to all direct children TextElements.
class TreeElement(DOMNode):
    def __init__(self):
        DOMNode.__init__(self)
        self.tag = ''
        self.attributes = dict()
        self.style = ''
        self.xpath = ''


# TextElement holds text sequences as direct child of TreeElement.
# TextElements do _not_ hold any children!
class TextElement(DOMNode):
    def __init__(self, text):
        DOMNode.__init__(self)
        self.text = text



