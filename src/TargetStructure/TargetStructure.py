from src.SentenceSegmentation.LanguageClassification import getLang
from src.SentenceSegmentation.Segmenter import segmentSentences
from src.TargetStructure.Document import Document
from src.TargetStructure.Section import parseToSections, Section


# Generates the JSON target structure.
# Attributes: hierarchyTree = root node of hierarchy tree; link = url to website;
# title = the websites title
def generateTargetStructure(hierarchyTree, link, title):
    language = getLang(hierarchyTree)

    document = Document(title, link)
    parseResult = parseToSections(hierarchyTree)
    if parseResult.text == '':
        sections = parseResult.subsections
    else:
        sections = [Section('', parseResult.text, [])] + parseResult.subsections
    segmentSentences(sections, language)
    document.content = sections

    toReturn = document.getExtraction()
    return toReturn
