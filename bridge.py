import readCSV
import calculateInversion 


hands = readCSV.createArray([4,3,2,1,0])
print(hands)

print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))

hands2 = readCSV.createArray([1,2,3,4,0])
print(hands2)

print("1,2,3,4 - ",calculateInversion.calculateInversion(hands2))


