import pygame
from Settings import *

class LightManager:
    def __init__(self, game):
        self.lights = []
        self.game = game

    def createLightSource(self, Position, Radius, Intensity):
        lightSource = LightSource(Position, Radius, Intensity)
        self.lights.append(lightSource)
        self.game.GetAllSpriteGroup().add(lightSource)

    def destroyLightSource(self, lightSource):
        if lightSource in self.lights:
            self.lights.remove(lightSource)
            if lightSource in self.game.GetAllSpriteGroup(): self.game.GetAllSpriteGroup().remove(lightSource)
        else:
            print(f"{lightSource} is not in lights. ignored")

    def handleLight(self):
        pass

class LightSource(pygame.sprite.Sprite):
    def __init__(self, position, radius, intensity):
        super().__init__()
        self.position = position
        self.radius = radius
        self.intensity = intensity # it is a decimal percentage (0 to 1 is 0% to 100%)
        self.image = pygame.surface.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self._createLightImage()


    def _createLightImage(self):
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                pixelPosition = pygame.Vector2(x - self.radius, y - self.radius).length()
                if pixelPosition <= self.radius:
                    alpha = max(0, int((1 - (pixelPosition / self.radius)) * 255 * self.intensity))
                    self.image.set_at((x, y), (255,255,255,alpha))

class CameraGroup(pygame.sprite.Group):
    def __init__(self, lightManager=LightManager):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.halfWidth = self.screen.get_width()/2
        self.halfHeight = self.screen.get_height()/2

        self.offset = pygame.math.Vector2()

        #zoom
        self.zoomScale = 3
        self.internalSurfaceSize = (self.screen.get_width() // self.zoomScale,self.screen.get_height() // self.zoomScale)
        self.internalSurface = pygame.Surface(self.internalSurfaceSize, pygame.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center=(self.halfWidth, self.halfHeight))
        self.internalSurfaceSizeVector = pygame.math.Vector2(self.internalSurfaceSize)
        self.internalOffset = pygame.math.Vector2()
        self.internalOffset.x = self.internalSurfaceSize[0] // 2 - self.halfWidth
        self.internalOffset.y = self.internalSurfaceSize[1] // 2 - self.halfHeight

        #lighting
        self.lightManager = lightManager

    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.halfWidth 
        self.offset.y = player.rect.centery - self.halfHeight

        self.internalSurface.fill('black')

        for layer in LAYERS.values():
            if layer == LAYERS['BACKGROUND']:
                offset = -self.offset + self.internalOffset
                self.internalSurface.blit(player.getGame().defaultTileSurface,offset)
                continue


            for sprite in self.sprites():
                
                if sprite.z == layer:
                    # if sprite.z == LAYERS['PARTICLES']:
                    #     offset = sprite.position - self.offset
                    #     self.screen.blit(sprite.image, offset)
                    #     continue
                    if sprite.z == LAYERS['TILES']:
                        continue
                    offset = sprite.rect.topleft - self.offset + self.internalOffset
                    self.internalSurface.blit(sprite.image, offset)
                    #region Draw player hitbox
                    if layer == LAYERS['PLAYER']:
                        collideRectOffest = sprite.CollideRect.topleft - self.offset + self.internalOffset
                        rect = pygame.rect.Rect(collideRectOffest.x  
                                                , collideRectOffest.y
                                                , sprite.CollideRect.width, sprite.CollideRect.height)
                        # pygame.draw.rect(self.internalSurface, (255,0,0,5), rect)
                    if layer == LAYERS['ENEMY']:
                        sprite.drawHealthBar(offset, self.internalSurface)
                        collideRectOffest = sprite.CollideRect.topleft - self.offset + self.internalOffset
                        rect = pygame.rect.Rect(collideRectOffest.x  
                                                , collideRectOffest.y
                                                , sprite.CollideRect.width, sprite.CollideRect.height)
                        # pygame.draw.rect(self.internalSurface, (255,0,0,5), rect)

                    #endregion
        scaledSurface = pygame.transform.scale(self.internalSurface, self.internalSurfaceSizeVector * self.zoomScale)
        scaledRect = scaledSurface.get_rect(center=(self.halfWidth, self.halfHeight))
        self.screen.blit(scaledSurface, (scaledRect.x, scaledRect.y), scaledRect)


        
class EnvironmentGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

        #camera values
        self.offset = pygame.math.Vector2(0,0)
        self.screen = pygame.display.get_surface()

        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2
        print(str(self.half_w))
        print(str(self.half_h))



    def centerCamera(self, target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h 
        #print("offset is:" + str(self.offset))


    def drawBackground(self, target):
        self.centerCamera(target)
        for sprite in self.sprites():
            #if sprite == Obstacle:
            #    self.drawObstacles(sprite)
            #   return
            offset = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset)
class PlayerEnvironment(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.screen = pygame.display.get_surface()
        self.player = None
    #offset
        self.offset = pygame.math.Vector2(0,0)
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

    def centerCamera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h 
        #print("offset is:" + str(self.offset))


    def draw(self, target):
        for sprite in self.sprites():
            self.offset.x = self.player.rect.centerx - self.half_w 
            self.offset.y = self.player.rect.centery - self.half_h 
            offset = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset)
            centeroffset = target.CenterRect.topleft - self.offset
            collideRectOffest = target.CollideRect.topleft - self.offset
            rect = pygame.rect.Rect(collideRectOffest.x  
                                    , collideRectOffest.y
                                    , target.CollideRect.width, target.CollideRect.height)
            pygame.draw.rect(self.screen, ("red"), rect, 0)
            pygame.draw.circle(self.screen, ("blue"), centeroffset, 10)           
            pygame.draw.circle(self.screen, ("yellow"), self.offset, 3)
class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.screen = pygame.display.get_surface()
    #offset
        self.offset = pygame.math.Vector2(0,0)
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

    def centerCamera(self, target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h 

    def draw(self, target):
        self.centerCamera(target)
        for sprite in self.sprites():
            offset = sprite.rect.topleft - self.offset
            offset.x -= (sprite.image.get_width()//4)
            offset.y -= (sprite.image.get_height()//4)
            
            self.screen.blit(sprite.image, offset)
    
    def update(self):
        for enemy in self.sprites():
            enemy.update()
class ObstacleGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

        #camera values
        self.offset = pygame.math.Vector2(0,0)
        self.screen = pygame.display.get_surface()

        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2
        print(str(self.half_w))
        print(str(self.half_h))



    def centerCamera(self, target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h 
        #print("offset is:" + str(self.offset))


    def drawBackground(self, target):
        self.centerCamera(target)
        for sprite in self.sprites():
            offset = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset)

            colliderectOffset = sprite.collideRect.topleft - self.offset
            pygame.draw.rect(self.screen, ("blue"), sprite.collideRect)
            