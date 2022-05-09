from src.HierarchyExtractor.Block import Block


class BlockNode:
    def __init__(self):
        self.children = []
        self.headline = None

    def getWholeContent(self):
        text = ''
        if self.headline is not None:
            text += self.headline.text
        for child in self.children:
            text += child.getWholeContent()

        return text


def printTree(node, depth):
    indent = ' '
    inFurther = '>'
    for i in range(0, depth):
        indent += inFurther
    indent += ' '


    if isinstance(node, BlockNode):
        print(indent + str(node.headline))
        for elem in node.children:
            printTree(elem, depth + 1)
    elif isinstance(node, Block):
        print(indent + '\t' + node.text)
