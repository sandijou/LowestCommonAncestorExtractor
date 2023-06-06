from src.DOMParser.Font import Font
from src.HierarchyExtractor.BlockList import BlockList
from src.HierarchyExtractor.BlockNode import BlockNode


# Visual-based hierarchy extraction.
# Attributes: mainContent = main content dom node; defaultStyle = MCS not regarded as a possible headline
def extractHierarchyVisually(mainContent, defaultStyle):
    blockList = BlockList(mainContent)
    #printBlockList(blockList)
    hierarchyTree = separateBlocks(blockList, defaultStyle)
    return hierarchyTree



# Print a list of blocks and its associated information (DEBUGGING).
# Attributes: blockList = list of blocks
def printBlockList(blockList):
    for entry in blockList.list:
        print(str(entry.style) + '\t' + str(entry.numeration) + '\t' + entry.text)



# Separate blocks using a visual-based hierarchy extraction.
# Attributes: blockList = list of blocks; defaultStyle = MCS
def separateBlocks(blockList, defaultStyle):
    toReturn = BlockNode()
    toReturn.children = separateBlocksRec(blockList.list, defaultStyle)
    return toReturn



# Separate blocks using a visual-based hierarchy extraction (REC).
# Attributes: blockList = list of blocks; defaultStyle = MCS
def separateBlocksRec(nodeList, defaultStyle):

    # find next headline style
    headlineStyle = findNextHeadlineStyle(nodeList, defaultStyle)
    if headlineStyle is None:
        # create list of all noneStyleHeadLine occurrences
        for i in range(0, len(nodeList)):
            #print(f'\n NoneStyle Nodelist entry at index [i] attribute Text: {nodeList[i].text}\n')
            # new if condition to try fallback solution of regex headline matching including spaced-out words
            if is_valid_headline(nodeList[i].text):
                headLineList.append(i)
                #print(f"valid_headline (Nonestyle): {repr(nodeList[i].text)}\n")
        if headLineList == []:
            return nodeList

    else:
        headLineList = []
        # create list of all headline style occurrences
        for i in range(0, len(nodeList)):
             #print(f'\n Nodelist instance at index [i] attribute Text: {nodeList[i].text}\n')
            if nodeList[i].style == headlineStyle:
                headLineList.append(i)
            # new else if condition to try fallback solution of regex headline matching including spaced-out words
            if is_valid_headline(nodeList[i].text):
                headLineList.append(i)
                #print(f"valid headline with headlineStyle: {headlineStyle}: \n{repr(nodeList[i].text)}\n")
        
    # save all blocks before the headline as content to the current node
    childListToReturn = []
    if headLineList != []:
        childListToReturn = nodeList[0:headLineList[0]]

    # split the block list according to headline style occurrences and recursively process the
    # content in between headlines
    for i in range(0, len(headLineList)):
        toAppend = BlockNode()
        toAppend.headline = nodeList[headLineList[i]]
        if i == len(headLineList) - 1:
            toAppend.children = separateBlocksRec(nodeList[(headLineList[i] + 1):len(nodeList)], defaultStyle)
        else:
            toAppend.children = separateBlocksRec(nodeList[(headLineList[i] + 1):headLineList[i+1]], defaultStyle)
        childListToReturn.append(toAppend)

    return childListToReturn



# Determines whether a style is more prominent than the MCS.
# Attributes: style = currently investigated style; defaultStyle = MCS
def isMoreProminent(style, defaultStyle):
    if style.isUnderlined or style.weight > defaultStyle.weight:
        return True
    else:
        return style.fontSize > defaultStyle.fontSize



# Searches for the next headline style.
# Attributes: list = block list; defaultStyle = MCS
def findNextHeadlineStyle(list, defaultStyle):
    for elem in list:
        if (elem.style != defaultStyle and elem.style != Font(1, 300, False, 'undefined')) \
                and (len(elem.text.split())) <= 10 and isMoreProminent(elem.style, defaultStyle):
            return elem.style
    return None







