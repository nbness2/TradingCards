import TCGMain as tc
from modules import pyrand

def runTests():
    rngTest()
    packTest()

def rngTest():

    testInputList = ('50', '30', '10', '5', '3', '1.5', '.5')
    perfectResults = {x+'%':int(float(x)*100) for x in testInputList}
    testInputList = [x+'%' for x in testInputList]
    testWeightList = (.5, .3, .1, .05, .03, .015, .005)
    results = {x:0 for x in testInputList}
    print('\nTesting 10000 iterations of 1-draw weighted choice rng~~')

    for test in range(10000):
        result = pyrand.weightchoice(testInputList, testWeightList)
        results[result] += 1

    print(results)
    results = {x:0 for x in testInputList}
    print('\nTesting 1000 iterations of 10-draw weighted choice rng~~')

    for test in range(1000):
        resultList = pyrand.weightchoice(testInputList, testWeightList, draws = 10)

        for result in resultList:
            results[result] += 1

    print(results)
    results = {x:0 for x in testInputList}
    print('\nTesting 100 iterations of 100-draw weighted choice rng~~')

    for test in range(100):
        resultList = pyrand.weightchoice(testInputList, testWeightList, draws = 100)

        for result in resultList:
            results[result] += 1

    print(results)
    print('\nPerfect results~~')
    print(perfectResults)

    testInputList = [x+1 for x in range(25)]
    results = {x:0 for x in testInputList}
    print('\nTesting 100 iterations of 100-draw non-weighted 1-25 randint() choice rng~~')

    for test in range(100):
        resultList = pyrand.randint(1, 25, 100)

        for result in resultList:
            results[result] += 1

    print(results)

def packTest():

    print('Opening packs')
    print('Testing opening packs. Opening 10 rounds of packs.\n')

    for pack in tc.packs.values():

        print(pack.packName, pack.cardAmt, pack.themeCardChance, pack.maxThemed)

        for x in range(10):
            print('\tPack', x+1, end='\n\t\t')
            cards = pack.openPack()

            for card in cards:
                print(card.cardTier, card.cardName, end=', ')

            print()

def strTest():

    print('Generating 10 random strings with a length of 15 characters')
    for x in range(15):
        print(pyrand.randstring(15, 512))

def testPack(packName, packAmt = 25, printRes = False):

    try:
        pack = tc.packs[packName]

    except:
        raise ValueError('Invalid pack name: {0}'.format(packName))

    tca = packAmt*pack.cardAmt
    cardList = []
    tcc = 0

    for x in range(packAmt):
        cardList.extend(pack.openPack())

    for card in cardList:

        if card.cardTheme == pack.extraTheme:
            tcc += 1

    cardList = []
    tccp = round(tcc/tca*100, 4)

    if printRes:
        print(tcc, 'out of', tca, 'cards were themed giving a total of', tccp, '% themed cards')
        print('optimal themed cards is', tca*pack.themeCardChance)

    return tcc, tccp




if __name__ == '__main__':
    strTest()
