from enum import Enum
from src.DOMParser.Font import Font
from src.HierarchyExtractor.RomanNumber import RomanNumber
import re

class EnumerationType(Enum):
    Numeric = 1
    Roman = 2
    Alphabetic = 3
    List = 4

# Compiled regex patterns for faster execution
roman_pattern = re.compile("[IVXLivxl]{1,7}")
numeric_pattern = re.compile("[0-9]{1,2}")
alphabetic_pattern = re.compile("[a-zA-Z]")

# Retrieve numeration from given text.
def getNumeration(txt):
    # Looking for possible numerations in text.
    possible_nums = re.search("\s[\(§]?(([IVXLivxl]{1,7})|([0-9]{1,2})|[a-zA-Z])([\.\-,:](([IVXLivxl]{1,7})|([0-9]{1,2})|[a-zA-Z]))*[\-:\.)]?\s", ' ' + txt + ' ')
    
    if possible_nums is None:
        return []
    else:
        # Normalizing different
        first_num = possible_nums[0][:-1]
        first_num = re.sub(r'[-,:)\(§\s\xa0]', '.', first_num)

        # Splitting string into different levels at dots.
        nums = first_num.split('.')
        return translateNums(nums)



# Translate list of strings to integer list; supports decimal numbers, roman numbers & letters.
def translateNums(nums):
    toReturn = []
    for n in nums:
        if roman_pattern.search(n):
            toReturn.append((RomanNumber(n).getValue(), EnumerationType.Roman))
        elif numeric_pattern.search(n):
            toReturn.append((int(n), EnumerationType.Numeric))
        elif alphabetic_pattern.search(n):
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

