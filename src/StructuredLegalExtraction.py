from enum import Enum

from selenium import webdriver

import src.ContentExtractor.ContentExtractorTypes
from src.ContentExtractor import ContentExtractor
from src.ContentExtractor.ContentExtractor import getMainContent
from src.ContentExtractor.TreeUtilities import getFrequencyOfStyles
from src.Downloader.Downloader import getDOMTree, extractStyleForSubtree
from src.HierarchyExtractor.HierarchyExtractor import extractHierarchy
from src.TargetStructure.TargetStructure import generateTargetStructure


def extractTandC(url, contentExtractor=src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyleAndShortTextExclusion,
                 threshold=0.85, driver=None):

    # Check for legality of threshold.
    if not threshold > 0.5:
        print('Threshold must be above 0.5!')
        return None

    # Use Downloader component:
    extractStyle = False
    if contentExtractor is src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyle \
            or contentExtractor is src.ContentExtractor.ContentExtractorTypes.ContentExtractor.RenderedStyleAndShortTextExclusion:
        extractStyle = True
    website = getDOMTree(url, extractStyle, driver)
    title = website[1]
    bodyNode = website[0]


    # Use Content Extractor component:
    mainContent = getMainContent(bodyNode, contentExtractor, threshold)


    # Add styling if this did not happen before.
    if not extractStyle:
        extractStyleForSubtree(url, mainContent, driver)

    hierarchyTree = extractHierarchy(mainContent, contentExtractor)

    toReturn = generateTargetStructure(hierarchyTree, url, title)
    return toReturn


#def extractTandC_content(link, driver=None):
#    website = getDOMTree(link, False, driver)
#    bodyNode = website[0]
#    dic = getFrequencyOfStyles(bodyNode, src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyleAndShortTextExclusion)
#    mainContent = getMainContent(bodyNode, src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyleAndShortTextExclusion, 0.85)
#    return (mainContent.getWholeContent(), bodyNode.getWholeContent(), dic, mainContent)



# Extract multiple T&Cs with the same driver and return result list.
# Attributes: links = list of links as string; contentExtractor = content extraction method; threshold = minimum
# coverage for main content node; driver = Selenium driver
def extractTandD_multiple(links, contentExtractor=src.ContentExtractor.ContentExtractorTypes.ContentExtractor.NaiveStyleAndShortTextExclusion,
                          threshold=0.85, driver=None):
    close = False
    if driver is None:
        close = True
        driver = webdriver.Chrome(executable_path='../chromedriver')
    results = []
    for link in links:
        results.append(extractTandC(link, contentExtractor, threshold, driver))
    if close:
        driver.close()
    return results
