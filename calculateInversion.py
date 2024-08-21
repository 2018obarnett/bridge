import bisect
import math
import time
from typing import Dict, List
from utility import Seat, Trump, getTricks
import pandas as pd

def calculateInversionForDF(df:pd.DataFrame) -> int:
    hands = []
    for _, row in df.iterrows():
        hands.append((row['NSPoints'], int(getTricks(Seat.North, Trump.No, row['trx']))))
    start_inv = time.time()
    inv = calculateInversion(hands)
    print("Inversion time: ", time.time()-start_inv)
    
    start_inv = time.time()
    altInv = altCalculateInversion(hands)
    print("altInversion time: ", time.time()-start_inv)
    print("Inversion: ", inv, " altInversion: ", altInv)
    
    return inv
    

def altCalculateInversion(hands:List[int]) -> int:
    distribution = generateDistribution(hands)
    cumBins = getCumulativeDistribution(distribution)
    return round(acountInversionsFromDict(distribution, cumBins))

def calculateInversion(hands:List[int]) -> int:
    bins = generateDistribution(hands)
    newBins = sumBins(bins)
    return round(countInversion(newBins, bins))

def generateDistribution(hands:List[List[int]]) -> List[Dict[int, int]]:
    '''
    Generate an array of dicts to represent the distribution of hands by points and tricks
    bins[tricks][points] = count

    Args:
        hands (List[List[int]]): A list of tuples (points, tricks)

    Returns:
        List[Dict[int, int]]: array of dicts representing the distribution of hands by points and tricks
    '''
    distribution = [{} for _ in range(0, 14)]
    for points, tricks in hands:
        if (tricks > 13 or tricks < 0):
            print("Invalid number of tricks: ", tricks)
        else: 
            if (points in distribution[tricks]):
                distribution[tricks][points] += 1
            else:
                distribution[tricks][points] = 1
    return distribution

def getCumulativeDistribution(distribution:List[Dict[int, int]]) -> List[Dict[int, int]]:
    '''
    for each bin [now looking at all hands with same number of tricks taken]
        sort the keys (number of points)
        get cumulative sum, so newBin represents [points, number of hands that took same number of tricks with this many points or fewer]
        create a new bin with the key and the cumulative sum of the values
    for the provided distribution of d[tricks][points] = count, calculate
                                    cd[tricks][points] = count of hands that took same number of tricks with same or fewer points
        

    Args:
        bins (List[Dict[int, int]]): array of dicts representing the distribution of hands by points and tricks

    Returns:
        List[Dict[int, int]]: list of dicts representing the cumulative totals of hands by points and tricks, 
                                result[tricks][points] = cumulative total of hands taking exactly that many tricks and had that many or fewer points
    '''
    cumulativeDistribution = [{} for _ in range(0, 14)]
    for numTricks in range(len(cumulativeDistribution)):
        pointSet = sorted(distribution[numTricks].keys())
        runningTotal = 0
        for point in pointSet:
            runningTotal += distribution[numTricks][point]
            cumulativeDistribution[numTricks][point] = runningTotal
    return cumulativeDistribution
        

def countInversionsFromDict(distribution:List[Dict[int, int]], cumDistribution:List[Dict[int, int]]) -> int:
    ### TODO: vectorize with numpy
    '''
    _summary_

    Args:
        bins (List[Dict[int, int]]): bin[tricks][points] = number of hands with exactly that many points that took exactly that number of tricks
        cumulativeBins (List[Dict[int, int]]): cumBin[tricks][points] = number of hands taking exactly that many tricks with this many or fewer points

    Returns:
        int: number of pairs of hands where points(h1) > points(h2) and tricks(h1) < tricks(h2)
    '''
    total = 0
    for ind in range(len(distribution)):
        bin = distribution[ind]
        for numPoints in bin.keys():
            # find hands that took more tricks with fewer points
            diff = 0
            for cumBin in cumDistribution[ind+1:]:
                diff += 1
                # Number of hands that took
                if not cumBin or numPoints <= min(cumBin.keys()):
                    count = 0
                else:
                    count = cumBin[max([k for k in cumBin.keys() if k < numPoints])]
                total += bin[numPoints] * count * math.sqrt(diff)
    return total

def acountInversionsFromDict(distribution: List[Dict[int, int]], cumDistribution: List[Dict[int, int]]) -> int:
    total = 0

    # Precompute the maximum key for each dictionary in cumDistribution to avoid recalculating inside the loop
    max_keys = []
    sorted_cum_keys = []
    for cumBin in cumDistribution:
        if cumBin:
            max_keys.append(max(cumBin.keys()))
            sorted_cum_keys.append(sorted(cumBin.keys()))
        else:
            max_keys.append(float('-inf'))
            sorted_cum_keys.append([])

    for ind, bin in enumerate(distribution):
        for numPoints, bin_count in bin.items():
            diff = 0
            for j in range(ind + 1, len(cumDistribution)):
                diff += 1

                # Skip unnecessary checks based on precomputed max_keys
                if max_keys[j] < numPoints:
                    continue

                # Binary search to find the largest key in cumBin that is less than numPoints
                keys = sorted_cum_keys[j]
                pos = bisect.bisect_left(keys, numPoints)
                if pos > 0:
                    max_valid_key = keys[pos - 1]
                    count = cumDistribution[j][max_valid_key]
                else:
                    count = 0

                total += bin_count * count * math.sqrt(diff)

    return total

def sumBins(bins:List[Dict[int, int]]) -> List[List[int]]:
    '''
    _summary_
    
    for each bin [now looking at all hands with same number of tricks taken]
        sort the keys (number of points)
        get cumulative sum, so newBin represents [points, number of hands that took same number of tricks with this many points or fewer]
        create a new bin with the key and the cumulative sum of the values
        
    result is an array of pairs (why not dict?) consisting of [points, ]
    
        

    Args:
        bins (List[Dict[int, int]]): array of dicts representing the distribution of hands by points and tricks

    Returns:
        List[List[int]]: _description_
    '''
    sumBins = []
    for bin in bins: 
        keys = sorted(bin.keys())
        newBin = []
        total = 0
        for key in keys:
            total += bin[key]
            newBin.append([key,total])
        sumBins.append(newBin)
    return sumBins

def countInversion(newBins, oldBins):
    index = 0
    total = 0
    for oldBin in oldBins:
        for key in oldBin.keys():
            diff = 1
            for newBin in newBins[index+1:]:
                count = binarySearch(newBin, key)
                total += (math.sqrt(diff))*count*oldBin[key]
                diff+=1
                
        index+=1
    return total

def binarySearch(bins, value):
    '''
    _summary_

    Args:
        bins (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    '''
    low = 0
    high = len(bins)
    if (high == 0):
        return 0
    
    while(high > low):
        mid = (high + low) // 2
        if (bins[mid][0] == value):
            high = 0
        elif (bins[mid][0] > value):
            high = mid -1
        else:
            low = mid+1
            
    if(bins[mid][0] > value):
        if mid > 0:
            return bins[mid-1][1]
        else:
            return 0
    return bins[mid][1]
