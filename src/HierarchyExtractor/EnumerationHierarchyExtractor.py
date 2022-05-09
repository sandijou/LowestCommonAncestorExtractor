from src.HierarchyExtractor.Block import Block, EnumerationType
from src.HierarchyExtractor.BlockNode import BlockNode



# Façade for different hierarchy extraction approaches based on enumeration patterns.
# Attributes: rootNode = rootNode of the visually separated hierarchy tree
def extractHierarchyNumerically(rootNode):
    separateBlocksNums(rootNode)
    validateBlocksNums(rootNode)
    adjustListNums(rootNode)



# Apply enumeration patterns for lists.
# Attributes: rootNode = rootNode of the visually and hierarchically separated hierarchy tree
def adjustListNums(rootNode):
    if isinstance(rootNode, BlockNode):
        sepList = []
        sepList.append(0)
        for i in range(0, len(rootNode.children)):

            if isinstance(rootNode.children[i], BlockNode):
                adjustListNums(rootNode.children[i])
            else:
                if EnumerationType.List in rootNode.children[i].getNumerationPattern():
                    sepList.append(i)
                elif i - 1 == sepList[len(sepList) - 1] and sepList[len(sepList) - 1] != 0:
                    sepList.append(i)


        if len(sepList) > 1:
            sepList.append(sepList[len(sepList)-1]+1)
            sepList.append(len(rootNode.children))
            newChildren = []
            for i in range(0, len(sepList) - 1):
                toAppend = BlockNode()
                toAppend.headline = Block('', None)
                toAppend.children = rootNode.children[sepList[i]:sepList[i+1]]
                newChildren.append(toAppend)

            rootNode.children = newChildren



# Check the textual content of a block for occuring enumeration patterns.
# Attributes: node = node, which content should be checked
def separateBlocksNums(node):
    relevantBlocks = list(filter(lambda x: isinstance(x, Block), node.children))
    otherBlockNodes = list(filter(lambda x: isinstance(x, BlockNode), node.children))
    headlineStyles = getAllStyles(relevantBlocks)
    for style in headlineStyles:
        isValidNumStyleRes = isValidNumStyle(style, relevantBlocks)
        if isValidNumStyleRes[0]:
            headlineList = []
            for i in range(0, len(relevantBlocks)):
                if isinstance(relevantBlocks[i], Block) and relevantBlocks[i].getNumerationPattern() == style[0]:
                    headlineList.append(i)
            if isValidNumerationPattern(relevantBlocks, headlineList):
                headlineList.append(len(relevantBlocks))

                newChildren = relevantBlocks[0:headlineList[0]]
                for i in range(0, len(headlineList) - 1):
                    toAppend = BlockNode()
                    if isValidNumStyleRes[1]:
                        # no headline
                        toAppend.headline = Block('', None)
                        toAppend.children = relevantBlocks[(headlineList[i]):headlineList[i+1]]
                    else:
                        # with headline
                        toAppend.headline = relevantBlocks[headlineList[i]]
                        toAppend.children = separateBlocksNumsRec(relevantBlocks[(headlineList[i] + 1):headlineList[i+1]])
                    newChildren.append(toAppend)
                newChildren += otherBlockNodes
                node.children = newChildren
                break

    for child in node.children:
        if isinstance(child, BlockNode):
            separateBlocksNums(child)



# Check the textual content of a block for occuring enumeration patterns (REC).
# Attributes: blockList = block list of textual content to be checked
def separateBlocksNumsRec(blockList):
    headlineStyles = getAllStyles(blockList)
    for style in headlineStyles:
        isValidNumStyleRes = isValidNumStyle(style, blockList)
        if isValidNumStyleRes[0]:
            headlineList = []
            for i in range(0, len(blockList)):
                if isinstance(blockList[i], Block) and blockList[i].getNumerationPattern() == style[0]:
                    headlineList.append(i)
            if isValidNumerationPattern(blockList, headlineList):
                headlineList.append(len(blockList))

                newChildren = blockList[0:headlineList[0]]
                for i in range(0, len(headlineList) - 1):
                    toAppend = BlockNode()
                    if isValidNumStyleRes[1]:
                        # no headline
                        toAppend.headline = Block('', None)
                        toAppend.children = blockList[(headlineList[i]):headlineList[i+1]]
                    else:
                        # with headline
                        toAppend.headline = blockList[headlineList[i]]
                        toAppend.children = separateBlocksNumsRec(blockList[(headlineList[i] + 1):headlineList[i+1]])
                    newChildren.append(toAppend)
                return newChildren
    return blockList



# Check if a numeration pattern is occurring at least twice in a list of blocks and if blocks contain a headline.
# Attributes: style = numeration patter; nodeChildren = list of blocks
def isValidNumStyle(style, nodeChildren):
    if EnumerationType.List in style[0]:
        return (False, False)
    if len(list(filter(lambda block: block.getNumerationPattern() == style[0],\
                            list(filter(lambda child: isinstance(child, Block), nodeChildren))))) <= 1:
        return (False, False)

    if len(nodeChildren[style[1]].text.split()) >= 10:
        return (True, True)
    elif style[1] == len(list(filter(lambda child: isinstance(child, Block), nodeChildren))) - 1:
        return (nodeChildren[style[1]].getNumerationPattern() != nodeChildren[style[1] - 1].getNumerationPattern(), False)
    else:
        return (nodeChildren[style[1]].getNumerationPattern() != nodeChildren[style[1] + 1].getNumerationPattern(), False)



# Gather all enumeration patterns whithin a list of blocks.
# Attributes: nodeChildren = list of blocks
def getAllStyles(nodeChildren):
    toReturn = []
    for i in range(0, len(nodeChildren)):
        if isinstance(nodeChildren[i], Block) and len(nodeChildren[i].numeration) >= 1:
            toReturn.append((nodeChildren[i].getNumerationPattern(), i))
    return toReturn



# Check if a numeration pattern is valid in a list of blocks.
# Attributes: nodeList = list of blocks; headlineList = indexes of all occurring headlines
def isValidNumerationPattern(nodeList, headlineList):
    if len(headlineList) >= 10:
        return True
    for i in range(1, len(headlineList)):
        if isinstance(nodeList[headlineList[i]], Block):
            if not isValidStep(nodeList[headlineList[i-1]].numeration, nodeList[headlineList[i]].numeration):
                return False
        else:
            if not isValidStep(nodeList[headlineList[i-1]].headline.numeration, nodeList[headlineList[i]].headline.numeration):
                return False
    return True



# Check if a step within a numeration pattern is valid.
# Attributes: num1 = first numeration pattern; num2 = second numeration pattern
def isValidStep(num1, num2):
    sumNumbers1 = sum(list(map(lambda x: x[0], num1)))
    sumNumbers2 = sum(list(map(lambda x: x[0], num2)))
    return sumNumbers2 - sumNumbers1 <= 2 and sumNumbers2 - sumNumbers1 >= 1



# Check all headlines for existing enumeration patterns (including those detected visually-based).
# Attributes: node = node, which headline should be checked
def validateBlocksNums(node):
    headlineStyles = list(map(lambda y: list(map(lambda x: x[1], y.headline.numeration)), list(filter(lambda x: isinstance(x, BlockNode) and (not x.headline is None), node.children))))
    for headlineStyle in headlineStyles:
        headlineList = []
        for i in range(0, len(node.children)):
            if isinstance(node.children[i], BlockNode) and \
                    list(map(lambda x: x[1], node.children[i].headline.numeration)) == headlineStyle:
                headlineList.append(i)

        if isValidNumerationPattern(node.children, headlineList) and \
                len(headlineList) >= 2 and len(list(filter(lambda x: isinstance(x, BlockNode), node.children))) != len(headlineList):
            newChildren = node.children[0:headlineList[0]]
            for i in range(0, len(headlineList)):
                toAppend = BlockNode()
                toAppend.headline = node.children[headlineList[i]].headline
                toAppend.children = node.children[headlineList[i]].children
                if i == len(headlineList) - 1:
                    toAppend.children += node.children[(headlineList[i] + 1):len(node.children)]
                else:
                    toAppend.children += node.children[(headlineList[i] + 1):headlineList[i+1]]

                newChildren.append(toAppend)

            node.children = newChildren
            break


    for child in node.children:
            if isinstance(child, BlockNode):
                validateBlocksNums(child)




