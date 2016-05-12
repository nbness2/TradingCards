import pygame

pygame.init()
clock = pygame.time.Clock()
crashed = False
img = pygame.image

colors = {'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
          'purple': (255, 0, 255), 'yellow': (255, 255, 0)}

disWidth = 1000
disHeight = 750
gameDis = pygame.display.set_mode((disWidth, disHeight))
pygame.display.set_caption('TCGui')


class Button:

    def __init__(self, button_color, sizex, sizey, posx, posy, text='', font='freesansbold.ttf', font_color='black'):
        self.text = text
        self.button_color = button_color
        self.sizex, self.sizey = sizex, sizey
        self.posx, self.posy = posx, posy
        self.font = font
        self.font_color = font_color

    def draw(self):
        # x, y, width, height
        textx = self.posx+(self.sizex/2)
        texty = self.posy+(self.sizey/2)
        textsize = self.sizex / 5.3
        pygame.draw.rect(gameDis, colors[self.button_color], (self.posx, self.posy, self.sizex, self.sizey))
        display_text(self.text, textx, texty, self.font, textsize, colors[self.font_color])


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.load(str(image_name))
        self.x = int(x)
        self.y = int(y)

    def draw(self):
        gameDis.blit(self.image, (self.x, self.y))

    def move(self, x, y):
        self.x += int(x)
        self.y += -int(y)

    def rotate(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)

testButton = Button('green', 200, 50, 300, 300, 'testButton')
testSprite = ImageSprite('assets/cardimg/BasicCard.png', 300, 300)


def display_text(msg, textx, texty, font='freesansbold.ttf', font_size=20, text_color=(0, 0, 0), background_color=None):
    msgFont = pygame.font.Font(str(font), int(font_size))
    textSurface = msgFont.render(msg, True, text_color, background_color)
    textRect = textSurface.get_rect()
    textRect.center = (textx, texty)
    gameDis.blit(textSurface, textRect)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                testSprite.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                testSprite.move(1, 0)
            if event.key == pygame.K_UP:
                testSprite.move(0, 1)
            elif event.key == pygame.K_DOWN:
                testSprite.move(0, -1)
            if event.key == pygame.K_1:
                testSprite.rotate(45)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                pass
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                pass
    gameDis.fill(colors['white'])
    display_text('Message', 300, 300,'freesansbold.ttf', 80, colors['blue'], colors['yellow'])
    testButton.draw()
    testSprite.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
