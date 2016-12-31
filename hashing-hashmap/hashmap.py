__author__ = 'zjb'
__author__='Varun Rajiv Mantri'

from collections import namedtuple
import re
import io

Entry = namedtuple('Entry', ('key', 'value','collisions'))

class _delobj: pass
DELETED = Entry(_delobj(),None,None)

class Hashmap:

    __slots__ = 'table','numkeys','cap','maxload','probes','NoCollisions','hashStringer'

    def __init__(self,funHash,initsz=100,maxload=0.7):
        '''
        Creates an open-addressed hash map of given size and maximum load factor
        :param initsz: Initial size (default 100)
        :param maxload: Max load factor (default 0.7)
        :param funHash: Hash Function to be used by the hash map
        '''
        self.cap = initsz
        self.table = [None for _ in range(self.cap)]
        self.numkeys = 0
        self.maxload = maxload
        self.probes=0
        self.NoCollisions=0
        self.hashStringer=funHash

    def put(self,key,value,defaultVal=1,rehashFlag=False):
        '''
        Adds the given (key,value) to the map, replacing entry with same key if present.
        Also keeps the count of number of collisions and probings that occure
        :param key: Key of new entry
        :param value: Value of new entry
        '''

        index = self.hashStringer(key) % self.cap
        #print("put called", key,index)
        #enteredFlag=0
        if self.table[index] is not None:
            self.NoCollisions=self.NoCollisions+1
        while self.table[index] is not None and \
                        self.table[index] != DELETED and \
                        self.table[index].key != key:
            self.probes=self.probes+1
            index += 1
            if index == len(self.table):
                index = 0
        if rehashFlag ==False and self.table[index] is None:
            self.numkeys += 1
            self.table[index] = Entry(key,value,defaultVal)
        elif rehashFlag==False and self.table[index].key == key:
            retrivedValue=int(self.table[index].collisions)
            #print(key,"Value is",retrivedValue)
            self.table[index] = Entry(key, value, retrivedValue+1)
        elif rehashFlag==True:
            #retrivedValue = int(self.table[index].collisions)
            # print(key,"Value is",retrivedValue)
            self.numkeys += 1
            self.table[index] = Entry(key, value, defaultVal)
        if self.numkeys/self.cap > self.maxload:
            # rehashing
            oldtable = self.table
            # refresh the table
            self.cap *= 2
            self.table = [None for _ in range(self.cap)]
            self.numkeys = 0
            # put items in new table
            for entry in oldtable:
                if entry is not None:
                    self.put(entry[0],entry[1],entry[2],True)

    def printAll(self):
        for item in self.table:
            if item!=None:
                print("word:"+str(item.value)+" count:"+str(item.collisions))

    def findMax(self):
        refernce=1
        maxWord=""
        for item in self.table:
            if item!=None:
                if int(refernce)<int(item.collisions):
                    maxWord=item.value
                    refernce=item.collisions
        return maxWord

    def wordCounter(self,word):
        index=self.hash_func(word)%self.cap
       #print('testing:'+str(self.table[index].value))
        while self.table[index]!=None  and self.table[index].value!=word:
            index=index+1
            if index == len(self.table):
                index = 0
        if self.table[index]==None:
            print("This word has occured 0 times")
        else:
            print("This word occured "+ str(self.table[index].collisions))

    def remove(self,key):
        '''
        Remove an item from the table
        :param key: Key of item to remove
        :return: Value of given key
        '''
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            index += 1
            if index == len(self.table):
                index = 0
        if self.table[index] is not None:
            self.table[index] = DELETED


    def get(self,key):
        '''
        Return the value associated with the given key
        :param key: Key to look up
        :return: Value (or KeyError if key not present)
        '''
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            self.probes = self.probes + 1
            index += 1
            if index == self.cap:
                index = 0
        if self.table[index] is not None:
            return self.table[index].value
        else:
            raise KeyError('Key ' + str(key) + ' not present')

    def __contains__(self,key):
        '''
        Returns True/False whether key is present in map
        :param key: Key to look up
        :return: Whether key is present (boolean)
        '''
        index = self.hash_func(key) % self.cap
        while self.table[index] is not None and self.table[index].key != key:
            self.probes = self.probes + 1
            index += 1
            if index == self.cap:
                index = 0
        return self.table[index] is not None

    def hash_func(self,key):
        '''
        Not using Python's built in hash function here since we want to
        have repeatable testing...
        However it is terrible.
        Assumes keys have a len() though...
        :param key: Key to store
        :return: Hash value for that key
        '''
        # if we want to switch to Python's hash function, uncomment this:
        #return hash(key)
        return len(key)


def hasher(key):
    return hash(key)

def printMap(map):
    for i in range(map.cap):
        print(str(i)+": " + str(map.table[i]))

def readFile(filename,map):
    with io.open(filename,encoding='utf8') as file:
        for line in file:
            line = line.strip()
            line=re.split('\W+',line)
            for word in line:
                if len(word)!=0:
                    word=str.lower(word)
                    insertMap(word,map)
    print("Collisions:" + str(int(map.NoCollisions)))
    print("Probes:" +str(int(map.probes)))
    print("HashQul"+str((1/int(map.probes))))
    print('Maximum occuring word is: '+str(map.findMax()))

def hashStringer(key):
        alternater=1
        result=''
        if len(key)!=1:
            for item in key:
                if alternater==1:
                    val = str((ord(item) - 22) * 9)
                    result=result+val[len(val)-2]
                    alternater=-1
                else:
                    val=str((ord(item)-22)*9)
                    result=result+val[1]
                    alternater=1
        else:
            result=ord(key)
        result=str(result*31)
        sum=0
        for item in result:
            sum=sum+int(item)
        if sum%2==0:
            result=int(result)>>1
            result = str(result-1)
        else:
            result=str(int(result)>>2)
        sum = 0
        for item in result:
            if item!='-':
                sum = sum + int(item)
        if int(sum)%2==0:
            result=int(result)*97
            result=result>>1
        else:
            result = int(result) * 41
            result = result >> 2

        return hash(key)
def insertMap(word,map):
    map.put(word,word)

def testMap():
    map = Hashmap(hashStringer)
    filename=input("Enter file name")
    readFile(filename,map)

if __name__ == '__main__':
    testMap()
