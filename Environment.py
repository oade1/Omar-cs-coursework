import pygame, Tiles


class EnvironmentGroup(pygame.sprite.Group):
    def __init__(self, dictionaryOfTiles, MapManager=map):
        super().__init__()
        self.maplist = dictionaryOfTiles
        self.screen = pygame.display.get_surface()
        self.map = map


    def drawTiles(self):


        x = 0
        y = 0
        for row in self.maplist:
            x = 0
            for num in row:
                try :
                    if num != "-1":
                        self.screen.blit(self.map.TilesToWorkWith[num], ((x * self.map.tw) - self.map.tw, (y * self.map.th)- self.map.th)) 
                        coord = (str(x),str(y))
                        self.map.tiles[coord] = num

                    print(str(num))
                except: 
                    if num != "-1":print("Value " + str(num) + " is not in dictionary")
            y = y + 1
            print("this is y: " + str(y))



