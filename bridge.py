import readCSV
import calculateInversion 
import matplotlib.pyplot as plt

hands = readCSV.createArray([4,3,2,1,0])
print("4,3,2,1 - ",calculateInversion.calculateInversion(hands))


hands = readCSV.createArray([1,2,3,4,0])
print("1,2,3,4 - ",calculateInversion.calculateInversion(hands))


hands = readCSV.createArray([19,12,6,2,1.5])
print("new - ",calculateInversion.calculateInversion(hands))


hands = readCSV.createArray([1,0,.5,0,0])
print("ace .5 - ",calculateInversion.calculateInversion(hands))

hands = readCSV.createArray([1,0,.6,0,0])
print("ace .6 - ",calculateInversion.calculateInversion(hands))

hands = readCSV.createArray([1,0,.4,0,0])
print("ace .4  - ",calculateInversion.calculateInversion(hands))

min = -1
minI = -1
x = []
y = []


for i in range(0,100):
    hands = readCSV.createArray([1,.66,.38,.2,.09])
    inversions = calculateInversion.calculateInversion(hands)
    if inversions < min or min < 0:
        min = inversions
        minI = i
    print(i, " has ", inversions)
    x.append(i)
    y.append(inversions)

print("done \n")
print(minI, " with ", min) 

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()



