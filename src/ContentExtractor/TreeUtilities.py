from src.ContentExtractor.ContentExtractorTypes import ContentExtractor
from src.DOMParser.DOMNode import TextElement, TreeElement
from src.ContentExtractor.ContentExtractor import *



# Calculate the depth of the subtree expanded by the given 'node'.
# Attributes: node = node, of which subtree is investigated
def getDepth(node):
    if node.children == []:
        return 0
    else:
        depths = []
        for child in node.children:
            depths.append(getDepth(child))
        return 1 if len(depths) == 0 else 1 + max(depths)



# Calculate the frequency (number of characters) of different styles in the node.
# Attributes: node = node, of which subtree is investigated; contentExtractor = content extraction method
def getFrequencyOfStyles(node, contentExtractor):
    classes = dict()
    if isinstance(node, TreeElement):
        style = getStyle(node, contentExtractor)
        noC = numberOfCharacters(node, contentExtractor)
        classes[style] = noC
    getStylesRec(classes, node, contentExtractor)
    return classes



# Recursive counterpart to getLowestCommonAncestorNodeOfStyle
# Attributes: classes = collector dictionary; node = investigated node in this recursion step;
# contentExtractor = content extraction method
def getStylesRec(classes, node, contentExtractor):
    for child in node.children:
        style = getStyle(child, node, contentExtractor)
        print(style + '\t' + str(c.text))
        if style in classes.keys():
            classes[style] = classes[style] + numberOfCharacters(child, contentExtractor)
        else:
            classes[style] = numberOfCharacters(child, contentExtractor)
        getStylesRec(classes, child, contentExtractor)
    return classes



# Find lowest common ancestor of a given style covering at least 'threshold' (%) of all occurrences of the
# given style ('noOfCharacters') in the document (i.e. in tree expanded by 'rootNode').
# Whenever there is no such node, extract a maximum subsequence of direct children to the body containing the 'style'.
# Attributes: rootNode = root node of whole content tree; style = most common style; noOfCharacters = number of total
# (valid) characters for the style; threshold = minimum coverage for main content node; contentExtractor = content
# extraction method
def getLowestCommonAncestorNodeOfStyle(rootNode, style, noOfCharacters, threshhold, contentExtractor):
    resultList = []
    getLowestCommonAncestorNodeOfStyleRec(rootNode, style, noOfCharacters, 1, resultList, contentExtractor)
    maxDepth = getDepth(rootNode)
    # find common ancestor
    for currentDepth in range(maxDepth, 0, -1):
        for result in resultList:
            if result[2] == currentDepth and result[1] > threshhold:
                return result[0]

    # find maximum subsequence if no common ancestor
    # TODO largest relevant character subsequence??? TODODODODOD
    bitmap = []
    for child in rootNode.children:
        styleDict = getFrequencyOfStyles(child, contentExtractor)
        bitmap.append(True) if style in styleDict.keys() else bitmap.append(False)
    maxSubSeq = findMaximumSubsequenceOfTrue(bitmap)
    returnList = []
    for index in maxSubSeq:
        returnList.append(rootNode.children[index])
    toReturn = TreeElement()
    toReturn.children = returnList
    toReturn.tag = 'body'
    toReturn.xpath = '/html/body'
    return toReturn



# Recursive counterpart to getLowestCommonAncestorNodeOfStyle
# Attributes: node = node investigated in this recursion step; style = most common style; noOfCharacters = number of
# total (valid) characters for the style; depth = current depth in subtree expanded by root; resultList = collector
# list; contentExtractor = content extraction method
def getLowestCommonAncestorNodeOfStyleRec(node, style, noOfCharacters, depth, resultList, contentExtractor):
    for child in node.children:
        styleDict = getFrequencyOfStyles(child, contentExtractor)
        if style in styleDict.keys():
            coverage = float(float(styleDict[style])/float(noOfCharacters))
            resultList.append((child, coverage, depth))
            #if coverage > 0.51:
                #print(str(child.xpath) + '\t' + str(coverage))
            getLowestCommonAncestorNodeOfStyleRec(child, style, noOfCharacters, depth+1, resultList, contentExtractor)



# Calculate the number of (valid, according to used content extractor) characters in a node.
# Attributes: node = node investigated; contentExtractor = content extraction method
def numberOfCharacters(node, contentExtractor):
    sum = 0
    if contentExtractor == ContentExtractor.RenderedStyle or contentExtractor == ContentExtractor.NaiveStyle:
        for child in node.children:
            if isinstance(child, TextElement) and child.text is not None:
                sum = sum + len(child.text)
    elif contentExtractor == ContentExtractor.NaiveStyleAndShortTextExclusion or ContentExtractor.RenderedStyleAndShortTextExclusion:
        for child in node.children:
            if isinstance(child, TextElement) and child.text is not None and len(child.text.split()) > 3:
                sum = sum + len(child.text)
    return sum



# Extract style of node according to chosen method.
# Attributes: node = node investigated; parent = parent of 'node'; contentExtractor = content extraction method
def getStyle(node, parent, contentExtractor):
    if contentExtractor == ContentExtractor.NaiveStyle or contentExtractor == ContentExtractor.NaiveStyleAndShortTextExclusion:
        if isinstance(node, TextElement):
            return str(parent.tag) + '$' + str(parent.attributes)
        else:
            return str(node.tag) + '$' + str(node.attributes)
    elif contentExtractor == ContentExtractor.RenderedStyle or contentExtractor == ContentExtractor.RenderedStyleAndShortTextExclusion:
        if isinstance(node, TextElement):
            return parent.style
        else:
            return node.style
    else:
        return None



# Return list of all tags + '$' not rendered in HTML documents.
# These tags do not have to be included in the process of parsing.
def getListOfUnrederedTags():
    return ['noframes$', 'audio$', 'canvas$', 'script$', 'noscript$', 'datalist$', 'embed$', 'meter$', 'progress$',
            'template$', 'video$', 'wbr$', 'area$', 'col$', 'iframe$', 'img$', 'input$', 'link$', 'meta$',
            'optgroup$', 'option$', 'param$', 'select$', 'style$', 'applet$', 'title$', 'body$', 'head$', 'center$',
            'frame$', 'frameset$', 'svg$']



# Search for the range with the maximum subsequence of 'True' in a bitmap.
# Attributes: list = bitmap to be investigated
def findMaximumSubsequenceOfTrue(list):
    currentLength = 0;
    currentStart = 0;
    currentBest = range(0, 0)
    for i in range(0, len(list)):
        if list[i]:
            currentLength += 1
            if(len(currentBest) < currentLength):
                currentBest = range(currentStart, currentStart + currentLength)
        else:
            currentStart = i + 1
            currentLength = 0
    return currentBest



# Determine the number of child nodes.
# Method used for statistical purposes.
# Attributes: node = node = node investigated
def numberOfChildNodes(node):
    sum = 0
    for child in node.children:
        if isinstance(child, TreeElement):
            sum = sum + 1 + numberOfChildNodes(child)
    return sum
