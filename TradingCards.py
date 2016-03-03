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
            cardNameList = [x.strip() for x in cardNames.readlines()]
        return tuple(cardNameList)

    def readTierNames(self):
        with open('themes/{0}/tnames.txt'.format(self.themeName), 'r') as tierNames:
            tierNameList = [x.strip() for x in tierNames.readlines()]
        return tuple(tierNameList)

    def readTierChances(self):
        with open('themes/{0}/tchances.txt'.format(self.themeName), 'r') as tierChances:
            tierChanceList = [float(x) for x in tierChances.readlines()]
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
    def __init__(self, packName):
        self.packName = packName
        self.packPrice, self.cardAmt, self.themeCardChance, self.maxThemed = self.readConfigs()
        self.basicChances = self.readBasicChances()
        self.basicTheme, self.extraTheme = self.readThemes()

    def openPack(self):
        cardList = []
        themeCt = 0
        for x in range(self.cardAmt):
            if rand.random() <= self.themeCardChance and themeCt < self.maxThemed:
                cardList.append(Theme(self.extraTheme).makeCard())
                themeCt += 1
            else:
                cardList.append(Theme(self.basicTheme).makeCard())
        return tuple(cardList)

    def readConfigs(self):
        #[packPrice, packCardAmt, themeCardChance, maxThemeCards]
        configs = []
        with open('packs/{0}/pconfigs.txt'.format(self.packName), 'r') as configFile:
            for config in configFile:
                config = config.strip()
                try:
                    configs.append(int(config))
                except ValueError:
                    configs.append(float(config))
        return configs

    def readBasicChances(self):
        bclist = []
        with open('packs/{0}/basicChances.txt'.format(self.packName), 'r') as bcFile:
            for bc in bcFile.readlines():
                bclist.append(float(bc.strip()))
        return tuple(bclist)

    def readThemes(self):
        with open('packs/{0}/themes.txt'.format(self.packName), 'r') as themeFile:
            themeList = [theme.strip() for theme in themeFile]
        return tuple(themeList)


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
                tierChance = float(inpConf('Rarity for tier: {0} . {1:.3f} remaining chance. '.format(tierName, 100-usedChance*100)))/100
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
            if idx < len(cardNames)-1:
                cNameFile.write(str(cName)+'\n')
            else:
                cNameFile.write(str(cName))
    with open(fileDir+'tnames.txt', 'w') as tNameFile:
        for idx, tName in enumerate(tierNames):
            if idx < len(tierNames)-1:
                tNameFile.write(str(tName)+'\n')
            else:
                tNameFile.write(str(tName))
    with open(fileDir+'tchances.txt', 'w') as tChanceFile:
        for idx, tChance in enumerate(tierChances):
            if idx < len(tierChances)-1:
                tChanceFile.write(str(tChance)+'\n')
            else:
                tChanceFile.write(str(tChance))
            

def editTheme():
    isTheme = False
    themeList = listdir('themes')
    editThemeName = inpConf('{0}\nInput the name of the theme you are editing: '.format(themeList))c cv

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
            tierChance = float(inpConf('Rarity for {0} tier: {1} . {2:.2f} remaining chance. '.format(baseTheme, tierName, 100-usedChance*100)))/100
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

def readThemes():
    themes = {themeName : Theme(themeName) for themeName in listdir('themes')}
    return themes

def readPacks():
    packs = {packName : Pack(packName) for packName in listdir('packs')}
    return packs

themes = readThemes()

packs = readPacks()
