import os,csv, pygame, Enemy, random, Game, Functions
from Settings import *
from Objects import *


class MapManager():
    def __init__(self, csvFile, SpriteSheet, TileWidth, TileHeight, game=Game.Game):
        self.csv = csvFile
        self.ss = SpriteSheet
        self.tw = TileWidth
        self.th = TileHeight
        self.TilesToWorkWith = {}
        self.tiles = {}
        self.Layers = {}
        self.maplist = self.loadCSV()
        print("code:001")
        self.loadTileSprites(self.ss,int(self.ss.get_width()/TileWidth),int(self.ss.get_height()/TileHeight))

        self.game=game

        self.TileIDToAddCollidersTo = [] #[0,1,2,3,40,41,41,43,51,80,81,82,83,120,121,122,123,160,161,162,163,200,201,202,203,240,241,242,243,280,281,282,283]

        for i in range(0,4):
            for ii in range(0,8):
                self.TileIDToAddCollidersTo.append((ii * 40) + i) 
        
    def loadTileSprites(self, ss, PosX, PosY):
        for row in range(0, PosY):
            for sprite in range(0, PosX):
                surface = pygame.Surface((self.tw, self.th)).convert()
                surface.blit(ss,(0,0), ((sprite * self.tw), (row * self.th), self.tw, self.th))
                surface.set_colorkey((0,0,0))
                self.TilesToWorkWith[str(((row*PosX) + sprite))] = surface
                #print(str((row + sprite)))

        #print(str(self.TilesToWorkWith))

        
    def loadCSV(self):
        maplist = []
        with open(os.path.join(self.csv)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                maplist.append(list(row))
        #print(str(maplist))
        return maplist
    
    #region
    # def loadMap(self):
    #     x = 0
    #     y = 0
    #     for row in self.maplist:
    #         x = 0
    #         for num in row:
    #             try :
    #                 if num != "-1":
    #                     print(num)
    #                     if num in self.TileIDToAddCollidersTo == False:
    #                         Tile(self.TilesToWorkWith[num], ((x * self.tw) - self.tw, (y * self.th)- self.th), self.game.GetAllSpriteGroup())
    #                     else:
    #                         tile = Tile(self.TilesToWorkWith[num], ((x * self.tw) - self.tw, (y * self.th)- self.th), self.game.GetAllSpriteGroup())

    #                     coord = (str(x),str(y))
    #                     self.tiles[coord] = num

    #             except: 
    #                 if num != "-1":print("Value" + str(num) + " is not in dictionary")
            
            
            
    #             x = x + 1

    #         y = y + 1
    #endregion

    def loadMap(self, howFarDownToDraw, howFarAcrossToDraw):
        x = 0
        y = 0

        counterForCollidableTiles = 0

        listOfSeenTileIDs = []
        

        for row in self.maplist:
            x = 0
            for num in row:
                try :
                    if num != "-1" and num != "66" and num != "46":
                        #print("x is: " + str(howFarAcrossToDraw + (x * self.tw) - self.tw))
                        #print("x is: " + str(howFarAcrossToDraw + (x * self.tw) - self.tw))
                        tileBlitted = False
                        for id in self.TileIDToAddCollidersTo:
                            if int(num) == int(id):
                                tile = CollidableTile(self.TilesToWorkWith[num], (howFarAcrossToDraw + (x * self.tw) - self.tw, howFarDownToDraw+ (y * self.th)- self.th), self.game.GetAllSpriteGroup(), z=LAYERS['OBSTACLES'])                        
                                self.game.addToCollideGroup(tile)
                                #print("Collision Tile Created") 
                                counterForCollidableTiles += 1            
                                tileBlitted = True
                        if tileBlitted == False: Tile(self.TilesToWorkWith[num], (howFarAcrossToDraw + (x * self.tw) - self.tw, howFarDownToDraw+ (y * self.th)- self.th), self.game.GetAllSpriteGroup())
                        
                        
                        
                        coord = (str(x),str(y))
                        self.tiles[coord] = num

                except: 
                    if num != "-1":print("Value" + str(num) + " is not in dictionary")
            
            
            
                x = x + 1

            y = y + 1
        print(listOfSeenTileIDs)
        print(counterForCollidableTiles)
        print(self.TileIDToAddCollidersTo)
        self.AddListOfTileIDCollider = []

    def AddTileIDCollider(self, tileid):
        self.TileIDToAddCollidersTo.append(tileid)
    def AddListOfTileIDCollider(self, tileidList):
        for tileid in tileidList:
            self.TileIDToAddCollidersTo.append(tileid)

class mainSurface(pygame.sprite.Sprite):
    def __init__(self, surface,position=pygame.Vector2(0,0), z = LAYERS['COLLECTABLE']):
        self.position = position
        self.z = z

        self.image = surface
        self.rect = self.image.get_rect(topleft=position)

        super().__init__()

class MapManagerTwo:
    def __init__(self, game=Game.Game, collidableLayer=['3', '5','6', '8']):
        self.game = game
        self.tileSize = self.game.tileSize
        self.collidableLayer = collidableLayer

        self.SpriteSheets = {
            'DUNGEON': pygame.image.load('World\WORLD\Dungeon.png'),
            'DESERT': pygame.image.load('World\WORLD\Desert.png'),
            'LAVA': pygame.image.load('World\WORLD\Lava.png'),
            'EXTERIOR': pygame.image.load('World\WORLD\Exterior.png')
        } #this changes to a dictionary with numbers as keys (the numbers are the tile id of that tileset) and the values being a surface of that tile

        self.SpriteSheetsTiles = {}

        self.CSVs = {}

        self.mapWidth = None
        self.mapHeight = None

        self.LoadTiles()
        self.LoadCSVs()

        print(self.CSVs.keys())
        self.CSVs = {i: self.CSVs[i] for i in sorted(self.CSVs, key=int)} #this sorts the keys of the csvs so then I can loop through them easily
        print(self.CSVs.keys())

        self.mainSurface = pygame.surface.Surface((self.mapWidth * self.tileSize, self.mapHeight * self.tileSize), pygame.SRCALPHA).convert_alpha()
        
        print('printing map width and height...')
        print(self.mapWidth, self.mapHeight)

        self.LoadMap()

        self.surfaceObject = mainSurface(self.mainSurface)
        self.game.GetAllSpriteGroup().add(self.surfaceObject)

    def LoadMap(self):

        for key, value in self.CSVs.items(): # key is the first letter and value is the maplist
            tilesToWorkWith = self.SpriteSheetsTiles[CSVMaps[key]]
            print(f'loading map from this spritesheet {CSVMaps[key]}')
            x = 0 
            y = 0

            for row in value:
                x = 0
                for coloum in row:
                    if coloum == '-1': 
                        x += 1
                        continue
                    # print(row, coloum)
                    # print(x,y)
                    self.mainSurface.blit(tilesToWorkWith[int(coloum)], (x * self.tileSize, y * self.tileSize))
                    if self.collidableLayer is not None:
                        if key in self.collidableLayer:
                            CollidableTile(tilesToWorkWith[int(coloum)], (x * self.tileSize, y * self.tileSize), self.game.GetCollideGroup())
                    x += 1
                y += 1
                

    def LoadCSVs(self):
        currentDirectory = os.getcwd()
        directory = os.path.join(currentDirectory, 'World', 'CSV')
        for file in os.listdir(directory):
            mapList = []
            fileDirectory = os.path.join(directory, file)
            with open(fileDirectory) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    mapList.append(list(row))
            self.CSVs[file[0]] = mapList # the first letter of the files is the number in which they are blitted onto the main surface and the same order they are in in tiled
            if self.mapWidth is None: self.mapWidth = len(mapList[0])
            if self.mapHeight is None: self.mapHeight = len(mapList)

    def LoadTiles(self):
        for Name, Spritesheet in self.SpriteSheets.items():
            dic = {}

            SpritesheetWidth = Spritesheet.get_width() / self.tileSize 
            SpritesheetHeight = Spritesheet.get_height() / self.tileSize 
            
            x = 0
            y = 0
            print('loading spritesheet...')
            print(f"Loading tiles from {Name} - width: {SpritesheetWidth}, height: {SpritesheetHeight}")

            for row in range(int(SpritesheetHeight)):
                x = 0
                for coloumb in range(int(SpritesheetWidth)):
                    surface = pygame.Surface((self.tileSize, self.tileSize), pygame.SRCALPHA).convert_alpha()
                    surface.blit(Spritesheet, (0,0), (x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))
                    print(f'Tile x:{x*self.tileSize} and y:{y*self.tileSize} has been loaded with tileID{int((row * SpritesheetWidth) + coloumb)}')

                    # print(str(int((coloumb * SpritesheetWidth) + row))) correct number
                    
                    # print(((coloumb // SpritesheetWidth) * self.tileSize, (coloumb % SpritesheetWidth) * self.tileSize, self.tileSize, self.tileSize)) turns out that (coloumb // SpritesheetWidth) * self.tileSize is always 0

                    dic[int(row*SpritesheetWidth + coloumb)] = surface
                    
                    x += 1
                y += 1

            self.SpriteSheetsTiles[Name] = dic


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos, group, z = LAYERS['TILES'], inheritedTo = None):
        super().__init__(group)
        pygame.sprite.Sprite.__init__(self)
        self.image = image

        if inheritedTo is None: 
            self.rect = self.image.get_rect(center = pos)
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class CollidableTile(Tile):
    def __init__(self,image,pos,group,z = LAYERS['TILES'], inflateBy = None):
        super().__init__(image, pos, group,z, inheritedTo=1)
        self.CollideRect = self.rect.copy()
        if inflateBy is not None: 
            self.CollideRect = self.rect.copy().inflate(inflateBy[0], inflateBy[1])



#region Level creation 
class Level():
    def __init__(self,game=Game.Game, levelNumber=int, ListOfMaps=[], howFarDownToDraw=int, howFarAcrossToDraw=int):
        self.tileSize = 32
        self.game = game
        self.levelNumber = levelNumber
        self.game.SetLevel(self)
        self.mapToLoad = ListOfMaps[0]
        self.map = MapManager(self.mapToLoad,  pygame.image.load('TileMaps\Outside.png'),self.tileSize ,self.tileSize ,game)

        #

        #print(listOfIDsToAddColliderTo)
        #self.map.AddListOfTileIDCollider(listOfIDsToAddColliderTo)

        #self.map.loadMap(howFarDownToDraw, howFarAcrossToDraw)
        self.game.SetLevel(self)

        self.mapLength = game.mapHeight * game.tileSize  
        self.mapWidth = game.mapWidth * game.tileSize 
        
        self.game.GetPlayer().maxx = self.game.mapWidth * self.tileSize

        self.game.HowFarDownIsAMap = levelNumber * self.mapLength
        print("new map starting y: " + str(self.game.HowFarDownIsAMap))
        print("new map starting x: " + str(self.game.HowFarAcrossIsAMap))

        self.game.GetPlayer().maxy = self.game.mapHeight * self.tileSize
        
        self.fullMapLength =  self.mapLength 

        self.Spawners = []
        # for i in range(5):
        #     spawner = CustomSpawner('MapsTiled/custommap02.csv', game, self.getSpawnerPosition(), csvNumberForSpawner='4', numOfEnemies=10)
        #     self.Spawners.append(spawner)

        # self.skeletonSpawners = [SkeletonSpawner]
        # for i in range(10):
        #     skeletonSpawner = SkeletonSpawner(40, 40, 5,game)
        #     self.skeletonSpawners.append(skeletonSpawner)

        #self.SpawnEnemies()
        self.SpawnCampfire(random.randint(150,300))

    def getSpawnerPosition(self):
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
        return pygame.math.Vector2(posTopLeftX, posTopLeftY)

    def SpawnCampfire(self, amountOfCampFire=int):
        print("printing start and end of random location camp fire")
        print(0, self.mapWidth)
        print((self.mapLength*self.levelNumber) -self.mapLength, (self.mapLength*self.levelNumber))
        for i in range(amountOfCampFire):
            x = random.randint(0, self.mapWidth)
            y = random.randint((self.mapLength*self.levelNumber) -self.mapLength, (self.mapLength*self.levelNumber))
            Functions.createFireCamp((x,y), self.game)

    def SpawnEnemies(self):
        numOfEnemies = random.randint(2,5) * self.levelNumber
        print("printing start and end of random location enemies")
        print(0, self.mapWidth)
        print((self.mapLength*self.levelNumber) -self.mapLength, self.mapLength * self.levelNumber)
        for i in range(numOfEnemies):
            # x = random.randint(0, self.mapWidth)
            # y = random.randint((self.mapLength*self.levelNumber) -self.mapLength, self.mapLength * self.levelNumber)
            x = random.randint(2338, 3842)
            y = random.randint(1589 + ((self.mapLength*self.levelNumber) -self.mapLength), self.mapLength * self.levelNumber - (self.mapLength - 2322))

            pos = pygame.math.Vector2(x,y)
            skeleton = Enemy.Skeleton(pos, self.game)
            skeleton.LowerAttackCooldown(skeleton.scalingOnAttackCooldown * self.levelNumber)
        return
class LevelFinished():
    def __init__(self, game=Game.Game):
        self.game = game
        self.game.clearUpdateFunctions()
        self.deleteStuff()
        Level(game, game.currentLevel.levelNumber+ 1, game.listOfMaps, game.HowFarDownIsAMap, game.HowFarAcrossIsAMap )
    def deleteStuff(self):
        pastLevel = self.game.GetLevel()
        self.game.LevelFinished()
        
        del(pastLevel)
        
        typeToDelete = [CollidableTile, Pathway, EnemyRing, CollisionRect, SkeletonSpawner, CustomSpawnerCollisionRect]
        layerToDelete = [LAYERS['OBSTACLES'], LAYERS['ENEMYRING'], LAYERS['PATHWAY']]
        objToDelete = [CustomSpawner, CustomSpawnerSurface]

        for sprite in self.game.GetCollideGroup().sprites():
            if type(sprite) in typeToDelete:
                # self.game.GetCollideGroup().remove(sprite)
                self.game.addToDeletionQueue(sprite)

        for obstacle in self.game.GetAllSpriteGroup().sprites():
            if obstacle.z in layerToDelete or obstacle in objToDelete:
                try:
                    self.game.GetAllSpriteGroup().remove(obstacle)
                except:
                    print("error while deleting obstacles")





class StartLevels():
    def __init__(self, game=Game.Game):
        Level(game, 1, game.listOfMaps, game.HowFarDownIsAMap, game.HowFarAcrossIsAMap)

#endregion

#region Obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, spriteSheet, width, height, fromX, fromY,Collision=bool,game=Game.Game,allSprites=pygame.sprite.Group, z = LAYERS['OBSTACLES']):
        super().__init__(allSprites)
        self.z = z
        self.PixelWidth = width
        self.PixelHeight = height
        self.SpriteSheet = spriteSheet
        self.FromX = fromX
        self.FromY = fromY
        self.doCollision = Collision
        self.game = game
        self.image = self.LoadObstacleImage()
        self.rect = self.image.get_rect(topleft=(0,0))
        self.LoadObstacleImage()

        if self.doCollision: self.game.GetCollideGroup().add(self)

    def LoadObstacleImage(self):
        image = pygame.surface.Surface((self.PixelWidth, self.PixelHeight)).convert()
        image.blit(self.SpriteSheet, (0,0),((self.PixelWidth * self.FromX), (self.PixelHeight * self.FromY),self.PixelWidth, self.PixelHeight))
        image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
        image.set_colorkey((0,0,0))
        return image
class AnimatedObstacle(Obstacle):
    def __init__(self, spriteSheet, width, height, fromX, fromY,Collision=bool,game=Game.Game,allSprites = pygame.sprite.Group, frames=int):
        super().__init__(spriteSheet, width, height, fromX, fromY,Collision,game,allSprites)
        
        self.timeToAnimateAgainst = pygame.time.get_ticks()
        self.animationCooldowm = 200

        self.Frames = frames
        self.AnimationList = self.loadAnimationList()

        self.animationCounter = 0

        #print("Animated obstacle created")
        #print(self.AnimationList)
    
    def update(self):
        if pygame.time.get_ticks() > self.timeToAnimateAgainst:
            self.timeToAnimateAgainst += self.animationCooldowm
            self.animationCounter += 1
            if self.animationCounter >= len(self.AnimationList):
                self.animationCounter = 0
            
            self.image = self.AnimationList[self.animationCounter]

    def loadAnimationList(self):
        list = []
        counter = self.FromX
        for i in range(1, self.Frames+1):
            image = pygame.surface.Surface((self.PixelWidth, self.PixelHeight)).convert()
            image.blit(self.SpriteSheet, (0,0),((self.PixelWidth * counter), (self.PixelHeight * self.FromY),self.PixelWidth, self.PixelHeight))
            image = pygame.transform.scale(image, (image.get_width() * 3, image.get_height() * 3))
            image.set_colorkey((0,0,0))
            list.append(image)
            counter += 1
        
        return list
    
class CampFire(AnimatedObstacle):
    def __init__(self, Position,game,allSprites):
        super().__init__(pygame.image.load('Images\Spritesheets\Obstacles\Resources.png'), 16, 32, 7, 3.5, True, game, allSprites, 4)
        self.rect.topleft = Functions.getPosToGrid(game, pygame.math.Vector2(Position[0], Position[1]))

        self.CollideRect = self.rect.copy().inflate((-self.rect.width *0.2, -self.rect.height * 0.8))
            
#endregion

#region Enemy Spawners
class EnemySpawner():
    def __init__(self, csvFile, SpriteSheet, game=Game.Game,TileSize=32):
        self.csv = csvFile
        self.ss = SpriteSheet
        self.tw = TileSize
        self.th = TileSize
        self.TilesToWorkWith = {}
        self.tiles = {}
        self.Layers = {}
        self.maplist = self.loadCSV()
        print("code:001")
        self.loadTileSprites(self.ss,int(self.ss.get_width()/TileSize),int(self.ss.get_height()/TileSize))

        self.game=game

        self.TileIDToAddCollidersTo = [] #[0,1,2,3,40,41,41,43,51,80,81,82,83,120,121,122,123,160,161,162,163,200,201,202,203,240,241,242,243,280,281,282,283]

        for i in range(0,4):
            for ii in range(0,8):
                self.TileIDToAddCollidersTo.append((ii * 40) + i) 
        
        

    def loadTileSprites(self, ss, PosX, PosY):
        for row in range(0, PosY):
            for sprite in range(0, PosX):
                surface = pygame.Surface((self.tw, self.th)).convert()
                surface.blit(ss,(0,0), ((sprite * self.tw), (row * self.th), self.tw, self.th))
                surface.set_colorkey((0,0,0))
                self.TilesToWorkWith[str(((row*PosX) + sprite))] = surface
                #print(str((row + sprite)))
        #print(str(self.TilesToWorkWith))
    def loadCSV(self):
        maplist = []
        with open(os.path.join(self.csv)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                maplist.append(list(row))
        return maplist
    def loadMap(self, howFarDownToDraw, howFarAcrossToDraw):
        x = 0
        y = 0

        counterForCollidableTiles = 0

        listOfSeenTileIDs = []
        

        for row in self.maplist:
            x = 0
            for num in row:
                try :
                    if num != "-1":
                        #print("x is: " + str(howFarAcrossToDraw + (x * self.tw) - self.tw))
                        #print("x is: " + str(howFarAcrossToDraw + (x * self.tw) - self.tw))
                        tileBlitted = False
                        for id in self.TileIDToAddCollidersTo:
                            if int(num) == int(id):
                                tile = CollidableTile(self.TilesToWorkWith[num], (howFarAcrossToDraw + (x * self.tw) - self.tw, howFarDownToDraw+ (y * self.th)- self.th), self.game.GetAllSpriteGroup(), z=LAYERS['OBSTACLES'])                        
                                self.game.addToCollideGroup(tile)
                                #print("Collision Tile Created") 
                                counterForCollidableTiles += 1            
                                tileBlitted = True
                        if tileBlitted == False: Tile(self.TilesToWorkWith[num], (howFarAcrossToDraw + (x * self.tw) - self.tw, howFarDownToDraw+ (y * self.th)- self.th), self.game.GetAllSpriteGroup())
                        
                        
                        
                        coord = (str(x),str(y))
                        self.tiles[coord] = num

                except: 
                    if num != "-1":print("Value" + str(num) + " is not in dictionary")
            
            
            
                x = x + 1

            y = y + 1
        print(listOfSeenTileIDs)
        print(counterForCollidableTiles)
        print(self.TileIDToAddCollidersTo)
        self.AddListOfTileIDCollider = []

    def AddTileIDCollider(self, tileid):
        self.TileIDToAddCollidersTo.append(tileid)
    def AddListOfTileIDCollider(self, tileidList):
        for tileid in tileidList:
            self.TileIDToAddCollidersTo.append(tileid)
    
# class Pathway(pygame.sprite.Sprite):
#     def __init__(self,pos,type, pathwayWidth, pathwayHeight,game=Game.Game,z = LAYERS['PATHWAY'], TileSize = 32, spriteSheetWidthRange = (20,22), spriteSheetHeightRange = (0, 2)):
#         self.spritesheet = pygame.image.load('TileMaps\Outside.png')
#         self.tilesToWorkWith = []
#         self.z = z

#         self.SpriteSheetTotalWidth = self.spritesheet.get_width()/TileSize
        

#         for i in range(spriteSheetWidthRange[0],spriteSheetWidthRange[1] + 1):
#             for ii in range(spriteSheetHeightRange[0],spriteSheetHeightRange[1] + 1):
#                 self.tilesToWorkWith.append((ii * self.SpriteSheetTotalWidth) + i) 
        
#         surface = pygame.surface.Surface((pathwayWidth * TileSize, pathwayHeight * TileSize)).convert_alpha()


#         self.tilesToWorkWith = sorted(self.tilesToWorkWith)
#         print(self.tilesToWorkWith)

#         iiCounter = 0

#         for i in range(0,pathwayWidth):
#             if i == 0: #do left corner
#                 surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[0]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[0]%self.SpriteSheetTotalWidth,TileSize, TileSize))        
#                 print("0")
#             elif i == pathwayWidth: #do right corner
#                 surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[2]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[2]%self.SpriteSheetTotalWidth,TileSize, TileSize))        
#                 print("1")   
#             else:
#                 surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[1]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[1]%self.SpriteSheetTotalWidth,TileSize, TileSize))        
#                 print("2")   
#             for ii in range(0, pathwayHeight):
#                 if (iiCounter > 0 and iiCounter < pathwayHeight) and i == 0:
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[3]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[3]%self.SpriteSheetTotalWidth,TileSize, TileSize))     
#                     print("3")   
#                 elif (iiCounter > 0 and iiCounter < pathwayHeight) and (i > 0 and i < pathwayWidth): # middle tiles
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[4]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[4]%self.SpriteSheetTotalWidth,TileSize, TileSize))                        
#                     print("4")   
#                 elif (iiCounter > 0 and iiCounter < pathwayHeight) and i == pathwayWidth: # right center tiles
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[5]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[5]%self.SpriteSheetTotalWidth,TileSize, TileSize))                        
#                     print("5")                   
#                 elif iiCounter == pathwayHeight-1 and i == 0: # bottom left tiles
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[6]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[6]%self.SpriteSheetTotalWidth,TileSize, TileSize))                        
#                     print("6")   
#                 elif iiCounter == pathwayHeight-1 and (i > 0 and i < pathwayWidth): # center bottom tiles
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[7]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[7]%self.SpriteSheetTotalWidth,TileSize, TileSize))                        
#                     print("7")   
#                 elif iiCounter == pathwayHeight-1 and i == pathwayWidth: # bottom right tiles
#                     surface.blit(self.spritesheet, (i * TileSize, iiCounter * TileSize), (self.tilesToWorkWith[8]//self.SpriteSheetTotalWidth,self.tilesToWorkWith[8]%self.SpriteSheetTotalWidth,TileSize, TileSize))                        
#                     print("8")   
#                 iiCounter += 1
#         self.image = surface
#         self.rect = self.image.get_rect(topleft=pos)
#         super().__init__(game.GetAllSpriteGroup())
