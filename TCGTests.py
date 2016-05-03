import TCGMain as tc
from modules import pyrand


def runtests():
    rngtest()
    packtest()
    openpacktest('Expert Booster', print_res=True)


def rngtest():
    test_input_list = ('50', '30', '10', '5', '3', '1.5', '.5')
    perfect_results = {x+'%': int(float(x)*100) for x in test_input_list}
    test_input_list = [x+'%' for x in test_input_list]
    test_weight_list = (.5, .3, .1, .05, .03, .015, .005)
    results = {x: 0 for x in test_input_list}
    print('\nTesting 10000 iterations of 1-draw weighted choice rng~~')

    for x in range(10000):
        testresult = pyrand.weightchoice(test_input_list, test_weight_list)
        results[testresult] += 1

    print(results)
    results = {x: 0 for x in test_input_list}
    print('\nTesting 1000 iterations of 10-draw weighted choice rng~~')

    for x in range(1000):
        testresults = pyrand.weightchoice(test_input_list, test_weight_list, 10)
        for result in testresults:
            results[result] += 1

    print(results)
    results = {x: 0 for x in test_input_list}
    print('\nTesting 100 iterations of 100-draw weighted choice rng~~')

    for test in range(100):
        testresults = pyrand.weightchoice(test_input_list, test_weight_list, 100)
        for result in testresults:
            results[result] += 1

    print(results)
    print('\nPerfect results~~')
    print(perfect_results)
    test_input_list = [x+1 for x in range(25)]
    results = {x: 0 for x in test_input_list}
    print('\nTesting 100 iterations of 100-draw non-weighted 1-25 randint() choice rng~~')

    for test in range(100):
        testresults = pyrand.randint(1, 25, 100)
        for result in testresults:
            results[result] += 1

    print(results)


def packtest():
    print('Opening packs')
    print('Testing opening packs. Opening 10 rounds of packs.\n')

    for pack in tc.packs.values():
        print(pack.pack_name, pack.card_amount, pack.theme_card_chance, pack.max_themed)
        for x in range(10):
            print('\tPack', x+1, end='\n\t\t')
            cards = pack.open_pack()
            for card in cards:
                print(card.card_tier, card.card_name, end=', ')
            print()


def strtest():
    print('Generating 10 random strings with a length of 15 characters')

    for x in range(15):
        print(pyrand.randstring(15))


def openpacktest(pack_name, pack_amt=25, print_res=False):
    try:
        pack = tc.packs[pack_name]
    except:
        raise ValueError('Invalid pack name: {0}'.format(pack_name))
    tca = pack_amt*pack.card_amount
    card_list = []
    tcc = 0

    for x in range(pack_amt):
        card_list.extend(pack.open_pack())

    for card in card_list:
        if card.card_theme == pack.extra_theme:
            tcc += 1

    del card_list
    tccp = round(tcc/tca*100, 4)
    if print_res:
        print(tcc, 'out of', tca, 'cards were themed giving a total of', tccp, '% themed cards')
        print('optimal themed cards is', tca*pack.theme_card_chance)

    return tcc, tccp

if __name__ == '__main__':
    runtests()
