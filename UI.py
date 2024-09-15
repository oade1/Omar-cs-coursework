import pygame


class button():
    def __init__(self, x, y, image, text, font, Screen):
        self.X = x
        self.Y = y 
        self.img = image
        self.Font = font
        self.screen = Screen
        self.rect = self.img.get_rect(center=(self.X, self.Y))
        self.txt = text
        self.text = self.Font.render(self.txt, True, "white")
        self.tect_rect = self.text.get_rect(center=(self.X,self.Y))

    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.screen.blit(self.text, self.tect_rect)

    def CheckHover(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.Font.render(self.txt, True, "grey")
        else:
            self.text = self.Font.render(self.txt, True, "white")

    def CheckClick(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True

    def getText(self): return self.txt
    def setText(self, newText):
        self.txt = newText
        self.text = self.Font.render(self.txt, True, "white")

class ShopButton(button):
    def __init__(self, Position,Text, Font):
        screen = pygame.display.get_surface()
        super().__init__(Position.x, Position.y, pygame.transform.scale_by(pygame.image.load(r"Shop\GenericButton.png").convert_alpha(),3), Text,Font, screen)
        self.buttonImagePressed = pygame.transform.scale_by(pygame.image.load(r"Shop\GenericButtonPressed.png").convert_alpha(),3)
        self.buttonImageHover = pygame.transform.scale_by(pygame.image.load(r"Shop\GenericButtonActive.png").convert_alpha(),3)
        self.CurrentButtonImage = self.img
        self.IsHover = False
        self.IsClicked = False

        self.ClickDuration = 50
        self.ClickDurationTime = 0


    def draw(self,MousePos):
        self.CheckHover(MousePos)

        if self.IsHover: self.CurrentButtonImage = self.buttonImageHover
        if self.IsClicked: self.CurrentButtonImage = self.buttonImagePressed
        if not self.IsHover and not self.CheckClick(MousePos): self.CurrentButtonImage = self.img

        self.screen.blit(self.CurrentButtonImage, self.rect)
        self.screen.blit(self.text, self.tect_rect)

        if self.IsClicked and pygame.time.get_ticks() > self.ClickDurationTime: self.IsClicked = False

    def CheckHover(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.IsHover = True
        else:
            self.IsHover = False

class TextField:
    def __init__(self, x,y, image, text,font=pygame.font.Font, colour=pygame.color.Color((255,0,0))):  
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.TextString = text
        self.font = font
        self.text = self.font.render(self.TextString, True,colour)
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

        self.screen = pygame.display.get_surface()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

#no clue where I was going with this but we move on
class ShopUI(TextField):
    def __init__(self,TEXT,Position=pygame.Vector2, Image=pygame.image,font=pygame.font.Font,Colour=pygame.color.Color((255,0,0))):
        super().__init__(Position.x, Position.y, Image, TEXT,font, Colour)

class DamageShopUi(ShopUI):
    def __init__(self,game,Position=pygame.Vector2, colour=pygame.Color):
        #create text field
        self.game = game
        self.colour = colour
        self.foozleFont = pygame.font.Font(r"Font\FOOZLE.ttf", 20)
        text = "Damage:" + str(game.PriceForDamage)  
        image = pygame.image.load(r"Shop\GenericTextField.png").convert_alpha()
        image = pygame.transform.scale_by(image, 3)
        super().__init__(text,Position,image, self.foozleFont, colour)

        #create button to buy
        ButtonText = "BUY"

        xOffset = 10
        ButtonPosition = pygame.math.Vector2((Position.x + image.get_width() + xOffset), Position.y)
        self.foozleFont = pygame.font.Font('Font\FOOZLE.TTF', 27)
        self.ShopButton = ShopButton(ButtonPosition, ButtonText, self.foozleFont)

    def UpdatePrice(self):
        text = "Damage:" + str(self.game.PriceForDamage)  
        self.text = self.font.render(text, True,self.colour)


    def draw(self, MousePos):
        self.ShopButton.draw(MousePos)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

class HealthShopUi(ShopUI):
    def __init__(self,game,Position=pygame.Vector2, colour=pygame.Color):
        #create text field
        self.game = game
        self.colour = colour
        self.foozleFont = pygame.font.Font(r"Font\FOOZLE.ttf", 20)
        text = "Health:" + str(game.PriceForHealth)  
        image = pygame.image.load(r"Shop\GenericTextField.png").convert_alpha()
        image = pygame.transform.scale_by(image, 3)
        super().__init__(text,Position,image, self.foozleFont, colour)

        #create button to buy
        ButtonText = "BUY"

        xOffset = 10
        ButtonPosition = pygame.math.Vector2((Position.x + image.get_width() + xOffset), Position.y)
        self.foozleFont = pygame.font.Font('Font\FOOZLE.TTF', 27)
        self.ShopButton = ShopButton(ButtonPosition, ButtonText, self.foozleFont)

    def UpdatePrice(self):
        text = "Health:" + str(self.game.PriceForHealth)  
        self.text = self.font.render(text, True,self.colour)


    def draw(self, MousePos):
        self.ShopButton.draw(MousePos)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

class SpeedShopUi(ShopUI):
    def __init__(self,game,Position=pygame.Vector2, colour=pygame.Color):
        #create text field
        self.game = game
        self.colour = colour
        self.foozleFont = pygame.font.Font(r"Font\FOOZLE.ttf", 20)
        text = "Speed:" + str(game.PriceForSpeed)  
        image = pygame.image.load(r"Shop\GenericTextField.png").convert_alpha()
        image = pygame.transform.scale_by(image, 3)
        super().__init__(text,Position,image, self.foozleFont, colour)

        #create button to buy
        ButtonText = "BUY"

        xOffset = 10
        ButtonPosition = pygame.math.Vector2((Position.x + image.get_width() + xOffset), Position.y)
        self.foozleFont = pygame.font.Font('Font\FOOZLE.TTF', 27)
        self.ShopButton = ShopButton(ButtonPosition, ButtonText, self.foozleFont)

    def UpdatePrice(self):
        text = "Speed:" + str(self.game.PriceForSpeed)  
        self.text = self.font.render(text, True,self.colour)



    def draw(self, MousePos):
        self.ShopButton.draw(MousePos)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)
















class Alert():
    def __init__(self, text, time):
        self.text = text
        self.lifespan = time
        