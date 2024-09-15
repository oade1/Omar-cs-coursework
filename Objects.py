import pygame,Game, random,Enemy,Functions, Tiles, os, csv
from Settings import *

class Pathway(pygame.sprite.Sprite):

    def __init__(self, pos, type, pathwayWidth, pathwayHeight, game=Game.Game, z=LAYERS['PATHWAY'], TileSize=32, spriteSheetWidthRange=(20, 22), spriteSheetHeightRange=(0, 2)):
        super().__init__(game.GetAllSpriteGroup())

        self.spritesheet = pygame.image.load('TileMaps\OutsideTransparent.png').convert_alpha()
        self.tile_size = TileSize
        self.z = z
        self.position = Functions.getPosToGrid(game,pos)
        self.sprite_sheet_width = self.spritesheet.get_width() // self.tile_size

        # get the list of tiles to work with
        self.tiles_to_work_with = []
        for i in range(spriteSheetWidthRange[0], spriteSheetWidthRange[1] + 1):
            for ii in range(spriteSheetHeightRange[0], spriteSheetHeightRange[1] + 1):
                self.tiles_to_work_with.append(ii * self.sprite_sheet_width + i)
        self.tiles_to_work_with = sorted(self.tiles_to_work_with)
        
        # make the surface
        self.surface = pygame.Surface((pathwayWidth * TileSize, pathwayHeight * TileSize), pygame.SRCALPHA)
        self.blit_tiles(pathwayWidth, pathwayHeight, TileSize)

        self.image = self.surface
        self.rect = self.image.get_rect(topleft=self.position)

    def blit_tiles(self, pathwayWidth, pathwayHeight, tileSize):
        for y in range(pathwayHeight):
            for x in range(pathwayWidth):
                if x == 0 and y == 0:
                    tile_index = 0
                elif x == pathwayWidth - 1 and y == 0:
                    tile_index = 2
                elif x == 0 and y == pathwayHeight - 1:
                    tile_index = 6
                elif x == pathwayWidth - 1 and y == pathwayHeight - 1:
                    tile_index = 8
                elif x == 0:
                    tile_index = 3
                elif x == pathwayWidth - 1:
                    tile_index = 5
                elif y == 0:
                    tile_index = 1
                elif y == pathwayHeight - 1:
                    tile_index = 7
                else:
                    tile_index = 4

                tile_index = min(tile_index, len(self.tiles_to_work_with) - 1)
                tile_id = self.tiles_to_work_with[tile_index]

                tile_x = (tile_id % self.sprite_sheet_width) * tileSize
                tile_y = (tile_id // self.sprite_sheet_width) * tileSize

                self.surface.blit(self.spritesheet, (x * tileSize, y * tileSize), (tile_x, tile_y, tileSize, tileSize))

class EnemyRing(pygame.sprite.Sprite):
    def __init__(self,pos, ringWidth, ringHeight, game=Game.Game, hasGate = True, gateWidth = 10,spriteSheetWidthRange = (0,3),spriteSheetHeightRange = (0,7),tileSize = 32,z= LAYERS['ENEMYRING']):
        self.spritesheet = pygame.image.load('TileMaps/OutsideTransparent.png').convert_alpha()
        self.tileSize = tileSize
        self.z = z
        self.position = pos
        self.position = Functions.getPosToGrid(game, pos)
        self.game = game
        self.SpriteSheetWidth = self.spritesheet.get_width() / self.tileSize
        self.hasGate = hasGate
        self.gateWidth = gateWidth

        #collisionRectanglesToAdd
        self.CollisionRects = [CollisionRect]

        #get the list of tiles to work with
        self.tiles_to_work_with = []
        for i in range(spriteSheetWidthRange[0], spriteSheetWidthRange[1] + 1):
            for ii in range(spriteSheetHeightRange[0], spriteSheetHeightRange[1] + 1):
                self.tiles_to_work_with.append(ii * self.SpriteSheetWidth + i)
        self.tiles_to_work_with = sorted(self.tiles_to_work_with)
        print(self.tiles_to_work_with)

        
        #make the surface
        self.surface = pygame.surface.Surface((ringWidth * self.tileSize, ringHeight * self.tileSize), pygame.SRCALPHA)
        self.blit_tiles(ringWidth, ringHeight, tileSize)

        self.image = self.surface
        self.rect = self.image.get_rect(topleft=pos)

        super().__init__(game.GetAllSpriteGroup())


    def blit_tiles(self, ringWidth, ringHeight, tileSize):

        for x in range(ringWidth):
            for y in range(ringHeight):
                if x == 0 and y == 0: # top left
                    tile_index = 26 # correct
                elif x == ringWidth - 1 and y == 0: # top right
                    tile_index = 27 # correct
                elif x == 0 and y == ringHeight - 1: # bottom left
                    tile_index = 30 # correct
                elif x == ringWidth - 1 and y == ringHeight - 1: # bottom right
                    tile_index = 31 # corret
                elif x == 0:
                    tile_index = 7
                elif x == ringWidth - 1:
                    tile_index = 7
                elif y == 0:
                    tile_index = 13
                elif y == ringHeight - 1:
                    tile_index = 13
                else:
                    continue
                
                if self.hasGate:
                    if y == ringHeight - 1:
                        if x > round(ringWidth/2) and x < round(ringWidth/2) + round(self.gateWidth/2):
                            continue
                        elif x < round(ringWidth/2) and x > round(ringWidth/2) - round(self.gateWidth/2):
                            continue
                        elif x == round(ringWidth/2):
                            continue
                        elif x == round(ringWidth/2) + round(self.gateWidth/2):
                            tile_index = 12
                        elif x == round(ringWidth/2) - round(self.gateWidth/2):
                            tile_index = 14





                tile_index = min(tile_index, len(self.tiles_to_work_with) - 1)
                tile_id = self.tiles_to_work_with[tile_index]

                tile_x = (tile_id % self.SpriteSheetWidth) * tileSize
                tile_y = (tile_id // self.SpriteSheetWidth) * tileSize

                collideRect = pygame.rect.Rect(self.position.x +( x * tileSize), self.position.y +(y * tileSize), tileSize, tileSize)
                instanceCollisionrect = CollisionRect(collideRect, self)
                
                self.CollisionRects.append(instanceCollisionrect)


                self.surface.blit(self.spritesheet, (x * tileSize, y * tileSize), (tile_x, tile_y, tileSize, tileSize))

    def delete(self):
        for collideRect in self.CollisionRects:
            self.game.GetCollideGroup().remove(collideRect)
            collideRect.kill()

class CollisionRect(pygame.sprite.Sprite):
    def __init__(self,rect,enemyRing=EnemyRing,z = LAYERS['ENEMYRING']):
        self.enemyRing = enemyRing
        self.image = None
        self.z = z 

        self.CollideRect = rect  

        game = self.enemyRing.game     

        super().__init__(enemyRing.game.GetCollideGroup())
        return


class SkeletonSpawner:
    def __init__(self, width, height, amountOfSkelies,  game=Game.Game):
        self.game = game

        self.numOfEnemies = amountOfSkelies
        self.WidthOfSpawner = width
        self.HeightOfSpawner = height


        works = False
        
        xWidth = 50 * self.game.tileSize
        yHeight = 50 * self.game.tileSize
        posTopLeftX = 0
        posTopLeftY = 0
        while works == False:
            posTopLeftX = random.randint(0,int(self.game.mapWidth * self.game.tileSize))
            posTopLeftY = random.randint(int(self.game.mapHeight * self.game.tileSize) - (self.game.mapHeightIncreaseOnLevel * self.game.tileSize),int(self.game.mapHeight * self.game.tileSize))


            
            if posTopLeftX + xWidth < (self.game.mapWidth * self.game.tileSize) and posTopLeftY + yHeight < (self.game.mapHeight * self.game.tileSize):
                works = True
            for topleftOfOtherSpawner in self.game.getSpawnersVectors():
                spawnerX = topleftOfOtherSpawner.x
                spawnerY = topleftOfOtherSpawner.y
                if abs(spawnerX - posTopLeftX) < xWidth and abs(spawnerY - posTopLeftY) < yHeight:
                    works = False

        
        posVector = pygame.math.Vector2(posTopLeftX, posTopLeftY)
        posVector = Functions.getPosToGrid(game, posVector)
        
        self.posVector = posVector
        self.game.addSpawnerVecotr(posVector)

        self.enemyRing = EnemyRing(posVector, width, height, game)

        print("pos of enemy ring")
        print(posVector)

        #calculating top right of path
        pathwayWidth = self.enemyRing.gateWidth #has to be even

        midOfPath = width/2 - ((pathwayWidth/2) - 1)# to account for gate width 
        posPath = pygame.math.Vector2(posTopLeftX,posTopLeftY)
        posPath.y += height * self.game.tileSize 
        posPath.x += midOfPath * self.game.tileSize
        posPath.y -= (3) * self.game.tileSize 
        self.pathway = Pathway(posPath, "BRICKS", pathwayWidth, 10, game)
        
        self.offsetForSkeletons = 10

        for i in range(amountOfSkelies):
            posX = random.randint(posTopLeftX + (self.offsetForSkeletons * self.game.tileSize), posTopLeftX + (width  * self.game.tileSize) - (self.offsetForSkeletons * self.game.tileSize))
            posY = random.randint(posTopLeftY + (self.offsetForSkeletons * self.game.tileSize), posTopLeftY + (height * self.game.tileSize) - (self.offsetForSkeletons * self.game.tileSize))
            posSkelyVec = pygame.math.Vector2(posX, posY)
            posSkelyVec = Functions.getPosToGrid(game, posSkelyVec)
            print(posVector)
            print(posSkelyVec)
            Enemy.SpawnerSkeleton(posSkelyVec, game, self)

        #generate a few campfires for the player to heal in the spawner
        
        for i in range(random.randint(1,amountOfSkelies)):
            posX = random.randint(posTopLeftX + (self.offsetForSkeletons * self.game.tileSize), posTopLeftX + (width  * self.game.tileSize) - (self.offsetForSkeletons * self.game.tileSize))
            posY = random.randint(posTopLeftY + (self.offsetForSkeletons * self.game.tileSize), posTopLeftY + (height * self.game.tileSize) - (self.offsetForSkeletons * self.game.tileSize))
            posCampVec = pygame.math.Vector2(posX, posY)
            posCampVec = Functions.getPosToGrid(game, posCampVec)
            Tiles.CampFire(posCampVec, game, game.GetAllSpriteGroup())

        #self.pathway.rect.center = self.enemyRing.rect.midbottom

        game.addSpawner(self)
        print(self.game.GetEnemies())
    
class CustomSpawnerCollisionRect(pygame.sprite.Sprite):
    def __init__(self,rect,game=Game.Game,z = LAYERS['ENEMYRING']):
        self.image = None
        self.z = z 

        self.CollideRect = rect 
        super().__init__(game.GetCollideGroup())


class CustomSpawnerSurface(pygame.sprite.Sprite):
    def __init__(self, pos, image, game=Game.Game, z = LAYERS['ENEMYRING']):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        super().__init__(game.GetAllSpriteGroup())

class CustomSpawner:
    def __init__(self, csvFile,game=Game.Game, Position = pygame.Vector2, csvNumberForSpawner='-2', typeOfEnemy=ENEMYTYPES['1'],numOfEnemies = 50, tileSize=32):
        self.csvFile = csvFile
        self.position = Position
        self.posVector = Position
        game.addSpawnerVecotr(self.position)
        self.game = game
        self.tileSize = tileSize
        self.EnemySpawnPointNumberInCSV = csvNumberForSpawner

        self.numOfEnemies = numOfEnemies #numofenemies has to be the name of the variable that holds the amount of enemies spawneed for any spawners
        self.typeOfEnemy = typeOfEnemy
        
        self.csvFileLoaded = self.loadCSV()

        self.EnemySpawnPoints = [pygame.math.Vector2]
        self.EnemiesSpawned = False

        self.MainSurface = pygame.surface.Surface((len(self.csvFileLoaded) * tileSize,len(self.csvFileLoaded[0])  * tileSize)).convert_alpha()

        self.WidthOfSpawner = len(self.csvFileLoaded)
        self.HeightOfSpawner = len(self.csvFileLoaded[0])

        self.centerpos = pygame.Vector2(self.position.x + self.WidthOfSpawner/2, self.position.y + self.HeightOfSpawner/2)

        self.TilesToWorkWith = game.getTilesToWorkWith()
        self.loadMainSurface()

        # print(self.EnemySpawnPoints)
        self.customSpawnerSurface = CustomSpawnerSurface(Position, self.MainSurface, game)

        self.game.addSpawner(spawner=self)
        self.game.addUpdateFunc(self.update)

        self.detectionX = 1280
        self.detectionY = 1280

        self.player = self.game.GetPlayer()

    def update(self):
        if abs(self.player.position.x - self.centerpos.x) < self.detectionX and abs(self.player.position.y - self.centerpos.y) < self.detectionY:
            if not self.EnemiesSpawned:
                self.SpawnEnemies()
                self.game.removeUpdateFunc(self.update)
                self.EnemiesSpawned = True
                print("Player in range, spawn enemies called")
    def SpawnEnemies(self):
        UsedSpawnPoints = [pygame.math.Vector2]
        print("spawning enemies for a custom spawner")
        for i in range(self.numOfEnemies):
            if len(UsedSpawnPoints) >= len(self.EnemySpawnPoints) - 1: 
                print("UsedSpawnPointsCleared")
                UsedSpawnPoints = [pygame.math.Vector2]
            Position = None
            PositionChosen = False
            while not PositionChosen:
                Position = random.choice(self.EnemySpawnPoints)
                if Position not in UsedSpawnPoints:
                    UsedSpawnPoints.append(Position)
                    PositionChosen = True
            # if Position.x == None: 
            #     print("Position set incorrectly")
            #     continue
            print("printing position next:")
            print(Position)
            x = (Position.x * 32) + self.position.x
            y = (Position.y * 32) + self.position.y
            Position = pygame.Vector2(x,y)

            if self.typeOfEnemy == ENEMYTYPES['1']: # SKEELTON
                Enemy.SpawnerSkeleton(Position, self.game, self)
                print(Position)
                print("spawner skeleton spawned")
        

        print("Spawning enemies for a custom spawner finished")



    def loadCSV(self):
        maplist = []
        with open(os.path.join(self.csvFile)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                maplist.append(list(row))
        return maplist

    def loadMainSurface(self):
        x = 0
        y = 0
        
        for row in self.csvFileLoaded:
            x = 0
            for column in row:
                if column == self.EnemySpawnPointNumberInCSV:
                    self.EnemySpawnPoints.append(pygame.Vector2(x,y))
                    x += 1
                    continue
                if column != '-1':
                    self.MainSurface.blit(self.TilesToWorkWith[column], (x * self.tileSize,y * self.tileSize))
                    CustomSpawnerCollisionRect(pygame.rect.Rect(self.position.x + (x * self.tileSize), self.position.y + (y * self.tileSize), self.tileSize, self.tileSize), self.game)
                    self.MainSurface.set_colorkey((0,0,0))
                x += 1 
            y += 1