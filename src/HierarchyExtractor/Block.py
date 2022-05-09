from enum import Enum
from src.DOMParser.Font import Font
from src.HierarchyExtractor.RomanNumber import RomanNumber
import re

class EnumerationType(Enum):
    Numeric = 1
    Roman = 2
    Alphabetic = 3
    List = 4

# Retrieve numeration from given text.
def getNumeration(txt):
    # Looking for possible numerations in text.
    possibleNums = re.search("\s[\(§]?(([IVXLivxl]{1,7})|([0-9]{1,2})|[a-zA-Z])([\.\-,:](([IVXLivxl]{1,7})|([0-9]{1,2})|[a-zA-Z]))*[\-:\.)]?\s", ' ' + txt + ' ')
    if possibleNums is None:
        return []

    else:
        # Normalizing different
        firstNum = possibleNums[0]
        firstNum = firstNum[:-1]
        firstNum = firstNum.replace('-', '.')
        firstNum = firstNum.replace(',', '.')
        firstNum = firstNum.replace(':', '.')
        firstNum = firstNum.replace(')', '.')
        firstNum = firstNum.replace('(', '')
        firstNum = firstNum.replace('§', '')
        firstNum = firstNum.replace(' ', '.')
        firstNum = firstNum.replace('\xa0', '.')

        # Splitting string into different levels at dots.
        nums = firstNum.split('.')
        return translateNums(nums)




# Translate list of strings to integer list; supports decimal numbers, roman numbers & letters.
def translateNums(nums):
    toReturn = []
    for n in nums:
        if re.search("[IVXLivxl]{1,7}", n):
            toReturn.append((RomanNumber(n).getValue(), EnumerationType.Roman))
        elif re.search("[0-9]{1,2}", n):
            toReturn.append((int(n), EnumerationType.Numeric))
        elif re.search("[a-zA-Z]", n):
            toReturn.append((ord(n.lower()) - 96, EnumerationType.Alphabetic))


    return toReturn



# A paragraph meant for building a tree.
class Block:

    def __init__(self, text, style):
        self.text = text
        self.numeration = getNumeration(text[:10])
        self.style = Font(12, False, False, 'FAMILY') if style is None else style

    def getWholeContent(self):
        if self.text is None:
            return ' '
        else:
            return self.text

    def __str__(self):
        return str(self.text)

    def getNumerationPattern(self):
        return list(map(lambda x: x[1], self.numeration))

    def getNumerationNumeral(self):
        return list(map(lambda x: x[0], self.numeration))

