import time
time.clock()
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
        tier = weightchoice(self.themeTiers, self.themeTierChances)
        return tier

    def pickName(self):
        name = weightchoice(self.themeCardNames)
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
            if randint(100) <= self.themeCardChance*100 and themeCt < self.maxThemed:
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
    themeStr = ', '.join(themeList)[0:]
    usedChance = 0
    validChoice = False
    while not isTheme:
        themeName = inpConf('{0}\nInput the exact name of the theme you are editing: '.format(themeStr))
        if themeName in themeList:
            isTheme = True
        else:
            print('Invalid theme:', themeName)
    fileDir = 'themes/'+themeName+'/'
    with open(fileDir+'cnames.txt', 'r') as cNameFile:
        cardNames =  [name.strip() for name in cNameFile.readlines()]
    cardNamesL = [name.lower() for name in cardNames]
    while True:
        cardNamesL = [name.lower() for name in cardNames]
        cardNameStr = ', '.join(cardNames)
        validChoice = False
        cardChoice = inpConf('(E)diting, (A)dding, or (D)eleting a card name (-- to quit): ').lower()
        if cardChoice[0] == 'e':
            print(cardNameStr)
            nameChoice = inpConf('Which name are you editing: ')
            validChoice = True
        elif cardChoice[0] == 'a':
            nameChoice = inpConf('Which name are you adding: ')
            validChoice = True
        elif cardChoice[0] == 'd':
            print(cardNameStr)
            nameChoice = inpConf('Which name are you deleting: ')
            validChoice = True
        elif cardChoice == '--':
            validChoice = False
            break
        else:
            validChoice = False
        if validChoice:
            if cardChoice == 'a':
                if not nameChoice.lower() in cardNamesL:
                    cardNames.append(nameChoice)
                else:
                    print('Card name already exists!')
            elif nameChoice.lower() in cardNamesL:
                nameIndex = cardNamesL.index(nameChoice.lower())
                if cardChoice == 'e':
                    cardNames[nameIndex] = inpConf('Input card name: ')
                elif cardChoice == 'd':
                    del cardNames[nameIndex]
                else:
                    print('editTheme error', cardNames, nameChoice)
            else:
                print('Name',nameChoice,'not found.')
        else:
            print('Invalid input:', cardChoice)

        with open(fileDir+'cnames.txt', 'w') as cNameFile:
            for idx, cName in enumerate(cardNames):
                if idx < len(cardNames)-1:
                    cNameFile.write(cName+'\n')
                else:
                    cNameFile.write(cName)

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

def randint(maxInt):

    global seedTime
    
    seed = int(seedTime * (2**30)-time.clock()+.1+.1+.1)

    seedMask = int(time.clock() * (2**30)-time.clock()+.1+.1+.1)

    seedTime =  time.clock() - (seedTimeMod*1*time.clock())
    
    return range(int(maxInt))[(seed^seedMask)%maxInt]

def weightchoice(inputList, weightList = None, maxPrecision = 3):

    global seedTime

    seed = int(seedTime * (2**30)+.1+.1+.1)

    if weightList == None:
        weightList = [1/len(inputList) for x in inputList]
    
    if not len(inputList) == len(weightList):
        raise ValueError('The length of input list ({0}) and weight list ({1}) must be equal'.format(len(inputList),
                                                                                                     len(weightList)))
    if not round(sum(weightList), maxPrecision) == 1:
        print(round(sum(weightList),maxPrecision))
        raise ValueError('The sum of all weights ({0}) must equal 1'.format(sum(weightList)))

    popList = []
    
    for inp, weight in zip(inputList, weightList):
        for i in range(int(weight*(10**maxPrecision))):
            popList.append(inp)

    seedOffset = int(time.clock()*512-time.clock()+.1+.1+.1)

    seedTime =  time.clock() - (seedTimeMod*1*time.clock())

    #return popList[randInt(len(popList))]
    
    return popList[~(seed^seedOffset)%len(popList)]

    

def readThemes():
    themes = {themeName : Theme(themeName) for themeName in listdir('themes')}
    return themes

def readPacks():
    packs = {packName : Pack(packName) for packName in listdir('packs')}
    return packs

themes = readThemes()

packs = readPacks()

seedTime = time.clock()
seedTimeMod = time.clock()*16

testInputList = ['50%','30%','10%','5%','3%','1.5%','.5%']
testWeightList = [.5,.3,.1,.05,.03,.015,.005]

results = {x:0 for x in testInputList}
results2 = {x:0 for x in testInputList}
