#from functools import total_ordering


#@total_ordering
class Font:

    def __init__(self, size, weight, underlined, fontFamily):
        self.weight = weight
        self.isUnderlined = underlined
        self.fontSize = size
        self.fontFamily = fontFamily

    def __str__(self):
        string = "<Font: Size " + str(self.fontSize) + "px | Props ["
        string = string + "Weight=" + str(self.weight)
        if self.isUnderlined:
            string = string + "Underlined"
        string = string + "] | Family " + str(self.fontFamily) + ">"
        return string

    def __eq__(self, other):
        if other is None:
            return False
        return self.weight == other.weight and self.isUnderlined == other.isUnderlined \
            and self.fontFamily == other.fontFamily and self.fontSize == other.fontSize

    def __hash__(self):
        return hash(self.weight) ^ hash(self.isUnderlined) ^ hash(self.fontSize) ^ hash(self.fontFamily)

