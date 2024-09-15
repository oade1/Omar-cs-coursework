import pygame
from Settings import *


class cameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2




    def customDraw(self, player):
        self.offset.x = player.rect.centerx - self.half_w 
        self.offset.y = player.rect.centery - self.half_h 

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if layer == sprite.z:
                    offset_rect = sprite.rect.copy()
                    offset_rect -=  self.offset
                    self.screen.blit(sprite.image, offset_rect)
