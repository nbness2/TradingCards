
class Card:
    '''Base class for all cards'''
    def __init__(self, cardName, cardTier, cardTheme):
        '''cardName = str, cardTier = int, cardTheme = Theme'''
        self._cardName = cardName
        self._cardTier = cardTier
        self._cardTheme = cardTheme
        

class Pack:
    '''Base class for all packs'''
    def __init__(self, packPrice, cardsInPack, cardTierChances, themeCardChance, packTheme):
        '''packPrice = int (0->inf), cardsInPack = int (1->inf), cardTierChances = tuple (lowest rarity -> highest rarity) (must add up to 100), themeCardChance = int (1->100), packTheme = Theme'''
        self._price = packPrice
        self._cardsInPack = cardsInPack
        self._tierChances = cardTierChances
        self._themeChance = themeCardChance # This chance is PER CARD not PER PACK. It will replace a card in the pack, not add a card to the pack.
        self._packTheme = packTheme

    def openPack(self):
        '''"Buys" and opens a pack of cards'''
        pass

class Theme:
    '''Base class for all themes'''
    def __init__(self, themeName, themeTiers, themeTierChances):
        '''themeName = str, themeTiers = tuple (lowest rarity -> highest rarity) (must add to 100), themeTierChances = tuple'''
        self._themeName = themeName
        self._themeTiers = themeTiers
        self._themeTierChances = themeTierChances
