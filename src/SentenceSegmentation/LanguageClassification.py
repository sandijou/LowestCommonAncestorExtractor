from enum import Enum
import langid

class Lang(Enum):
    de = 0
    en = 1


# Classify language (en/de) of a text.
# Attributes: txt = input text as string
def classifyLanguage(txt):
    langid.set_languages(['de','en'])
    res = langid.classify(txt)
    return Lang(0) if res[0] == 'de' else Lang(1)



# Classify language (en/de) for a hierarchy tree by transforming it into a string and classify
# its language.
# Attributes: hierarchyTree = tree, for which the language is determined.
def getLang(hierarchyTree):
    mainContentText = hierarchyTree.getWholeContent()
    return classifyLanguage(mainContentText)
