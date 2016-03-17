from os.path import exists
from os import makedirs

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

        for idx, cName in enumerate(cardNames, start = 1):

            if idx < len(cardNames):
                cNameFile.write(str(cName)+'\n')

            else:
                cNameFile.write(str(cName))

    with open(fileDir+'tnames.txt', 'w') as tNameFile:

        for idx, tName in enumerate(tierNames, start = 1):

            if idx < len(tierNames):
                tNameFile.write(str(tName)+'\n')

            else:
                tNameFile.write(str(tName))

    with open(fileDir+'tchances.txt', 'w') as tChanceFile:

        for idx, tChance in enumerate(tierChances, start = 1):

            if idx < len(tierChances):
                tChanceFile.write(str(tChance)+'\n')

            else:
                tChanceFile.write(str(tChance))


def createPack():

    baseTheme = 'Basic'
    baseThemeTiers = Theme(baseTheme).themeTiers
    baseThemeChances = []
    themeCardChance = 0
    maxThemeCards = 0
    usedChance = 0
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

    extraTheme = inpConf('Exact name of extra theme (-- for none): ')

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

        for idx, bChance in enumerate(baseThemeChances, start = 1):

            if idx < len(baseThemeChances):
                basicChanceFile.write(str(bChance)+'\n')

            else:
                basicChanceFile.write(str(bChance))

    with open(fileDir+'pconfigs.txt', 'w') as pConfigFile:
        pconfigs = [packPrice, packCardAmt, themeCardChance, maxThemeCards]

        for idx, config in enumerate(pconfigs, start = 1):

            if idx < len(pconfigs):
                pConfigFile.write(str(config)+'\n')

            else:
                pConfigFile.write(str(config))