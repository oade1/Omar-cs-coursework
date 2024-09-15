import Tiles
from Tiles import *


def createFireCamp(position,game):
    Tiles.CampFire(position, game, game.GetAllSpriteGroup())
    #print("create fire camp called")



def createMapDictionary(mapTileWidth, mapTileHeight,tilesize, defaultTileID):
    tileMap = {}

    for y in range(0, mapTileHeight):
        y = y * tilesize

        for x in range(0, mapTileWidth):
            x = x * tilesize
            tileMap[(x,y)] = defaultTileID

    
    print(tileMap)
    return tileMap

def getPosToGrid(game ,pos=pygame.Vector2):
    x = round(pos.x / game.tileSize) * game.tileSize
    y = round(pos.y / game.tileSize) * game.tileSize
    return pygame.math.Vector2(x,y)

def getGridLoc(game, pos=pygame.Vector2):
    x = round(pos.x/game.tileSize)
    y = round(pos.y/game.tileSize)
    return pygame.Vector2(x,y)