import TradingCards as tc

def run_tests():

    testInputList = ['50%','30%','10%','5%','3%','1.5%','.5%']
    testWeightList = [.5,.3,.1,.05,.03,.015,.005]
    results = {x:0 for x in testInputList}
    print('Opening packs')
    print('Testing opening packs. Opening 10 rounds of packs.\n')

    for pack in tc.packs.values():

        print(pack.packName, pack.cardAmt, pack.themeCardChance, pack.maxThemed)

        for x in range(10):

            print('\tPack', x+1)
            cards = pack.openPack()

            for card in cards:
                print('\t\t', card.cardTier, card.cardName)

    print('\nTesting 10000 iterations of RNG')

    for x in range(10000):
        results[tc.weightchoice(testInputList, testWeightList)]+=1

    print(results)


if __name__ == '__main__':
    run_tests()
