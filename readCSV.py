import csv
from typing import List


def createArray(weights:List[float]):
    with open('HandRecords/1000Deals-1.csv', newline='') as csvfile:
        hands = []
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        for row in spamreader:
            tricks = row[1]

            hand1 = row[2]+row[3]+row[4]+row[5]
            hand2 = row[6]+row[7]+row[8]+row[9]

            aces = hand1.count('A') + hand2.count('A')
            king = hand1.count('K') + hand2.count('K')
            queen = hand1.count('Q') + hand2.count('Q')
            jack = hand1.count('J') + hand2.count('J')
            tens = hand1.count('T') + hand2.count('T')

            hands.append([(aces*weights[0])+(king*weights[1])+(queen*weights[2])+(jack*weights[3])+(tens*weights[4]), int(tricks)])
    
    csvfile.close()
    return hands
