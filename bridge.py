import readCSV
import calculateInversion 


hands = readCSV.createArray([40,3,2,1,0])

print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))

hands2 = readCSV.createArray([1,2,3,4,50])

print("1,2,3,4 - ",calculateInversion.calculateInversion(hands2))


