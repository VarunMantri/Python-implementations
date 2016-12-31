"""
file: balances.py
language: python3
author1: vm9324@g.rit.edu Varun Rajiv Mantri
author2: sk1762@g.rit.edu Sourabh Khasbag
description: code to draw balance tree
"""

import turtle

superList=[]            # a global list used to insert all the beams for checking the balance of the same
changesTracker=[]       # a global list that keeps changes for weights labelled -1

'''
Weight class contains weight and distance slots.
'''
class Weight:
    __slots__ = ('weight', 'distance')

    def __init__(self, weight, distance):
        self.weight = weight
        self.distance = distance

'''
Beam class contains list called as bList which stores Weight objects
'''
class Beam:
    __slots__ = ('bList')

    def __init__(self):
        self.bList=[]

    def insert(self,weightObject):
        self.bList.append(weightObject)

    def draw(self,refList):
        '''
        draw function draws the turtle representation using the helper function
        :pre: position(0,0), pointing East, pen down
        :post:position(0,100),pointing East, pen down
        :param refList: list containing reference to root node
        :return: None
        '''
        rNode = refList[1]
        turtle.left(90)
        turtle.up()
        turtle.forward(100)
        turtle.down()
        turtle.left(180)
        turtle.left(90)
        changesTracker.reverse()
        self.helperDraw(rNode, 40, 150)

    def helperDraw(self,rNode, scalingFactor, scalingFactor2):
        '''
        helperDraw() is an helper function to draw() which draws balance tree recursively
        :pre:position(0,100),pointing East, pen down
        :post:position(0,100),pointing East, pen down
        :param rNode: reference to beam object(root node)
        :param scalingFactor: Horizontal scaling factor
        :param scalingFactor2: vertical scaling factor
        :return:
        '''
        #------------------------
        for item in rNode.bList:
            if int(item.distance) < 0:
                turtle.back(-1 * int(item.distance) * scalingFactor2)
                turtle.right(90)
                turtle.forward(scalingFactor)
                if isNumber(item.weight) == True:
                    turtle.forward(15)
                    turtle.up()
                    turtle.forward(15)
                    if int(item.weight) == -1:
                        temp=changesTracker.pop()
                        print('Calculated balance weight:'+str(temp))
                        turtle.write(temp)
                    else:
                        turtle.write(item.weight)
                    turtle.back(15)
                    turtle.down()
                    turtle.back(15 + scalingFactor)
                    turtle.left(90)
                    turtle.forward(-1 * int(item.distance) * scalingFactor2)
                else:
                    turtle.forward(40)
                    turtle.left(90)
                    max=scalingDecider(item)
                    self.helperDraw(item.weight, scalingFactor, (scalingFactor2-10)/max)
                    turtle.right(90)
                    turtle.back(40 + scalingFactor)
                    turtle.left(90)
                    turtle.forward(-1 * int(item.distance) * scalingFactor2)
            elif int(item.distance) > 0:
                turtle.forward(int(item.distance) * scalingFactor2)
                turtle.right(90)
                turtle.forward(scalingFactor)
                if isNumber(item.weight) == True:
                    turtle.forward(15)
                    turtle.up()
                    turtle.forward(15)
                    if int(item.weight) == -1:
                        temp=changesTracker.pop()
                        print('Calculated balance weight:'+str(temp))
                        turtle.write(temp)
                    else:
                        turtle.write(item.weight)
                    turtle.back(15)
                    turtle.down()
                    turtle.back(15 + scalingFactor)
                    turtle.left(90)
                    turtle.back(int(item.distance) * scalingFactor2)
                else:
                    turtle.forward(40)
                    turtle.left(90)
                    max=scalingDecider(item)
                    self.helperDraw(item.weight, scalingFactor , (scalingFactor2-10)/max )
                    turtle.right(90)
                    turtle.back(40 + scalingFactor)
                    turtle.left(90)
                    turtle.back(int(item.distance) * scalingFactor2)

def scalingDecider(item):
    '''
    scalingDecider finds out the maximum number of slots for a given beam(use full in deciding scaling factor)
    :param item: reference to a beam object
    :return: max: maximum number of slots present per given beam
    '''
    # checking the max for scaling factor
    if int(item.weight.bList[0].distance) < 0:
        max = (-1) * int(item.weight.bList[0].distance)
    else:
        max = int(item.weight.bList[0].distance)
    for it in item.weight.bList:
        if int(it.distance) < 0:
            if (-1) * int(it.distance) > max:
                max = (-1) * int(it.distance)
        else:
            max = int(it.distance)
    return max

def readFile():
    '''
    readFile() reads the input file and builds up a data structure
    :return: None
    '''
    fileName = input('Enter file name to be read')
    tList = []
    refList=[]
    try:
        with open (fileName) as file:
            for line in file:
                beam=Beam()
                wList=[]
                dList=[]
                namePtrList=[]
                alternater=1
                line=line.strip()
                tList=line.split()
                for item in tList[1:]:
                    if alternater==1:
                        dList.append(item)
                        alternater=-1
                    elif alternater==-1:
                        wList.append(item)
                        alternater=1
                for iterator in range(len(wList)):
                    temp=wList[iterator]
                    if temp[0]=='B':
                        for i in refList:
                            if wList[iterator] in i:
                                wList[iterator]=i[1]
                                refList.remove(i)
                    weightObject=Weight(wList[iterator],dList[iterator])
                    beam.insert(weightObject)
                namePtrList.append(line[0]+line[1])
                namePtrList.append(beam)
                refList.append(namePtrList)
        variable = refList[0]
        listComputer(variable[1])
        isBalance = checkBalance()
        if isBalance == True:
            print("The given structure is balanced, have a look at its turtle representation")
            b=Beam()
            b.draw(refList[0])
        else:
            print("The given structure is unbalanced!! No turtle representation needed.")
    except FileNotFoundError:
        print("Entered file name is incorrect!")


def checkBalance():
    '''
    function that checks if the structure is balanced
    :return: None
    '''
    effectiveTorque=0
    for item in superList:
        for wd in item.bList:
            effectiveTorque=effectiveTorque+(int(wd.weight)*int(wd.distance))
        if effectiveTorque!=0:
            return False
    return True


def listComputer(rNode):
    '''
    listComputer() builds up individual lists for every beam and calculates effective weight acting at every point
    This method also computes the missing weight if any
    :param rNode: reference to a beam object
    :return: summation of the effective weight of the beam
    '''
    beam = Beam()
    sum=0
    notify=0
    index=[]
    counter=0
    for item in range(len(rNode.bList)):
        if isNumber(rNode.bList[item].weight)==True:
            if int(rNode.bList[item].weight)==-1:
                notify=-1
                index.append(counter)
            else:
                sum=sum+int(rNode.bList[item].weight)
            weight=Weight(rNode.bList[item].weight,rNode.bList[item].distance)
            beam.insert(weight)
            counter=counter+1
        else:
            temp=listComputer(rNode.bList[item].weight)
            weight=Weight(temp,rNode.bList[item].distance)
            sum = sum + temp
            beam.insert(weight)
            counter=counter+1
    if notify==-1:
        for item in index:
            tsum = 0
            flag = 0
            if len(beam.bList)-1==(item):
                flag=1
            for ind in range(len(beam.bList[:item])):
                tsum=tsum+(int(beam.bList[ind].weight)*int(beam.bList[ind].distance))
            if flag==0:
                for ind in range(len(beam.bList[:item])+1,len(beam.bList)):
                    tsum=tsum+(int(beam.bList[ind].weight)*int(beam.bList[ind].distance))
            beam.bList[item].weight=-1*(tsum)/(int(beam.bList[item].distance))
            changesTracker.append(int(beam.bList[item].weight))
            sum=sum+int(beam.bList[item].weight)
    superList.append(beam)
    return sum


def isNumber(refObject):
    '''
    isNumber() determines if the input variable is holding a number
    :param refObject:
    :return: True if its a number, else False
    '''
    try:
        int(refObject)
        return True
    except:
        return False

def main():
    readFile()
    turtle.mainloop()

if __name__=="__main__":
    main()