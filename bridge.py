import readCSV
import calculateInversion 


hands = readCSV.createArray([4,3,2,1,0])

print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))




hands = readCSV.createArray([4,3,2,1,0])
hands = hands*1000000
print(len(hands))

print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))

