import numpy.random as rand
from os.path import exists
from os import makedirs, listdir

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
        self.themeCardNames = self.readCardNames()
        self.themeTiers = self.readTierNames()
        self.themeTierChances = self.readTierChances()

    def readCardNames(self):
        with open('themes/{0}/cnames.txt'.format(self.themeName), 'r') as cardNames:
            cardNameList = [x[:-1] for x in cardNames.readlines()]
        return tuple(cardNameList)

    def readTierNames(self):
        with open('themes/{0}/tnames.txt'.format(self.themeName), 'r') as tierNames:
            tierNameList = [x[:-1] for x in tierNames.readlines()]
        return tuple(tierNameList)

    def readTierChances(self):
        with open('themes/{0}/tchances.txt'.format(self.themeName), 'r') as tierChances:
            tierChanceList = [float(x[:-1]) for x in tierChances.readlines()]
        return tuple(tierChanceList)

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

    def getConfigs(self):
        #[packPrice, packCardAmt, themeCardChance, maxThemeCards]
        with open('packs/{0}/pconfigs', 'w') as meow:
            pass


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
    cardNames = []
    tierNames = []
    cardName = ''
    tierName = ''
    tierChances = []
    tierChance = 0
    breakLoop = False
    usedChance = 0
    themeName = inpConf('Input Theme name: ')
    fileDir = 'themes/'+themeName+'/'
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
        for tierName in tierNames:
            try:
                tierChance = int(inpConf('Rarity for tier: {0} . {1:.3f} remaining chance. '.format(tierName, 100-usedChance*100)))/100
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
    if not exists(fileDir):
        makedirs(fileDir)
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
    baseTheme = 'Basic'
    baseThemeTiers = Theme(baseTheme).themeTiers
    baseThemeChances = []
    themeCardChance = 0
    maxThemeCards = 0
    usedChance = 0
    packCardAmt = 0
    packPrice = 0
    breakLoop = False
    packName = inpConf('Input Pack name: ')
    packPrice = int(inpConf('Input Pack price: '))
    packCardAmt = int(inpConf('Input amout of cards in this Pack: '))
    fileDir = 'packs/'+packName+'/'
    while not breakLoop:
        for tierName in baseThemeTiers:
            tierChance = int(inpConf('Rarity for {0} tier: {1} . {2:.2f} remaining chance. '.format(baseTheme, tierName, 100-usedChance*100)))/100
            usedChance += tierChance
            baseThemeChances.append(tierChance)
            if usedChance > 1:
                print('Cannot use over 100 chance!')
                break
        if len(baseThemeTiers) == len(baseThemeChances):
            breakLoop = True
    extraTheme = inpConf('Name of extra theme (-- for none): ')
    if extraTheme == '--':
        extraTheme == None
    else:
        themeCardChance = int(inpConf('Input theme card chance: '))/100
        maxThemeCards = int(inpConf('Input max theme cards per pack: '))

    if not exists(fileDir):
        makedirs(fileDir)
    with open(fileDir+'themes.txt', 'w') as themeNames:
        themeNames.write(baseTheme+'\n')
        themeNames.write(extraTheme)
    with open(fileDir+'basicChances.txt', 'w') as basicChanceFile:
        for idx, bChance in enumerate(baseThemeChances):
            if len(baseThemeChances)-1 != idx:
                basicChanceFile.write(str(bChance)+'\n')
            else:
                basicChanceFile.write(str(bChance))
    with open(fileDir+'pconfigs.txt', 'w') as pConfigFile:
        pconfigs = [packPrice, packCardAmt, themeCardChance, maxThemeCards]
        for idx, config in enumerate(pconfigs):
            if len(pconfigs)-1 != idx:
                pConfigFile.write(str(config)+'\n')
            else:
                pConfigFile.write(str(config))

'''packs = {'Beginner Pack':Pack(250, 7, basicCardChances = (.65, .15, .10, .05, .04, .01, 0)),
         'Intermediate Pack':Pack(500, 7, basicCardChances = (.65, .13, .12, .05, .035, .01, .005)),
         'Expert Pack':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01)),
         'Quacker Packer':Pack(1000, 7, basicCardChances = (.60, .15, .10, .07, .04, .03, .01), packTheme = 'theme_ducky', themeCardChance = .05)
        }'''
