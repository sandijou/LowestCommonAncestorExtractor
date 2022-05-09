from selenium import webdriver
from src.DOMParser.DOMParser import parseTree, parseStyle, extractStyleForSubtreeRec


# Download and parse DOM-tree for a website.
# Attributes: link = url to the website; getStyle = whether css rendered style should be parsed in this step;
# driver = Selenium driver
def getDOMTree(link, getStyle, driver):
    close = False
    if driver is None:
            driver = webdriver.Chrome(executable_path='../../chromedriver')
            close = True
    driver.get(link)
    body = parseTree(driver, getStyle)
    title = driver.title
    if close:
            driver.close()
    return (body, title)



# Extracts CSS style information for a given subtree.
# Attributes: url = url to the website; mainContentNode = node, which subtree is processed;
# driver = Selenium driver
def extractStyleForSubtree(url, mainContentDOMNode, driver=None):
    close = False
    if driver is None:
        driver = webdriver.Chrome(executable_path='../../chromedriver')
        close = True

    driver.get(url)
    mainContentDOMNode.style = parseStyle(driver, mainContentDOMNode.xpath)
    mainContentDOMNode.children = extractStyleForSubtreeRec(driver, mainContentDOMNode)
    if close:
        driver.close()
    return mainContentDOMNode
