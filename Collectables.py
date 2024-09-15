import pygame
from Functions import getPosToGrid
from Settings import *
class AnimatedCollectable(pygame.sprite.Sprite):
    def __init__(self,game, Position=pygame.math.Vector2, ListOfSurface=[], z = LAYERS['COLLECTABLE']):
        super().__init__(game.GetAllSpriteGroup())
        self.game = game
        self.AnimationList = ListOfSurface
        self.image = self.AnimationList[0]
        self.z = z
        position = getPosToGrid(game, Position)
        self.rect = self.image.get_rect(topleft=position)
        #animation
        self.animationFrame = 0
        
        self.animationCooldown = 120
        self.AnimationTime = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() > self.AnimationTime:
            self.AnimationTime += self.animationCooldown

            self.animationFrame += 1
            if self.animationFrame >= len(self.AnimationList): self.animationFrame = 0

            self.image = self.AnimationList[self.animationFrame]

        self.CheckCollision()

    def CheckCollision(self):
        pass

class SmallHealthPoition(AnimatedCollectable):
    def __init__(self,Position, game):
        self.Position = getPosToGrid(game, Position)
        self.game = game
        self.CreationTime = pygame.time.get_ticks()
        self.SpriteSheet = pygame.image.load("Collectables/SmallHealthPotion.png").convert_alpha()
        
        self.tileSize = self.SpriteSheet.get_height()
        self.AnimationFrames = int(self.SpriteSheet.get_width() / self.tileSize)
        
        ListOfSurface = []
        for i in range(self.AnimationFrames - 1):
            surface = pygame.surface.Surface((self.tileSize, self.tileSize)).convert_alpha()
            surface.blit(self.SpriteSheet, (0,0), (i*self.tileSize, 0, self.tileSize, self.tileSize))
            surface = pygame.transform.scale_by(surface, 3).convert_alpha()
            surface.set_colorkey((255,0,255))
            ListOfSurface.append(surface)

        super().__init__(game, self.Position, ListOfSurface)
        self.CollideRect = self.rect.copy().inflate(self.rect.width * -0.3, self.rect.height * -0.2)
    def CheckCollision(self):
        if pygame.time.get_ticks() > self.CreationTime + 1000:
            if self.CollideRect.colliderect(self.game.GetPlayer().CollideRect):
                self.game.GetPlayer().heal(20)
                self.kill()
class BigHealthPoition(AnimatedCollectable):
    def __init__(self,Position, game):
        self.Position = getPosToGrid(game, Position)
        self.game = game
        self.CreationTime = pygame.time.get_ticks()
        self.SpriteSheet = pygame.image.load("Collectables/BigHealthPotion.png").convert_alpha()
        
        self.tileSize = self.SpriteSheet.get_height()
        self.AnimationFrames = int(self.SpriteSheet.get_width() / self.tileSize)
        
        ListOfSurface = []
        for i in range(self.AnimationFrames - 1):
            surface = pygame.surface.Surface((self.tileSize, self.tileSize)).convert_alpha()
            surface.blit(self.SpriteSheet, (0,0), (i*self.tileSize, 0, self.tileSize, self.tileSize))
            surface = pygame.transform.scale_by(surface, 3).convert_alpha()
            surface.set_colorkey((255,0,255))
            ListOfSurface.append(surface)

        super().__init__(game, self.Position, ListOfSurface)
        self.CollideRect = self.rect.copy().inflate(self.rect.width * -0.3, self.rect.height * -0.2)
    def CheckCollision(self):
        if pygame.time.get_ticks() > self.CreationTime + 1000:
            if self.CollideRect.colliderect(self.game.GetPlayer().CollideRect):
                self.game.GetPlayer().heal(100)
                self.kill()