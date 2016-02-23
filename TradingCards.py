
class Card:
    '''
       Base class for all cards
       These are values that are assumed to be correct to work correctly
       cardName = str
       cardTier = int
       cardTheme = Theme
    '''
    def __init__(self, cardName, cardTier, cardTheme):
        self._cardName = cardName
        self._cardTier = cardTier
        self._cardTheme = cardTheme
        

class Pack:
    '''
       Base class for all packs
       These are values that are assumed to be correct to work correctly
       packPrice = int (0->inf), cardsInPack = int (1->inf)
       cardTierChances = tuple (lowest rarity -> highest rarity)(add up to 100)
       themeCardChance = int (1->100)
       packTheme = Theme
    '''
    def __init__(self, packPrice, cardsInPack, cardTierChances, themeCardChance, packTheme):
        self._price = packPrice
        self._cardsInPack = cardsInPack
        self._tierChances = cardTierChances
        self._themeChance = themeCardChance # This chance is PER CARD.
        self._packTheme = packTheme

    def openPack(self):
        '''
           Generates the cards in the pack.
        '''
        pass

class Theme:
    '''
       Base class for all themes
       These are values that are assumed to be correct to work correctly
       themeName = str
       themeTiers = tuple (lowest rarity -> highest rarity)
       themeTierChances = tuple (should add up to 100)
    '''
    def __init__(self, themeName, themeTiers, themeTierChances):
        self._themeName = themeName
        self._themeTiers = themeTiers
        self._themeTierChances = themeTierChances
