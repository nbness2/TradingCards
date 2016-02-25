import numpy.random as rand
from os.path import isdir, exists
from os import makedirs as makedir

class Card:
    '''
    Base class for all cards
    These are values that are assumed to be correct to work correctly
    cardName = str
    cardTier = int
    cardTheme = Theme
    '''

    def __init__(self, cardName, cardTier, cardTheme):
        self.dprint()
        self.cardName = cardName
        self.cardTier = cardTier
        self.cardTheme = cardTheme.themeName


class Pack:
    '''
    Base class for all packs
    These are values that are assumed to be correct to work correctly
    packPrice = int (0->X)
    cardsInPack = int (1->X)
    cardTierChances = None/tuple (lowest rarity -> highest rarity)(add up to 1)
    ~corresponds to the basic theme, set to 0 for no chance of that tier
    themeCardChance = None/int (0->1)
    packTheme = None/Theme (this is an extra theme in addition to the default basic theme)
    '''
    def __init__(self, packPrice, cardsInPack, basicCardChances = None, packTheme = None, themeCardChance = None, maxThemed = 1):
        self.price = packPrice
        self.cardsInPack = cardsInPack
        self.basicChances = basicCardChances if basicCardChances else themes['theme_basic'].themeTierChances
        self.themeChance = themeCardChance if (packTheme and themeCardChance) else 0 # This chance is PER CARD
        self.packTheme = themes[packTheme if packTheme else 'theme_basic']
        self.maxThemed = maxThemed

    def openPack(self):
        themect = 0
        cardlist = []
        for x in range(self.cardsInPack):
            if rand.random() <= self.themeChance and themect <= self.maxThemed:
                cardlist.append(self.packTheme.makeCard())
                themect += 1
            else:
                cardlist.append(themes['theme_basic'].makeCard())
        return cardlist

class Theme:
    '''
    themeName = str
    themeCardNames = tuple (pool of theme-specific card names)
    themeTiers = tuple (pool of theme-specific card tiers)
    themeTierChances = tuple (chances for the corresponding theme tier)
    ~(should be same length as themeTiers)
    '''
    def __init__(self, themeName, themeCardNames, themeTiers, themeTierChances):
        #self.themeCardNames = self.getCardNames()
        self.themeCardNames = themeCardNames
        self.themeName = themeName
        self.themeTiers = themeTiers
        self.themeTierChances = themeTierChances

    '''def getCardNames(self):
        with open('names/{0}.txt'.format(self.themeName), 'r') as cardNames:
            return cardNames.readlines()
    '''

    def pickTier(self):
        tier = rand.choice(self.themeTiers, 1, p=self.themeTierChances)[0]
        return tier

    def pickName(self):
        name = rand.choice(self.themeCardNames)
        return name

    def makeCard(self):
        return Card(self.pickName(), self.pickTier(), self.themeName)

    def __bool__(self):
        return True

def buyPack(packname):
    for x in packs[packname].openPack():
        print(x.cardTier, x.cardName)

def inpConf(inpstr):
    conf = False
    while not conf:
        reply = input(inpstr)
        confinp= input('Confirm "{0}" Y/N: '.format(reply))[0].lower()
        if confinp == 'n':
            conf = False
        elif confinp == 'y':
            return str(reply)
        else:
            print('Invalid input: {0} . Please try again'.format(reply))

def editTheme():
    pass
            if len(tierNames) == len(tierChances):

with open('names.txt', 'r') as nameFile:
    cardnames = tuple([x[:-1] for x in nameFile.readlines()])

themes = {'theme_basic' : Theme('Basic', cardnames, ('Black', 'Green', 'Yellow', 'Blue', 'Purple', 'Red', 'White'), (.55, .15, .12, .08, .05, .03, .02)),
          'theme_ducky' : Theme('Ducky', ('Bill', 'George', 'Deborah', 'Sneaker', 'Oppenheimer', 'Jill', 'Squilliam'), ('Quacky', 'Quackier', 'Quackiest'), (.75,.20,.05))}

packs = {'Beginner Pack':Pack(250, 7, basicCardChances = (.65, .15, .10, .05, .04, .01, 0)),
         'Intermediate Pack':Pack(500, 7, basicCardChances = (.65, .13, .12, .05, .035, .01, .005)),
         'Expert Pack':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01)),
         'Quacker Packer':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01), packTheme = 'theme_ducky', themeCardChance = .05)
        }
