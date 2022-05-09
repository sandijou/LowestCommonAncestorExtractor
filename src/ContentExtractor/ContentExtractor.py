from src.ContentExtractor.TreeUtilities import getFrequencyOfStyles, getLowestCommonAncestorNodeOfStyle

# Enum for different content extractors presented in the thesis.
from src.DOMParser.DOMParser import cleanMainContent


# Extracting the main content using the method presented in the thesis.
# Attributes: body = body HTML node; contentExtractor = content extraction method; threshold = minimum coverage for
# main content node.
def getMainContent(bodyDOMNode, contentExtractor, threshold):
    dic = getFrequencyOfStyles(bodyDOMNode, contentExtractor)
    max_key = max(dic, key=dic.get)
    mainContent = getLowestCommonAncestorNodeOfStyle(bodyDOMNode, max_key, dic[max_key], threshold, contentExtractor)

    # Clean main content from empty nodes and other
    cleanMainContent(mainContent)
    return mainContent
