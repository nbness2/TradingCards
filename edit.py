from os import listdir

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

            for idx, cName in enumerate(cardNames, start = 1):

                if idx < len(cardNames):
                    cNameFile.write(cName+'\n')

                else:
                    cNameFile.write(cName)