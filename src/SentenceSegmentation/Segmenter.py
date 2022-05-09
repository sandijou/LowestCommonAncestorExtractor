from somajo import SoMaJo
from src.SentenceSegmentation.LanguageClassification import Lang



# Segment and tokenize a German string.
# Attributes: input = string to be tokenized
def getTokensFromStringDe(input):
    tokenizer = SoMaJo("de_CMC", split_sentences=True)
    toReturn = []
    sentences = tokenizer.tokenize_text([input])
    for sentence in sentences:
        senteceList = []
        for word in sentence:
            senteceList.append(word.text)
        toReturn.append(senteceList)
    return toReturn



# Segment and tokenize an English string.
# Attributes: input = string to be tokenized
def getTokensFromStringEn(input):
    tokenizer = SoMaJo("en_PTB", split_sentences=True)
    toReturn = []
    sentences = tokenizer.tokenize_text([input])
    for sentence in sentences:
        senteceList = []
        for word in sentence:
            senteceList.append(word.text)
        toReturn.append(senteceList)
    return toReturn



# Segment and tokenize a tree.
# Attributes: tree = node, which subtree will be processed; lang = language of content (en/de)
def segmentSentences(tree, lang):
    for subsection in tree:
        if lang is Lang.de:
            subsection.text = getTokensFromStringDe(subsection.text)
        elif lang is Lang.en:
            subsection.text = getTokensFromStringEn(subsection.text)
        segmentSentences(subsection.subsections, lang)



