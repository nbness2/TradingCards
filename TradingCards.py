from os import listdir
import pyrand

try:
    from time import perf_counter as pc

except ImportError:
    from time import clock as pc

except:
    raise ImportError('Failed to import perf_counter and clock from time module')

pc()



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

        tier = pyrand.weightchoice(self.themeTiers, self.themeTierChances)
        return tier


    def pickName(self):

        name = pyrand.weightchoice(self.themeCardNames)
        return name


    def makeCards(self, cardAmt = 1):

        cardList = []

        for x in range(cardAmt):
            cardList.append(Card(self.pickName(), self.pickTier(), self.themeName))

        return tuple(cardList)


    def __bool__(self):

        return True




class Pack:
    """
    Base class for all packs
    These are values that are assumed to be correct to work correctly
    packPrice = int (0->X)
    cardsInPack = int (1->X)
    cardTierChances = None/tuple (lowest rarity -> highest rarity)(add up to 1)
    ~corresponds to the basic theme, set to 0 for no chance of that tier
    themeCardChance = None/int (0->1) - chance to replace 1 card in your pack with a themed card
    packTheme = None/Theme (this is an extra theme in addition to the default basic theme)
    """

    global themes

    def __init__(self, packName):
        self.packName = packName
        self.basicTheme, self.extraTheme = self.readThemes()
        self.packPrice, self.cardAmt, self.themeCardChance, self.maxThemed = self.readConfigs()
        self.basicChances = self.readBasicChances()


    def openPack(self):
        packCards = []
        packCards.extend(themes[self.basicTheme].makeCards(self.cardAmt))

        for x in range(self.maxThemed):

            rand = pyrand.randint()/100

            if rand <= self.themeCardChance:
                packCards[pyrand.randint(0, len(packCards)-1)] = themes[self.extraTheme].makeCards()[0]

        return tuple(packCards)


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
        confinp = input('Confirm "{0}" Y/N: '.format(reply))[0].lower()

        if confinp == 'n':
            conf = False

        elif confinp == 'y':
            return str(reply)

        else:
            print('Invalid input: {0} . Please try again'.format(reply))


def readPacks():
    return {packName : Pack(packName) for packName in listdir('packs')}

def readThemes():
    return {themeName : Theme(themeName) for themeName in listdir('themes')}

def readTP():
    return readThemes(), readPacks()

themes, packs = readTP()
