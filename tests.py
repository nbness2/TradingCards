import TradingCards as tc
import pyrand


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
            print('\tPack', x+1)
            cards = pack.openPack()

            for card in cards:
                print('\t\t', card.cardTier, card.cardName)

if __name__ == '__main__':
    runTests()
