import pygame

pygame.init()
clock = pygame.time.Clock()
crashed = False
img = pygame.image

colors = {'black' : (0,0,0), 'white' : (255,255,255), 'red' : (255,0,0), 'green' : (0,255,0), 'blue' : (0,0,255),
          'purple' : (255,0,255), 'yellow' : (255,255,0)}

disWidth = 1000
disHeight = 750
gameDis = pygame.display.set_mode((disWidth, disHeight))
pygame.display.set_caption('TCGui')


class Button:

    def __init__(self, buttonColor, sizeX, sizeY, posX, posY, text = '', font = 'freesansbold.ttf', fontColor = 'black'):
        self.text = text
        self.buttonColor = buttonColor
        self.sizeX, self.sizeY = sizeX, sizeY
        self.posX, self.posY = posX, posY
        self.font = font
        self.fontColor = fontColor

    def draw(self):
        # x, y, width, height
        textX = self.posX+(self.sizeX/2)
        textY = self.posY+(self.sizeY/2)
        textSize = self.sizeX / 5.3
        pygame.draw.rect(gameDis, colors[self.buttonColor], (self.posX, self.posY, self.sizeX, self.sizeY))
        dispText(self.text, textX, textY, self.font, textSize, colors[self.fontColor])

class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, imgName, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.load(str(imgName))
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
testSprite = ImageSprite('assets/cards/BasicCard.png', 300, 300)


def dispText(msg, textX, textY, font = 'freesansbold.ttf', fontSize = 20, textColor = (0,0,0), bgColor = None):
    msgFont = pygame.font.Font(str(font), int(fontSize))
    textSurface = msgFont.render(msg, True, textColor, bgColor)
    textRect = textSurface.get_rect()
    textRect.center = (textX, textY)
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
    dispText('Message', 300, 300,'freesansbold.ttf', 80, colors['blue'], colors['yellow'])
    testButton.draw()
    testSprite.draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
