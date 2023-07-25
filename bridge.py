import readCSV
import calculateInversion 


hands = readCSV.createArray([4,3,2,1,0])

print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))

hands = readCSV.createArray([1,2,3,4,0])

print("1,2,3,4 - ",calculateInversion.calculateInversion(hands))

hands = readCSV.createArray([19,12,6,2,1.5])

print("new - ",calculateInversion.calculateInversion(hands))

hands = readCSV.createArray([0,0,0,0,10])

print("count only 10's -  ",calculateInversion.calculateInversion(hands))



