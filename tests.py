import TradingCards as tc

def test_packs():

    testInputList = ['50%','30%','10%','5%','3%','1.5%','.5%']
    testWeightList = [.5,.3,.1,.05,.03,.015,.005]
    results = {x:0 for x in testInputList}
    print('Opening packs')

    for pack in tc.packs.values():
        cards = pack.openPack()

        for card in cards:
            print('{} {} from {}'.format(card.cardTier, card.cardName, pack.packName))

    print('Testing 10000 iterations of RNG')

    for x in range(10000):
        results[tc.weightchoice(testInputList, testWeightList)]+=1

    print(results)


if __name__ == '__main__':
    test_packs()
