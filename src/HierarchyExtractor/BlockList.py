from enum import Enum

from src.DOMParser.DOMNode import TextElement, TreeElement
from src.HierarchyExtractor.Block import Block, EnumerationType

class Type(Enum):
    split = 0
    listStart = 1
    listEnd = 2


class BlockList:
    def __init__(self, mainContent):
        tfList = getTFList(mainContent)
        self.list = formListFromTF(tfList)


class TextFraction:
    def __init__(self, text, style, tag):
        self.text = text
        self.style = style
        self.tag = tag


def formListFromTF(tfList):
    splitList = []
    counter = [0]
    for i in range(0, len(tfList)):
        if tfList[i] == Type.split:
            splitList.append(i)
    blockList = []
    for i in range(0, len(splitList) - 1):
        blockList.append(formBlockTF(tfList[ splitList[i] + 1 : splitList[i+1] ], counter))

    return list(filter(lambda x: not x is None, blockList))


def formBlockTF(tfList, counter):
    styles = dict()
    totalText = ''
    if len(tfList) > 0 and tfList[0] == Type.listStart and tfList[len(tfList) - 1] == Type.listEnd:
        toReturn = formBlockTF(tfList[1:len(tfList) - 1], counter)
        toReturn.numeration = [(counter[0], EnumerationType.List)]
        counter[0] += 1
        return toReturn

    for entry in tfList:
        if isinstance(entry, TextFraction):
            if (str(entry.tag) + '$') != 'a$':
                if entry.style in styles.keys():
                    styles[entry.style] += len(entry.text)
                else:
                    styles[entry.style] = len(entry.text)
            elif (str(entry.tag) + '$') == 'a$':
                if entry.style not in styles.keys():
                    styles[entry.style] = 0

            totalText += (' ' + entry.text)

    if len(totalText) > 2:
        mcs = max(styles, key=styles.get)
        return Block(totalText[1:], mcs)
    else:
        return None



# Generate a list of TextFractions by traversing the tree (depth-first) and safe every content
# string to the TF list.
# Attributes: mainContent = root node of main content
def getTFList(mainContent):
    toFill = []
    toFill.append(Type.split)
    getTFListRec(mainContent, toFill)
    toFill.append(Type.split)
    return toFill



# Generate a list of TextFractions by traversing the tree (depth-first) and safe every content
# string to the TF list (REC).
# Attributes: node = node to be processed; toFill = list of TextFractions
def getTFListRec(node, toFill):
    if (str(node.tag) + '$') in getParagraphFormingTags():
        toFill.append(Type.split)

        for child in node.children:
            if isinstance(child, TextElement):
                toFill.append(TextFraction(child.text, node.style, node.tag))
            elif isinstance(child, TreeElement):
                if (str(child.tag) + '$') == 'li$':
                    toFill.append(Type.split)
                    toFill.append(Type.listStart)
                    getTFListRec(child, toFill)
                    toFill.append(Type.listEnd)
                    toFill.append(Type.split)
                else:
                    getTFListRec(child, toFill)
        toFill.append(Type.split)
    elif (str(node.tag) + '$') == 'br$':
        toFill.append(Type.split)
    else:
        for child in node.children:
            if isinstance(child, TextElement):
                toFill.append(TextFraction(child.text, node.style, node.tag))
            elif isinstance(child, TreeElement):
                getTFListRec(child, toFill)



# Return list of all tags + '$' rendered as a paragraph in HTML documents.
# These tags trigger a 'split' during the formation of a TF list.
def getParagraphFormingTags():
    return ['article$', 'section$', 'nav$', 'aside$', 'h1$', 'h2$', 'h3$', 'h4$', 'h5$', 'h6$', 'hgroup$', 'header$',
        'footer$', 'address$', 'p$', 'pre$', 'blockquote$', 'ol$', 'ul$', 'menu$', 'li$', 'dl$', 'dt$', 'dt$', 'dd$',
        'figure$', 'figcaption$', 'main$', 'div$', 'summary$', 'td$', 'th$', 'caption$', 'legend$', 'form$',
        'fieldset$', 'details$']

'''
# modified for OLD Cases files: (not properly tested yet)
['article$', 'section$', 'nav$', 'aside$', 'h1$', 'h2$', 'h3$', 'h4$', 'h5$', 'h6$', 'hgroup$',
            'header$', 'footer$', 'address$', 'p$', 'pre$', 'blockquote$', 'ol$', 'ul$', 'menu$', 'li$', 'dl$',
            'dt$', 'dd$', 'figure$', 'figcaption$', 'main$', 'div$', 'summary$', 'td$', 'th$', 'caption$', 'legend$',
            'form$', 'fieldset$', 'details$', 'span$', 'a$', 'hr$', 'b$', 'u$', 'strong$', 'table$',
            'tr$', 'tbody$', 'col$', 'i$', 'em$']
'''

