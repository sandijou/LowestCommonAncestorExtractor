from src.DOMParser.Font import Font
from src.DOMParser.DOMNode import TreeElement, TextElement
from io import StringIO
from lxml import etree



# Parse the HTML doc loaded as a Datalink by Selenium.
# Attributes: driver  = Selenium driver; extractStyle = whether style is rendered in this step
def parse_tree(sess_driver, extractStyle):    
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(sess_driver.page_source), parser)
    root = tree # -> lxml.etree._ElementTree, which represents the whole document, so it doesn't have a 'tag' (unclear why the copy?)
    #root = tree.getroot() -> lxml.etree._Element
    body = tree.xpath('/html/body')[0]
    xpath = tree.getpath(body)
    
    if not xpath == '/html/body':
        print(f"\n xpath =! /html/body: Root node: {root.getroot().tag}, body node: {body.tag}, xpath: {xpath}")
    
    toReturn = TreeElement() # => DOMnode self.tag = '',self.attributes = dict(), self.style = '',self.xpath = ''
    toReturn.tag = body.tag
    toReturn.xpath = xpath
    if extractStyle:
        toReturn.style = parseStyle(sess_driver, xpath)
        #print('ROOT style: ', toReturn.style)    
    toReturn.children = parseSeleniumTreeRec(sess_driver, root, body.xpath('child::node()'), extractStyle)    
    return toReturn

# Checking if manipulating the visual text content of the html document looses actual content
def print_string_difference(str1, str2):
    # Find the length of the shorter string
    length = min(len(str1), len(str2))
    # Iterate over the characters and compare
    #for i in range(length):
        #if str1[i] != str2[i]:
            #print(f"Difference at index {i}: '{str1[i]}' vs '{str2[i]}'")
    # Print the remaining characters if one string is longer than the other
    if len(str1) - length > 2:
        print(f"Additional characters in str1: '{str1[length:]}'")
    elif len(str2) - length > 2:
        print(f"Additional characters in str2: '{str2[length:]}'")

# Recursive counterpart to parseSeleniumTree
# Attributes: driver = Selenium driver; root = root HTML element; currentElem = node investigated in this recursion
# step; extractStyle = whether style is rendered
def parseSeleniumTreeRec(sess_driver, root, currentElem, extractStyle):
    childList = []
    for child in currentElem:
        if isinstance(child, str): # or isinstance(child, etree._ElementUnicodeResult):
            #cutted = cutStrToVisibleContent(child)
            reformatted = check_headline_formatting(child)
            
            # Checking for content loss
            #string1 = repr(reformatted)
            #string2 = repr(child)
            #print_string_difference(string1, string2)
            #if not cutted == '' and len(cutted) < 50:
                #print(f'\n TEXTelement: parent elem.tag {tmpTag}:  \n{repr(cutted)}\n')
            
            childList.append(TextElement(reformatted))
        #elif (str(child.tag) + '$') in getListOfUnrenderedTags():
          #print(f'found unrendered Tag: {str(child.tag)}')
        elif not ((str(child.tag) + '$') in getListOfUnrederedTags()) and not ('Comment' in str(child.tag)):
            #print(f"Processing element child with tag: {child.tag}")
            #tmpTag = str(child.tag)
            treeElement = TreeElement()
            xpath = root.getpath(child)
            treeElement.attributes = child.attrib
            treeElement.tag = child.tag
            treeElement.xpath = xpath
            if extractStyle:
                #if not hasOnlyTreeChildren(treeElement):
                treeElement.style = parseStyle(sess_driver, xpath)
            treeElement.children = parseSeleniumTreeRec(sess_driver, root, child.xpath('child::node()'), extractStyle)
            childList.append(treeElement)
        else:
            None
    return childList


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
    except Exception as e:
        # Print exception for debugging
        print("Exception occurred during style parsing:", str(e))
        # Return a fallback style object
        return Font(1, 300, False, 'undefined')


# Cut unimportant characters from text.
# Attributes: text = input string
def cutStrToVisibleContent(text):
    toReturn = ''.join(c for c in text if ord(c) == 10 or ord(c) >= 32)
    return toReturn.strip().replace('\n', ' ')

# (Cut whitespaces at begin and end from text. # Attributes: text = input string)
## Function replaced with cutStr above (string.strip())


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
    newChildren = [child for child in node.children if not (isinstance(child, TextElement) and hasNoContent(child))]
    for i, child in enumerate(newChildren):
        if isinstance(child, TreeElement):
            newChildren[i] = cleanMainContent(child)
    node.children = newChildren
    return node

# Checks, whether a TextElement node has no content
# Attributes: textNode = TextElement which is investigated
def hasNoContent(textNode):
    return not any(ord(c) > 32 for c in textNode.text)

# Checks, whether a nodes children are all TreeElements and do not hold a single TextElement.
# Attributes: node = node, of which subtree is investigated
def hasOnlyTreeChildren(node):
    return not any(isinstance(child, TextElement) for child in node.children)

