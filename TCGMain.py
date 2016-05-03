from os import listdir, path
from modules import pyrand


class Card:
    '''
    Base class for all cards
    These are values that are assumed to be correct to work correctly
    card_name = str
    card_tier = int
    card_theme = Theme
    '''

    def __init__(self, card_name, card_tier, card_theme):
        self.card_name = card_name
        self.card_tier = card_tier
        self.card_theme = card_theme


class Theme:
    '''
    theme_name = str
    theme_card_names = tuple (pool of theme-specific card names)
    theme_tiers = tuple (pool of theme-specific card tiers)
    theme_tier_chances = tuple (chances for the corresponding theme tier)
    ~(should be same length as theme_tiers)
    '''

    def __init__(self, theme_name):
        self.theme_name = theme_name
        self.theme_card_names = self.readcardnames()
        self.theme_tiers = self.readtiernames()
        self.theme_tier_chances = self.readtierchances()

    def readcardnames(self):
        with open('assets/themes/{0}/cnames.txt'.format(self.theme_name), 'r') as cnfile:
            cardnames = [x.strip() for x in cnfile.readlines()]

        return tuple(cardnames)

    def readtiernames(self):
        with open('assets/themes/{0}/tnames.txt'.format(self.theme_name), 'r') as tnfile:
            tiernames = [x.strip() for x in tnfile.readlines()]

        return tuple(tiernames)

    def readtierchances(self):
        with open('assets/themes/{0}/tchances.txt'.format(self.theme_name), 'r') as tcfile:
            tierchances = [float(x) for x in tcfile.readlines()]

        return tuple(tierchances)

    def pick_tier(self):
        tier = pyrand.weightchoice(self.theme_tiers, self.theme_tier_chances)
        return tier

    def pick_name(self):
        name = pyrand.weightchoice(self.theme_card_names)
        return name

    def make_cards(self, card_amount=1):

        card_list = []

        for x in range(card_amount):
            card_list.append(Card(self.pick_name(), self.pick_tier(), self.theme_name))

        return tuple(card_list)

    def __bool__(self):

        return True


class Pack:
    """
    Base class for all packs
    These are values that are assumed to be correct to work correctly
    pack_price = int (0->X)
    cardsInPack = int (1->X)
    card_tier_chances = None/tuple (lowest rarity -> highest rarity)(add up to 1)
    ~corresponds to the basic theme, set to 0 for no chance of that tier
    theme_card_chance = None/int (0->1) - chance to replace 1 card in your pack with a themed card
    packTheme = None/Theme (this is an extra theme in addition to the default basic theme)
    """

    global themes

    def __init__(self, pack_name):
        self.pack_name = pack_name
        self.base_theme, self.extra_theme = self.readthemes()
        self.pack_price, self.card_amount, self.theme_card_chance, self.max_themed = self.readconfigs()
        self.basicChances = self.rbchances()

    def open_pack(self):
        pack_cards = []
        pack_cards.extend(themes[self.base_theme].make_cards(self.card_amount))

        for x in range(self.max_themed):

            rand = pyrand.randint()/175

            if rand <= self.theme_card_chance*1.4:
                pack_cards[pyrand.randint(0, len(pack_cards)-1)] = themes[self.extra_theme].make_cards()[0]

        return tuple(pack_cards)

    def readconfigs(self):
        #[pack_price, packCardAmt, theme_card_chance, maxThemeCards]
        configs = []

        with open('assets/packs/{0}/pconfigs.txt'.format(self.pack_name), 'r') as cfile:

            for config in cfile:
                config = config.strip()

                try:
                    configs.append(int(config))

                except ValueError:
                    configs.append(float(config))

        return configs

    def rbchances(self):
        bclist = []
        with open('assets/packs/{0}/basicChances.txt'.format(self.pack_name), 'r') as bcfile:

            for bc in bcfile.readlines():
                bclist.append(float(bc.strip()))

        return tuple(bclist)

    def readthemes(self):
        with open('assets/packs/{0}/themes.txt'.format(self.pack_name), 'r') as tfile:
            tlist = [theme.strip() for theme in tfile]

        return tuple(tlist)


def input_confirm(inpstr):
    conf = False
    while not conf:
        reply = input(inpstr)
        confirmed = input('Confirm "{0}" Y/N: '.format(reply))[0].lower()
        if confirmed == 'n':
            conf = False
        elif confirmed == 'y':
            return str(reply)
        else:
            print('Invalid input: {0} . Please try again'.format(reply))


def read_packs():
    return {pack_name: Pack(pack_name) for pack_name in listdir('assets/packs/')}


def read_themes():
    return {theme_name: Theme(theme_name) for theme_name in listdir('assets/themes/')}


def read_themes_packs():
    return read_themes(), read_packs()

themes, packs = read_themes_packs()
