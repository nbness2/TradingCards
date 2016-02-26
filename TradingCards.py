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
        self.cardName = cardName
        self.cardTier = cardTier
        self.cardTheme = cardTheme

class Theme:
    '''
    themeName = str
    themeCardNames = tuple (pool of theme-specific card names)
    themeTiers = tuple (pool of theme-specific card tiers)
    themeTierChances = tuple (chances for the corresponding theme tier)
    ~(should be same length as themeTiers)
    '''
    def __init__(self, themeName):
        self.themeName = themeName
        self.themeCardNames = tuple(self.readCardNames())
        self.themeTiers = tuple(self.readTierNames())
        self.themeTierChances = tuple(self.readTierChances())

    def readCardNames(self):
        with open('themes/{0}/cnames.txt'.format(self.themeName), 'r') as cardNames:
            cardNameList = [x[:-1] for x in cardNames.readlines()]
            return cardNameList

    def readTierNames(self):
        with open('themes/{0}/tnames.txt'.format(self.themeName), 'r') as tierNames:
            tierNameList = [x[:-1] for x in tierNames.readlines()]
            return tierNameList

    def readTierChances(self):
        with open('themes/{0}/tchances.txt'.format(self.themeName), 'r') as tierChances:
            tierChanceList = [float(x[:-1]) for x in tierChances.readlines()]
            return tierChanceList

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

def createTheme():
    response = ' '
    cardNames = []
    tierNames = []
    cardName = ''
    tierName = ''
    tierChances = []
    tierChance = 0
    breakLoop = False
    usedChance = 0
    themeName = inpConf('Input theme name: ')
    while not breakLoop:
        cardName = inpConf('Input card name (-- to exit): ')
        if cardName == '--':
            breakLoop = True
        else:
            cardNames.append(cardName)
    breakLoop = False
    while not breakLoop:
        tierName = inpConf('Input Tier name (-- to exit): ')
        if tierName == '--':
            breakLoop = True
        else:
            tierNames.append(tierName)       
    breakLoop = False
    while not breakLoop:
        tierChances = []
        for x in tierNames:
            try:
                tierChance = int(inpConf('Rarity for tier: {0} . {1:.3f} remaining chance. '.format(x, 100-usedChance*100)))/100
                usedChance += tierChance
                tierChances.append(tierChance)
                if usedChance > 1:
                    print('Cannot use over 100 chance!')
                    break
            except:
                print('Invalid value: {0}'.format(x))
                break
        if len(tierNames) == len(tierChances):
            breakLoop = True
    fileDir = 'themes/'+themeName+'/'
    if not exists(fileDir):
        makedir(fileDir)
    with open(fileDir+'cnames.txt', 'w') as cNameFile:
        for idx, cName in enumerate(cardNames):
            if len(cardNames)-1 != idx:
                cNameFile.write(cName+'\n')
            else:
                cNameFile.write(cName)

    with open(fileDir+'tnames.txt', 'w') as tNameFile:
        for idx, tName in enumerate(tierNames):
            if len(tierNames)-1 != idx:
                tNameFile.write(tName+'\n')
            else:
                tNameFile.write(tName)

    with open(fileDir+'tchances.txt', 'w') as tChanceFile:
        for idx, tChance in enumerate(tierChances):
            if len(tierChances)-1 != idx:
                tChanceFile.write(str(tChance)+'\n')
            else:
                tChanceFile.write(str(tChance))

def editTheme():
    pass

def createPack():
    pass

themes = {}

'''packs = {'Beginner Pack':Pack(250, 7, basicCardChances = (.65, .15, .10, .05, .04, .01, 0)),
         'Intermediate Pack':Pack(500, 7, basicCardChances = (.65, .13, .12, .05, .035, .01, .005)),
         'Expert Pack':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01)),
         'Quacker Packer':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01), packTheme = 'theme_ducky', themeCardChance = .05)
        }'''
