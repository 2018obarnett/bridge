def calculateInversion(hands):
    print("hands - ", hands)
    bins = generateBins(hands)
    newBins = sumBins(bins)
    return countInversion(newBins, bins)

def generateBins(hands):
    bins = []
    for i in range(0,14):
        bins.append({})
    for (points,tricks) in hands:
        if(tricks > 13 or tricks < 0):
            print("incorrect number of tricks: ", tricks)
        else: 
            if(points in bins[tricks]):
                bins[tricks][points]+=1
            else:
                bins[tricks][points] = 1
    print()
    print(bins)
    return bins

def sumBins(bins):
    sumBins = []
    print(bins)
    for bin in bins:
        keys = sorted(bin.keys())
        newBin = []
        total = 0
        for key in keys:
            total+=bin[key]
            newBin.append([key,total])
        
        sumBins.append(newBin)
    return sumBins

def countInversion(newBins, oldBins):
    index = 0
    total = 0
    for oldBin in oldBins:
        for key in oldBin.keys():
            for newBin in newBins[index+1:]:
                total += binarySearch(newBin, key)
                
        index+=1
    return total

def binarySearch(bins, value):
    low = 0
    high = len(bins)
    if(high == 0):
        return 0
    while(high > low):
        mid = (high+low) // 2
        if(bins[mid][0] == value):
            high = 0
        elif(bins[mid][0] > value):
            high = mid -1
        else:
            low = mid+1
    if(bins[mid][0] > value):
        if mid > 0:
            return bins[mid-1][1]
        else:
            return 0
    return bins[mid][1]
