import TradingCards as tc

def test_packs():
    for pack in tc.packs.values():
        cards = pack.openPack()
        for card in cards:
            print('{} from {}'.format(card.cardName, pack.packName))


if __name__ == '__main__':
    test_packs()
