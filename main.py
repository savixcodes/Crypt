import hashlib
import random

key = ""

dicts = {}
numofDupl = 1
values = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
          "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ' ', '.', '!', '?']
global_values = ""
symbols = ["!", "?", "#", "^", "(", "@", "*", "&", ")", "+", "["]
keys = range((len(values)))
for i in keys:
    dicts[i] = values[i]

last = []

for x in range(0, 31):
    key += values[random.randrange(0, len(values)-1)]
print(f"This is the key: {key}")

def get_key(val):
    for key, value in dicts.items():
        if val == value:
            return key

    return "key doesn't exist"


def calc(string):
    global last
    i = 0
    overTheLimit = 0
    last_word = get_key(string[0])
    numofDupl = 1
    last = [dicts[get_key(string[0])]]
    while i < len(values) - 1:
        if dicts[int((get_key(string[i]) * last_word) + get_key(string[i])) % 26] not in last:
            last.append(dicts[int((get_key(string[i]) * last_word) + get_key(string[i])) % 26])
        else:
            if numofDupl < 10:
                last.append(str(numofDupl))
                numofDupl = numofDupl + 1
            else:
                last.append(symbols[overTheLimit])
                overTheLimit += 1
                numofDupl += 1
        last_word = int((get_key(string[i]) * last_word) + get_key(string[i])) % 26
        i += 1
    return last


def hash_key(tkey):
    hashed_output = hashlib.sha256(tkey.encode('ascii')).hexdigest()
    return hashed_output


def shift_map(mapdict, tkey):
    hash_key(tkey)


def encrypt(message, key):
    newMessage = ""
    cmap = calc(key)
    shift = ShiftingAlgo()
    tempValues = shift.shift_map(cmap, key)
    dmap = tempValues[0]
    global global_values
    global_values = tempValues[1]
    for eachLetter in message:
        newMessage += (dmap[get_key(eachLetter)])
    r = Repeater()
    newerMessage = r.main(global_values, newMessage)
    print(newerMessage)
    return newerMessage


def decrypt(message, key):
    newMessage = ""
    cmap = calc(key)
    shift = ShiftingAlgo()
    tempValues = shift.shift_map(cmap, key)
    dmap = tempValues[0]
    global global_values
    global_values = tempValues[1]

    r = Repeater()
    newerMessage = r.reverse(global_values, message)
    for eachLetter in newerMessage:
        newMessage += (dicts[dmap.index(eachLetter)])
    print(newMessage)
    return newerMessage


class ShiftingAlgo:
    hashNum = ""
    dicts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
             19, 20, 21, 22, 23, 24, 25, 26]
    values = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
              "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    def hash_key(self, tkey):
        hashed_output = hashlib.sha256(tkey.encode('ascii')).hexdigest()
        self.hashNum = hashed_output
        return hashed_output

    def gen_array(self, tkey):
        array = []
        temp = self.hash_key(tkey)
        i = 0
        while i < len(temp):
            array.append(temp[i])
            i += 1
        return array

    def gen_number(self, tkey):
        newMap = self.gen_array(tkey)
        array = [None] * len(newMap)
        x = 1

        for eachValue in values:
            i = 0
            while i < len(newMap):
                if eachValue in newMap[i]:
                    newMap[i] = str(x)
                    array[i] = newMap[i]
                i += 1
            x += 1

        prevNum = 0
        sumOfNum = 0
        for eachNum in newMap:
            sumOfNum = int(eachNum) + int(prevNum)
            prevNum = eachNum
            newNum = sumOfNum % 26
        return newNum

    def shift_map(self, cmap, key):
        num = self.gen_number(key)
        newArray = [None] * 30
        i = -num
        x = 0
        while x < 30:
            newArray[x] = cmap[i]
            x += 1
            i += 1

        return [newArray, self.hashNum]


class Repeater:
    global last
    listOfRepeats = []

    def hash_hash(self, hashV):
        hashed_output = hashlib.sha256(hashV.encode('ascii')).hexdigest()
        return hashed_output

    def gen_num(self, hashV):
        shift = ShiftingAlgo()
        number = shift.gen_number(hashV)
        return number

    def add_to_list(self, hashV):
        self.listOfRepeats = []
        i = 0
        numOfIterations = self.gen_num(self.hash_hash(hashV))
        while i < numOfIterations:
            self.listOfRepeats.append(last[i])
            i += 1

    def main(self, hashV, text):
        self.add_to_list(hashV)

        array = []
        counter = 0
        string = ""
        for eachLetter in text:
            array.append(eachLetter)
        tempHash = hashV
        for eachRepeat in self.listOfRepeats:
            i = 0
            x = 0
            j = 1
            jk = j

            while jk > 0:
                tempHash = self.hash_hash(tempHash)
                jk -= 1
            j += 1
            while i < len(text) + counter:
                try:
                    l = self.gen_num(tempHash) % 4
                    if eachRepeat == array[i + x]:
                        while l > 1:
                            array.insert(i + x, eachRepeat)
                            counter += 1
                            x += 1
                            l -= 1
                    else:
                        pass
                except:
                    pass
                i += 1

        for eachLetter in array:
            string += eachLetter
        print(self.listOfRepeats)
        return string

    def reverse(self, hashV, text):

        self.add_to_list(hashV)
        tempHash = hashV

        array = []
        counter = 0
        string = ""
        for eachLetter in text:
            array.append(eachLetter)

        for eachRepeat in self.listOfRepeats:
            i = 0
            x = 0
            j = 1
            jk = j

            while jk > 0:
                tempHash = self.hash_hash(tempHash)
                jk -= 1
            j += 1

            while i < len(text):
                try:
                    z = self.gen_num(tempHash) % 4
                    if eachRepeat == array[i]:
                        while z > 1:
                            del array[i + 1]
                            counter += 1
                            x += 1
                            z -= 1
                    else:
                        pass
                except:
                    pass
                i += 1

        for eachLetter in array:
            string += eachLetter

        return string


encrypted_message = encrypt("hello world", key.lower())

decrypt(encrypted_message, key.lower())

