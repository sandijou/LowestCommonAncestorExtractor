import src.ContentExtractor.ContentExtractorTypes
from src.ContentExtractor import ContentExtractor
from src.ContentExtractor.TreeUtilities import getFrequencyOfStyles
from src.HierarchyExtractor.EnumerationHierarchyExtractor import extractHierarchyNumerically
from src.HierarchyExtractor.VisualStyleHierarchyExtractor import extractHierarchyVisually


# Façade for different hierarchy extraction approaches.
# Attributes: mainContentDOMNode = node holding the main content; contentExtractor = content extractor type
def extractHierarchy(mainContentDOMNode, contentExtractor):
    defaultStyle = None

    # MCS is needed to determine non-headline style
    if contentExtractor is src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyleAndShortTextExclusion \
            or src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyleAndShortTextExclusion:
        dic = getFrequencyOfStyles(mainContentDOMNode, src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyleAndShortTextExclusion)
        defaultStyle = max(dic, key=dic.get)
    elif contentExtractor is src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyle or src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyle:
        dic = getFrequencyOfStyles(mainContentDOMNode, src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyle)
        defaultStyle = max(dic, key=dic.get)


    hierarchyTree = extractHierarchyVisually(mainContentDOMNode, defaultStyle)
    extractHierarchyNumerically(hierarchyTree)
    return hierarchyTree
