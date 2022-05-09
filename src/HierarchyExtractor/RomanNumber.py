class RomanNumber:



    def __init__(self, num):
        self.num = num.upper()
        self.valid = True
        self.resolve = {
            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
        }
        for c in self.num:
            if c not in self.resolve.keys():
                self.valid = False


    # Get integer decimal value of a roman number.
    def getValue(self):
        if not self.valid:
            return -1
        else:
            reversed = self.num[::-1]
            indexList = ['I', 'V', 'X', 'L']
            lastIndex = 0
            sum = 0
            for c in reversed:
                if indexList.index(c) < lastIndex:
                    sum -= self.resolve[c]
                else:
                    lastIndex = indexList.index(c)
                    sum += self.resolve[c]
            return sum


    def isValid(self):
        return self.valid

