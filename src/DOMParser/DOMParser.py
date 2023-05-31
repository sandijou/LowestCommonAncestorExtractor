from src.DOMParser.Font import Font
from src.DOMParser.DOMNode import TreeElement, TextElement
from io import StringIO
from lxml import etree



# Parse the HTML doc downloaded by Selenium.
# Attributes: driver  = Selenium driver; extractStyle = whether style is rendered in this step
def parseTree(driver, extractStyle):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(driver.page_source), parser)
    root = tree
    body = tree.xpath('/html/body')[0]
    xpath = tree.getpath(body)
    toReturn = TreeElement()
    toReturn.tag = body.tag
    toReturn.xpath = xpath
    if extractStyle:
        toReturn.style = parseStyle(driver, xpath)
    toReturn.children = parseSeleniumTreeRec(driver, root, body.xpath('child::node()'), extractStyle)
    return toReturn



# Recursive counterpart to parseSeleniumTree
# Attributes: driver = Selenium driver; root = root HTML element; currentElem = node investigated in this recursion
# step; extractStyle = whether style is rendered
def parseSeleniumTreeRec(driver, root, currentElem, extractStyle):
    childList = []
    for child in currentElem:
        if isinstance(child, str):
            cutted = cutStrToVisibleContent(child)
            childList.append(TextElement(cutted))
        elif not ('Comment' in str(child.tag)):         #((str(child.tag) + '$') in getListOfUnrederedTags()) and not 
            treeElement = TreeElement()
            xpath = root.getpath(child)
            treeElement.attributes = child.attrib
            treeElement.tag = child.tag
            treeElement.xpath = xpath
            if extractStyle:
                treeElement.style = parseStyle(driver, xpath)
            treeElement.children = parseSeleniumTreeRec(driver, root, child.xpath('child::node()'), extractStyle)
            childList.append(treeElement)
        else:
            None
    return childList


'''
def parseSeleniumTreeRec(driver, root, currentElem, extractStyle):
    childList = []
    for child in currentElem:
        if isinstance(child, str):
            cutted = cutStrToVisibleContent(child)
            childList.append(TextElement(cutted))
        elif not ((str(child.tag) + '$') in getListOfUnrederedTags()) and not ('Comment' in str(child.tag)):
            treeElement = TreeElement()
            xpath = root.getpath(child)
            treeElement.attributes = child.attrib
            treeElement.tag = child.tag
            treeElement.xpath = xpath
            if extractStyle:
                treeElement.style = parseStyle(driver, xpath)
            treeElement.children = parseSeleniumTreeRec(driver, root, child.xpath('child::node()'), extractStyle)
            childList.append(treeElement)
        else:
            None
    return childList
'''


# Parse style of given element.
# Attributes: driver = Selenium driver; xpath = XPath to currently investigated element
def parseStyle(driver, xpath):
    try:
        elem = driver.find_element("xpath",xpath) # Deprecated find_element_by_* and find_elements_by_* are now removed (#10712)
        sizeStr = str(elem.value_of_css_property('font-size'))
        size = float(sizeStr[:(len(sizeStr) - 2)])
        style = Font(\
                size,\
                        int(elem.value_of_css_property('font-weight')),\
                True if 'underline' in str(elem.value_of_css_property('text-decoration')).lower() else False,\
                str(elem.value_of_css_property('font-family'))\
            )
        return style
    except:
        # FALLBACK for failed style extraction
        return Font(16, 400, False, 'Times New Roman') #Font(1, 300, False, 'undefined')



# Cut unimportant characters from text.
# Attributes: text = input string
def cutStrToVisibleContent(text):
    toReturn = []
    for c in text:
        if ord(c) == 10 or ord(c) >= 32:
            toReturn.append(c)
    empty = ""
    return cutStartAndEndWhitespaces(empty.join(toReturn).replace('\n', ' '))



# Cut whitespaces at begin and end from text.
# Attributes: text = input string
def cutStartAndEndWhitespaces(text):
    firstCharStart = 0
    lastCharEnd = (len(text) - 1)
    for i in range(0, len(text)):
        if ord(text[i]) != ord(' '):
            firstCharStart = i
            break
    for i in range(len(text) - 1, -1, -1):
        if ord(text[i]) != ord(' '):
            lastCharEnd = i
            break
    return text[firstCharStart:(lastCharEnd + 1)]



# Return list of all tags + '$' not rendered in HTML documents.
# These tags do not have to be included in the process of parsing.
def getListOfUnrederedTags():
    return ['noframes$', 'audio$', 'canvas$', 'script$', 'noscript$', 'datalist$', 'embed$', 'meter$', 'progress$',
            'template$', 'video$', 'wbr$', 'area$', 'col$', 'iframe$', 'img$', 'input$', 'link$', 'meta$',
            'optgroup$', 'option$', 'param$', 'select$', 'style$', 'applet$', 'title$', 'body$', 'head$', 'center$',
            'frame$', 'frameset$', 'svg$']



# Extract all style information for a subtree expanded by node.
# Attributes: driver = Selenium driver, node = node, of which subtree is processed
def extractStyleForSubtreeRec(driver, node):
    childList = []
    for child in node.children:
        if isinstance(child, TreeElement):
            te = TreeElement()
            if not hasOnlyTreeChildren(child):
                te.style = parseStyle(driver, child.xpath)
            te.attributes = child.attributes
            te.tag = child.tag
            te.children = extractStyleForSubtreeRec(driver, child)
            childList.append(te)
        elif isinstance(child, TextElement):
            childList.append(child)
    return childList



# Removes empty nodes.
# Attributes: node = node, of which subtree is processed
def cleanMainContent(node):
    newChildren = []
    for child in node.children:
        if isinstance(child, TextElement) and hasNoContent(child):
            None
        elif isinstance(child, TreeElement):
            child = cleanMainContent(child)
            newChildren.append(child)
        else:
            newChildren.append(child)
    node.children = newChildren
    return node



# Checks, whether a TextElement node has no content
# Attributes: textNode = TextElement which is investigated
def hasNoContent(textNode):
    toReturn = True
    for c in textNode.text:
        if ord(c) > 32:
            toReturn = False
    return toReturn



# Checks, whether a nodes children are all TreeElements and do not hold a single TextElement.
# Attributes: node = node, of which subtree is investigated
def hasOnlyTreeChildren(node):
    toReturn = True
    for child in node.children:
        if isinstance(child, TextElement):
            toReturn = False
    return toReturn

