import pygame,math, Utilities, DataSystem
from Functions import *
from Settings import *

class Game():
    def __init__(self):
        #Level data
        self.currentLevel = None
        self.listOfMaps = [r'MapsTiled\map2.csv',r'MapsTiled\grassbackground.csv']
        self.customSpawners = ['MapsTiled/custommap01.csv']
        self.HowFarDownIsAMap = 0
        self.HowFarAcrossIsAMap = 0

        self.screen = pygame.display.get_surface()

        self.TileEnvironment = pygame.sprite.Group()
        self.EnemyEnvironment = pygame.sprite.Group()
        self.CollideGroup = pygame.sprite.Group()
        self.allSpritesGroup = pygame.sprite.Group()

        self.dt = None

        self.player = None


        self.mapHeightIncreaseOnLevel = 120
        self.mapHeight = 120
        self.mapWidth = 1000
        self.tileSize = 32
        self.defaultTile = 66
        self.defaultTileSurface = None
        self.tileMap = createMapDictionary(self.mapWidth,self.mapHeight,self.tileSize,self.defaultTile)
        self.initDefaultMap(pygame.image.load(r'TileMaps\OutsideTransparent.png'))

        self.dueDeletionQueue = Utilities.Queue()
        self.spawnQueue = Utilities.FunctionQueue()

        self.EnemiesPerSpawner = 0
        

        self.Spawners = []
        self.TopLeftOfSpawners = []
        self.closestSpawner = None

        self.PriceForHealth = 100   
        self.PriceForDamage = 100
        self.PriceForSpeed = 100

        self.IncreaseOnHealth = 10
        self.IncreaseOnDamage = 1
        self.IncreaseOnSpeed = 10
        
        self.initatePrices()

        self.SpriteSheet = pygame.image.load(r'TileMaps\OutsideTransparent.png')
        self.SpriteSheetWidth = self.SpriteSheet.get_width() / self.tileSize
        self.SpriteSheetHeight =  self.SpriteSheet.get_height() / self.tileSize
        self.TilesToWorkWith = {}
        self.loadTileSprites( self.SpriteSheet, int(self.SpriteSheetWidth), int(self.SpriteSheetHeight))

        self.updateFunctions = [] #this is for the spawners update so they only spawn enemies when the player is close enough
        
        self.particleSystem = None
        self.projectileManager = None
        self.enemyManager = None
        self.dataSystemManager  = None

    def clearUpdateFunctions(self):     self.updateFunctions.clear()
    def clearClosestSpawnerList(self):  self.TopLeftOfSpawners.clear()

    def removeUpdateFunc(self, func):
        self.updateFunctions.remove(func)

    def addUpdateFunc(self, func):
        self.updateFunctions.append(func)

    def update(self):
        for func in self.updateFunctions:
            func()

    
    # def CalculatePath(self, startPoint, endPoint, returnPathOnly=True):
    #     path,runs = self.finder.find_path(startPoint, endPoint, self.grid)
    #     if returnPathOnly:  return path
    #     else:   return path,runs
        
    # def getGrid(self):
    #     return self.grid

    def addToSpawnQueue(self, item, *args):
        self.spawnQueue.AddToQueue(item, args)

    def dequeueSpawnQueue(self):
        return self.spawnQueue.dequeue()

    def isSpawnQueueEmpty(self):
        return self.spawnQueue.isEmpty()

    def handleSpawnQueue(self): # handles only one spawn
        inst, args = self.dequeueSpawnQueue()
        inst(*args)
        pass

    def handleDeletionQueue(self):
        colliderToDelete = self.dequeuDeletionQueue()
        colliderToDelete.kill()
        self.CollideGroup.remove(colliderToDelete)
    
    def isDeletionQueueEmpty(self):
        return self.dueDeletionQueue.isEmpty()

    def dequeuDeletionQueue(self):
        return self.dueDeletionQueue.Dequeue()
    
    def addToDeletionQueue(self, item):
        self.dueDeletionQueue.AddToQueue(item)

    def getTileHeightOfSpriteSheet(self):
        return self.SpriteSheetHeight

    def getTileWidthOfSpriteSheet(self):
        return self.SpriteSheetWidth

    def getTilesToWorkWith(self):
        return self.TilesToWorkWith

    def loadTileSprites(self, ss, PosX, PosY):
        for row in range(0, PosY):
            for sprite in range(0, PosX):
                surface = pygame.Surface((self.tileSize, self.tileSize)).convert_alpha()
                surface.blit(ss,(0,0), ((sprite * self.tileSize), (row * self.tileSize), self.tileSize, self.tileSize))
                surface.set_colorkey((0,0,0))
                self.TilesToWorkWith[str(((row*PosX) + sprite))] = surface
                #print(str((row + sprite


    def IncreaseDamagePrice(self):
        self.PriceForDamage *= 1.2
        self.PriceForDamage = int(self.PriceForDamage)
    def IncreaseHealthPrice(self):
        self.PriceForHealth *= 1.2
        self.PriceForHealth = int(self.PriceForHealth)
    def IncreaseSpeedPrice(self):
        self.PriceForSpeed *= 1.2
        self.PriceForSpeed = int(self.PriceForSpeed)

    def getPriceForDamge(self):
        return self.PriceForDamage
    def getPriceForHealth(self):
        return self.PriceForHealth
    def getPriceForSpeed(self):
        return self.PriceForSpeed
    
    def getIncreaseOnDamge(self):
        return self.IncreaseOnDamage
    def getIncreaseOnHealth(self):
        return self.IncreaseOnHealth
    def getIncreaseOnSpeed(self):
        return self.IncreaseOnSpeed

    def SavePricesAndUpgrades(self):        
        file = open(r"stats\prices.txt", "w")

        file.write("DAMAGE:" + str(self.PriceForDamage) + ":" + str(self.IncreaseOnDamage )+ "\n")
        file.write("HEALTH:" + str(self.PriceForHealth) + ":" + str(self.IncreaseOnHealth )+ "\n")
        file.write("SPEED:" + str(self.PriceForSpeed) + ":" + str(self.IncreaseOnSpeed )+ "\n")

        file.close()
        return

    def initatePrices(self):
        try:
            file = open(r"stats\prices.txt", "r")
            for line in file:
                lineSPlit = line.split(":")
                typeOfStat = str(lineSPlit[0])
                PriceOfStat = int(lineSPlit[1])
                IncreaseOnStat = int (lineSPlit[2])

                if typeOfStat == "DAMAGE":
                    self.PriceForDamage = PriceOfStat
                    self.IncreaseOnDamage = IncreaseOnStat
                elif typeOfStat == "HEALTH":
                    self.PriceForHealth = PriceOfStat
                    self.IncreaseOnHealth = IncreaseOnStat
                elif typeOfStat == "SPEED":
                    self.PriceForSpeed= PriceOfStat
                    self.IncreaseOnSpeed = IncreaseOnStat


            file.close()
        except:
            
            try:
                file = open(r"stats\prices.txt", "x")
            except:
                print("file exists")

            #typeOfStat:Price:Increase
            file = open(r"stats\prices.txt", "a")
            file.write("DAMAGE:" + str(self.PriceForDamage) + ":" + str(self.IncreaseOnDamage )+ "\n")
            file.write("HEALTH:" + str(self.PriceForHealth) + ":" + str(self.IncreaseOnHealth )+ "\n")
            file.write("SPEED:" + str(self.PriceForSpeed) + ":" + str(self.IncreaseOnSpeed )+ "\n")
            
            file.close()
        return

    def getSpawners(self):
        return self.Spawners

    def addSpawner(self, spawner):
        self.Spawners.append(spawner)
        

    def removeSpawner(self, spawner):
        self.Spawners.remove(spawner)
        self.TopLeftOfSpawners.remove(spawner.posVector)
        self.setClosestSpawner()

    def setClosestSpawner(self):
        self.closestSpawner = self.getClosestSpawner()

    def getClosestSetSpawner(self):
        return self.closestSpawner

    def getClosestSpawner(self):
        if not self.TopLeftOfSpawners or not self.player:
            return
        
        minDistance = float('inf')


        closestSpawner = None

        for spawner in self.TopLeftOfSpawners:
            distance = math.hypot(spawner.x - self.player.position.x, spawner.y - self.player.position.y)

            if distance < minDistance:
                minDistance = distance
                closestSpawner = spawner

        spawner = self.Spawners[self.TopLeftOfSpawners.index(closestSpawner)]
        centerOfSpawner = pygame.math.Vector2(closestSpawner.x + (spawner.WidthOfSpawner/2 * self.tileSize), closestSpawner.y + (spawner.HeightOfSpawner/2 * self.tileSize))


        self.player.ClosestSpawnerVector = centerOfSpawner
        print("printing closesst spawner next")
        print(self.player.ClosestSpawnerVector)
        print(closestSpawner)
        return closestSpawner

    def getSpawnersVectors(self):
        return self.TopLeftOfSpawners

    def addSpawnerVecotr(self, pos=pygame.math.Vector2):
        if type(pos) is not pygame.math.Vector2: return
        self.TopLeftOfSpawners.append(pos)
    

    def handleMatrix(self):
        x = 0
        y = self.mapHeight

        for hight in range(self.mapHeightIncreaseOnLevel):
            list = [int]
            for width in range(self.mapWidth):
                list.append(0)
                x += 1
            
            self.matrix[y] = list
            y += 1
        
    def LevelFinished(self):
        # self.handleMatrix()

        self.screen.blit(self.defaultTileSurface, (0, ((self.mapHeight * self.tileSize) * (self.currentLevel.levelNumber + 1)) -(self.mapHeight * self.tileSize)))

        newSurface = pygame.surface.Surface((self.defaultTileSurface.get_width(), self.defaultTileSurface.get_height() + (self.tileSize * self.mapHeightIncreaseOnLevel)))
        newSurface.blit(self.defaultTileSurface, (0,0))
        mapAddonSurface = pygame.surface.Surface((self.mapWidth * self.tileSize, self.mapHeightIncreaseOnLevel * self.tileSize))
        mapAddonSurface.blit(self.defaultTileSurface, (0,0))
        newSurface.blit(mapAddonSurface, (0,newSurface.get_height() - (self.mapHeightIncreaseOnLevel * self.tileSize)))
        
        self.mapHeight += self.mapHeightIncreaseOnLevel

        self.defaultTileSurface = newSurface
        return
        
    def initDefaultMap(self,spriteSheet):
        spriteSheetWidth = spriteSheet.get_width()

        tileWidth = spriteSheetWidth / self.tileSize
        
        mainSurface = pygame.surface.Surface((self.mapWidth * self.tileSize, self.mapHeight * self.tileSize))

        for tileXY in self.tileMap:
            tileRow = self.tileMap[tileXY] // tileWidth #returns the division without the remainder
            tileColumn = self.tileMap[tileXY] % tileWidth #returns the remainder

            tileX = tileXY[0]
            tileY = tileXY[1]

            tileSurface = pygame.surface.Surface((self.tileSize, self.tileSize))
            tileSurface.blit(spriteSheet, (0,0), (tileColumn * self.tileSize,tileRow * self.tileSize , self.tileSize, self.tileSize))
            tileSurface.set_colorkey((0,0,0))

            mainSurface.blit(tileSurface,(tileX, tileY))


        self.defaultTileSurface = mainSurface

        # x = 0
        # y = 0

        # for hight in range(self.mapHeightIncreaseOnLevel):
        #     list = [int]
        #     for width in range(self.mapWidth):
        #         list.append(0)
        #         x += 1
            
        #     self.matrix[y] = list
        #     y += 1


    def deleteFromDeleteList(self):
        if self.ToDelete:
            item = self.ToDelete.pop()
            for obstacle in self.GetAllSpriteGroup().sprites():
                if obstacle.z == LAYERS['OBSTACLES']:
                    if obstacle == item:
                        self.GetAllSpriteGroup().remove(obstacle)



    def CheckDeleteList(self):
        return self.ToDelete

    def PopDeleteList(self):
        return self.ToDelete.pop()

    def AddToDelete(self, item):
        self.ToDelete.append(item)  

    def setDimensionsOfMap(self, widhtOfMap, HeightOfMap):
        self.HowFarAcrossIsAMap = widhtOfMap
        self.HowFarDownIsAMap = HeightOfMap

    def SetLevel(self, level):
        self.currentLevel = level
    def GetLevel(self):
        return self.currentLevel
    
    def GetScreen(self):
        return self.screen

    def SetCollideGroup(self, collidegroup=pygame.sprite.Group):
        self.CollideGroup = collidegroup
    
    def GetCollideGroup(self):
        return self.CollideGroup

    def SetProjectileManager(self, projectileManager): self.projectileManager = projectileManager
    def GetProjectileManager(self): return self.projectileManager

    def GetProjectilesForOwner(self, owner):
        if owner in self.projectileManager.ownersAndProjectiles:
            print(f"{owner} has projectiles, passed them back")
            return self.projectileManager.ownersAndProjectiles[owner]
        else:
            print("owner has no projectiles")
            return

    def SetParticleSystem(self, particleSystem): self.particleSystem = particleSystem
    def GetParticleSystem(self): return self.particleSystem 

    def SetTileEnvironment(self, tileEnvironment):
        self.TileEnvironment = tileEnvironment
    
    def SetEnemyEnvironment(self, enemyEnvironment):
        self.EnemyEnvironment = enemyEnvironment

    def GetEnemies(self):
        return self.EnemyEnvironment

    def SetAllSprites(self, allsprites):
        self.allSpritesGroup = allsprites

    def GetAllSpriteGroup(self):
        return self.allSpritesGroup
    
    def RemoveFromAllSpriteGroup(self,item): self.allSpritesGroup.remove(item)

    def SetDeltaTime(self, dt): 
        self.dt = dt

    def GetDeltaTime(self):
        return self.dt

    def SetPlayer(self, player):
        self.player = player

    def GetPlayer(self):
        return self.player
    
    def GetListOfMapsCSV(self):
        return self.listOfMaps

    def addToCollideGroup(self, sprite=pygame.sprite.Sprite):
        self.CollideGroup.add(sprite)

    def addToEnemyGroup(self, enemy=pygame.sprite.Sprite):
        self.EnemyEnvironment.add(enemy)

    def setEnemyManager(self, enemyManager):    self.enemyManager = enemyManager
    def setDataSystemManager(self, dataSystemManager): self.dataSystemManager = dataSystemManager

    def onQuit(self):
        


        #handling enemy data
        if self.enemyManager is not None:
            enemies = self.enemyManager.Enemies
            print("Enemy manager set correctly.")
            if len(enemies) > 0: # there are enemies currently spawned
                print(F"There are {len(enemies)} to handle and save correctly.")
                for enemy in enemies:
                    print(F"Saving {enemy}.")
                    enemyData = DataSystem.EnemyData()
                    enemy.UpdateData(enemyData)
                    print(f"going to print the enemy data. {enemyData.__dict__}")
                    if self.dataSystemManager is not None:
                        self.dataSystemManager.addEnemyData(enemyData)
                    print(f"printing enemy data in data dictionary, {self.dataSystemManager.data}")
            else: print("No enemies to save.")











        # saveAllData
        if self.dataSystemManager is not None:
            self.dataSystemManager.saveAllData()
