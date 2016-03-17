try:
    from time import perf_counter as pc

except ImportError:
    try:
        from time import clock as pc

    except:
        raise ImportError('Failed to import perf_counter and clock from time module')

def randint(minInt = 0, maxInt = 100, draws = 1):

    return weightchoice(range(minInt, maxInt+1), draws = draws)


def weightchoice(inputList, weightList = None, draws = 1, maxPrecision = 3):

    global seedTime

    try:
        draws = int(draws)

    except:
        raise TypeError('draws must be convertable to int()')

    if weightList == None:
        weightList = [1/len(inputList) for x in inputList]

    if draws < 1:
        raise ValueError('You can\'t have less than 1 draw')
    
    if not len(inputList) == len(weightList):
        raise ValueError('The length of input list ({0}) and weight list ({1}) must be equal'.format(len(inputList),
                                                                                                     len(weightList)))
    if not round(sum(weightList), maxPrecision) == 1:
        print(round(sum(weightList),maxPrecision))
        raise ValueError('The sum of all weights ({0}) must equal 1'.format(sum(weightList)))

    popList = []

    for inp, weight in zip(inputList, weightList):

        for i in range(int(weight*(10**maxPrecision))):
            popList.append(inp)

    drawsList = []

    for x in range(draws):
        seed = int(seedTime * (2**31)+.3)
        seedOffset = int(pc()*512-pc()+.3)
        seedTime = pc() - (seedTimeMod*pc())
        result = popList[~(int(seedTime*seed)^seedOffset)%len(popList)]

        if draws == 1:
            return popList[~(int(seedTime*seed)^seedOffset)%len(popList)]

        else:
            drawsList.append(popList[~(int(seedTime*seed)^seedOffset)%len(popList)])

    return drawsList

seedTime = pc() * 16
seedTimeMod = seedTime*2
