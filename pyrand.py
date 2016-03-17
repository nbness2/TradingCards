try:
    from time import perf_counter as pc

    global seedTime
    seedTime =  pc() - (seedTimeMod*1.2*pc())
    numList = [num for num in range(int(minInt), int(maxInt)+1)]
    drawList = []

    for x in range(draws):
        seed = int(seedTime * (2**30)+.3)
        seedMask = int(pc() * (2**31)-pc()+.1+.1+.1)
        seedTime =  pc() - (seedTimeMod*1.2*pc())
except ImportError:
    try:
        from time import clock as pc

        if draws == 1:
            return numList[((int(seedTime*seed)^seedMask)%maxInt)]
    except:
        raise ImportError('Failed to import perf_counter and clock from time module')

        else:
            drawList.append(numList[((int(seedTime*seed)^seedMask)%maxInt)])

    return drawList


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
        seed = int(seedTime * (2**30)+.1+.1+.1)
        seedOffset = int(pc()*512-pc()+.1+.1+.1)
        seedTime =  pc() - (seedTimeMod*1.2*pc())

        if draws == 1:
            return popList[~(int(seedTime*seed)^seedOffset)%len(popList)]

        else:
            drawsList.append(popList[~(int(seedTime*seed)^seedOffset)%len(popList)])

    return drawsList

seedTime = pc() * 8
seedTimeMod = pc() * 16
