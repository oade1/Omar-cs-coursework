from Settings import LAYERS
import pygame, random,Game, os, Raycast, math, DataSystem
from Settings import *
from Vectors import *
from pygame.locals import *
from Collectables import *
from Functions import getGridLoc

#region
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self,Image, Position, Health, Speed, Damage, game=Game.Game,group=pygame.sprite.Group, z = LAYERS['ENEMY']):
#         super().__init__(group)
#         self.image = Image
#         self.z = z
#         self.spawnPosition = Position
#         self.mask = pygame.mask.from_surface(self.image)
#         self.rect = self.image.get_rect(center=Position)
#         self.maxHealth = Health
#         self.currentHealth = Health
#         self.speed = Speed
#         self.damage = Damage

#         self.game = game 

#         self.AllAnimations = {}
#         self.currentAnimationList = []

#         self.direction = pygame.math.Vector2()
        
#         #flags
#         self.isInRange = False
#         self.isIdle = True
#         self.isMoving = False
#         self.isAttacking = False
#         self.isDead = False
#         self.EnemySpotted = False

#         self.DamageTaken = False

#         self.setUpAnimation(self.image, 32, 32)


#         #values
#         self.howfartogoonx = 0
#         self.howfartogoony = 0

#         self.timeToUpdateAnimationFrame = pygame.time.get_ticks()   
#         self.timeToHitTarget = pygame.time.get_ticks()

#         self.cooldownToUpdateAnimation = 80
#         self.cooldownToHitTarget = 5000

#         self.directionInInteger = 0
#         self.animationFrame = 0

#         randomImage = random.choice(list(self.AllAnimations.values()))

#         self.rect = randomImage[0].get_rect(center=(self.spawnPosition))
#         self.position =  pygame.math.Vector2(self.rect.center)
#         self.CollideRect = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)


#     def update(self):
#         self.checkCollision()
#         self.updateAnimation()
#         if self.EnemySpotted:
#             self.findDirection()
#             self.HandleMovement()
#         else:
#             self.roam()
#             self.SpotEnemy()
            
#             if self.isInRange:
#                 self.attackPlayer()



#         if abs(self.game.GetPlayer().CollideRect.x - self.rect.x) < 15 and abs(self.game.GetPlayer().CollideRect.y - self.rect.y) < 15:
#             self.isInRange = True
#         else: 
#             self.isInRange = False 
#     def attackPlayer(self):
#         if pygame.time.get_ticks() > self.timeToHitTarget:
#             self.timeToHitTarget += self.cooldownToHitTarget
#             self.game.GetPlayer().takeDamage(self.damage)
#             print("enemy hit")
#     def checkCollision(self):
#         if self.game.GetPlayer().isAttacking and self.DamageTaken == False:
#             if abs(self.position.x - self.game.GetPlayer().position.x) < 150 and abs(self.position.y - self.game.GetPlayer().position.y) < 100:
#                 if self.game.GetPlayer().CenterRect.x <= self.rect.x:
#                     if self.game.GetPlayer().idleDirection == 1:
#                         self.DamageTaken = True
#                         self.game.GetPlayer().ResetEnemyDamageVulnerability(self)
#                         self.takeDamage(self.game.GetPlayer().damage)                
#                         print("enemy is to the right of player,damage taken by enemy, health remaining: " + str(self.currentHealth))
#                 elif self.game.GetPlayer().CenterRect.x > self.rect.x:
#                     if self.game.GetPlayer().idleDirection == -1:
#                         self.DamageTaken = True
#                         self.game.GetPlayer().ResetEnemyDamageVulnerability(self)
#                         self.takeDamage(self.game.GetPlayer().damage)                
#                         print("enemy is to the left of player,damage taken by enemy, health remaining: " + str(self.currentHealth))
#                 if self.game.GetPlayer().CenterRect.y <= self.rect.y:
#                     if self.game.GetPlayer().idleDirection == 0:
#                         self.DamageTaken = True
#                         self.game.GetPlayer().ResetEnemyDamageVulnerability(self)
#                         self.takeDamage(self.game.GetPlayer().damage)                
#                         print("enemy is to the bottom of player,damage taken by enemy, health remaining: " + str(self.currentHealth))
#                 elif self.game.GetPlayer().CenterRect.y > self.rect.y:
#                     if self.game.GetPlayer().idleDirection == 2:
#                         self.DamageTaken = True
#                         self.game.GetPlayer().ResetEnemyDamageVulnerability(self)
#                         self.takeDamage(self.game.GetPlayer().damage)                
#                         print("enemy is to the top of player,damage taken by enemy, health remaining: " + str(self.currentHealth))
                
#     def HandleMovement(self):
        
#         self.position += self.direction * self.speed * self.game.GetDeltaTime() 

#         #horizontal
#         self.rect.centerx = round(self.position.x)
#         self.CollideRect.centerx = round(self.position.x)

#         #vertical
#         self.rect.centery = round(self.position.y)
#         self.CollideRect.centery = round(self.position.y)

#     def findDirection(self):
#         self.direction = pygame.math.Vector2(self.game.GetPlayer().position.x -self.rect.centerx,self.game.GetPlayer().position.y - self.rect.centery)
#         if self.direction: self.direction = self.direction.normalize()


#     def updateAnimation(self):
#         #print("update animation called")
#         #print(self.isInRange)
#         if self.direction.x > 0:
#             self.currentAnimationList = self.AllAnimations["WALKRIGHT"]
#             self.directionInInteger = 1
#         if self.direction.x < 0:
#             self.currentAnimationList = self.AllAnimations["WALKLEFT"]
#             self.directionInInteger = -1
#         else:
#             if self.directionInInteger == 1:
#                 self.currentAnimationList = self.AllAnimations["IDLERIGHT"]
#             elif self.directionInInteger == 0:
#                 self.currentAnimationList = self.AllAnimations["IDLE"]
#             elif self.directionInInteger == -1:
#                 self.currentAnimationList = self.AllAnimations["IDLELEFT"]
        
#         if self.animationFrame >= len(self.currentAnimationList):
#             self.animationFrame = 0
#         self.image = self.currentAnimationList[self.animationFrame]




#     def setUpAnimation(self, spritesheet, width, height):
#         self.getAnimationFrame(spritesheet,0,6,width,height,"IDLE", False)
#         self.getAnimationFrame(spritesheet,1,6,width,height,"IDLERIGHT", False)
#         self.getAnimationFrame(spritesheet,1,6,width,height,"IDLELEFT", True)
#         self.getAnimationFrame(spritesheet,2,6,width,height,"IDLEUP", False)
#         self.getAnimationFrame(spritesheet,3,6,width,height,"WALKUP", False)
#         self.getAnimationFrame(spritesheet,4,6,width,height,"WALKRIGHT", False)
#         self.getAnimationFrame(spritesheet,4,6,width,height,"WALKLEFT", True)
#         self.getAnimationFrame(spritesheet,5,6,width,height,"WALKDOWN", True)
#         self.getAnimationFrame(spritesheet,6,4,width,height,"ATTACK", False)
#         self.getAnimationFrame(spritesheet,7,4,width,height,"ATTACKRIGHT", False)
#         self.getAnimationFrame(spritesheet,7,4,width,height,"ATTACKLEFT", True)
#         self.getAnimationFrame(spritesheet,8,4,width,height,"ATTACKUP", False)
#         self.getAnimationFrame(spritesheet,9,3,width,height,"DEATH", False)
#         print("enemy animations loaded")

#     def resetDamage(self):
#         self.DamageTaken = False

#     def roam(self):
#         if self.howfartogoonx == 0:
#             self.howfartogoonx = random.randint(-50, 50)       


#         if self.howfartogoonx < 0:
#             self.howfartogoonx += 1
#             self.direction.x = -1
#         elif self.howfartogoonx > 0:
#             self.howfartogoonx -= 1
#             self.direction.x = 1
#         self.position += self.direction * self.speed * self.game.GetDeltaTime()
#         self.HandleMovement()
#     def SpotEnemy(self):
#         if abs(self.rect.x - self.game.GetPlayer().CollideRect.x) < 50 or abs(self.rect.y - self.game.GetPlayer().CollideRect.y) < 50:
#             self.EnemySpotted = True
#             self.direction.x = 0
#             self.direction.y = 0
#             print("enemy spotted")



#     def getAnimationFrame(self, spritesheet, y, frames, width, height, animationNameInCaps, flip:bool):
#         list = []

#         for frame in range(frames):
#             surface = pygame.Surface((width, height)).convert()
#             surface.set_colorkey((0,0,0))
#             surface.blit(spritesheet, (0,0), ((width * frame), (height * y), width, height))
#             surface = pygame.transform.scale(surface, (width * 3, height * 3))
#             if flip:
#                 surface = pygame.transform.flip(surface, True, False)            
#             surface.set_colorkey((0,0,0))
#             list.append(surface)
        
#         self.AllAnimations[animationNameInCaps] = list
#         #print(self.AllAnimations)

#     def takeDamage(self, damage):
#         self.currentHealth -= damage
#         if self.currentHealth <= 0:
#             self.kill()
#             self.game.GetPlayer().addGold(int(self.maxHealth/5) * random.randint(1,4))
#endregion


class EnemyManager:
    def __init__(self, game=Game.Game):
        self.game = game
        self.AllAnimations = {} #key is the name of the enemy (skeleton, necromancer etc) and the value is the dictionary of animations (key is the animation name and value is list of those sprites)
        self.Enemies = []

        self.loadAllEnemies()

        game.setEnemyManager(self)

    def onQuit(self):
        pass
    

    def loadAllEnemies(self):
        enemiesToLoad = ['Skeleton', 'Necromancer']
        for enemyName in enemiesToLoad:
            self.loadEnemySprites(FolderName=enemyName)



        print(self.AllAnimations)

    def loadEnemySprites(self, FolderName='Skeleton'): # folder name is the name of the folder that holds the enemy's sprites
        #width and height are both 48
        AnimationDictionary = {}
        pixelSize = 48
        mainSubDirectory = "/Enemies/"+FolderName
        subDirectories = [mainSubDirectory+"/Down",mainSubDirectory+"/Up",mainSubDirectory + "/Right", mainSubDirectory + "/Left"]
        currentDirectory = os.getcwd()
        for i in range(len(subDirectories)):
            for file in os.listdir(currentDirectory + subDirectories[i]):
                #print(file)
                image = pygame.image.load(currentDirectory+subDirectories[i]+"/"+file).convert()
                width = image.get_width()
                height = image.get_height()

                framesWidth = int(width/pixelSize)
                framesHeight = height/pixelSize
                
                fileName = file.removesuffix(".png")
                #print(framesWidth)
                fromx = 0
                listOfFrames = []
                for frame in range(framesWidth):
                    fromx += 1
                    surface = pygame.surface.Surface((pixelSize, pixelSize)).convert()
                    surface.blit(image, (0,0), ((fromx * pixelSize) - pixelSize,0, pixelSize, pixelSize))
                    # surface = pygame.transform.scale(surface, (pixelSize*3, pixelSize*3))
                    surface.set_colorkey((255,0,255))
                    listOfFrames.append(surface)

                AnimationDictionary[fileName] = listOfFrames

        self.AllAnimations[FolderName] = AnimationDictionary

        #print(self.allAnimations)

    def createSkeleton(self, Position):
        self.addEnemy(Skelly(self,Position, self.AllAnimations['Skeleton']))
    
    def createNecromancer(self, Position):
        self.addEnemy(Necromancer(self,Position, self.AllAnimations['Necromancer']))

    def addEnemy(self, enemy):
        self.Enemies.append(enemy)
        self.game.GetAllSpriteGroup().add(enemy)
        self.game.GetCollideGroup().add(enemy)
        self.game.GetEnemies().add(enemy)

    def removeEnemy(self, enemy):
        if enemy in self.Enemies:
            self.Enemies.remove(enemy)
            self.game.GetAllSpriteGroup().remove(enemy)
            self.game.GetCollideGroup().remove(enemy)
            self.game.GetEnemies().remove(enemy)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, EnemyManager=EnemyManager, Position=pygame.Vector2, AnimationDictionary={}, z = LAYERS['ENEMY'],AnimationStart=str):
        super().__init__(EnemyManager.game.GetAllSpriteGroup())

        self.serializedNumber = len(EnemyManager.Enemies) + 1
        print(self.serializedNumber)

        self.die = EnemyManager.removeEnemy
        self.getDeltaTime = EnemyManager.game.GetDeltaTime

        self.target = EnemyManager.game.GetPlayer()
        self.Animations = AnimationDictionary
        print(self.Animations)
        self.position = Position
        self.spawnPoint = pygame.Vector2(self.position.x, self.position.y)
        self.z = z
        keys = list(self.Animations.keys())
        ran = random.choice(keys)
        self.image = self.Animations[ran][0]
        self.rect = self.image.get_rect(center=self.position)
        self.CollideRect = self.rect.copy().inflate(self.rect.width * -0.8,self.rect.height * -0.5)

        #state
        self.speed = None
        self.maxHealth = None
        self.currentHealth = None
        self.damage = None
        self.attackCooldown = None
        self.loadEnemyStats()

        #Animation variables
        self.AnimationStart = AnimationStart
        self.AnimationAction = ''
        self.AnimationDirection = ''
        self.Animationlist = None

        self.AnimationTime = pygame.time.get_ticks()
        self.AnimationCooldown = 80

        self.Frame = 0

        #Movement
        self.direction = pygame.Vector2(0,0)

        #state maangement
        # self.CurrentState = None
        # self.states = {
        #     'IDLE': IdleState(),
        #     'FOLLOW': FollowState(),
        #     'ATTACK': AttackState(),
        #     'GOTO': GoToState(),
        #     'REST': RestState(),
        #     'HURT': HurtState(),
        #     'DIE': DeathState()
        # }   
        # self.changeState('IDLE')
        #State machine should be in the inherited classes

        #UI
        self.healthBar = pygame.rect.Rect(self.rect.x,self.rect.y, self.rect.width * 0.8, self.rect.height * 0.05)
        self.healthBarRatio = self.maxHealth/self.healthBar.width
    
    def takeHealth(self, damage):
        self.currentHealth -= damage
        print(f"enemy took damage:{self.currentHealth}.")

    def takeDamage(self, damage):
        print("Player took damage")
        if type(self.CurrentState) is not HurtState:
            self.changeState('HURT')
            print(f"state changed to {self.CurrentState}.")
        self.states['HURT'].damageTaken += damage
        print(f"Player took damage, damage taken by player {self.states['HURT'].damageTaken}.")


    def changeState(self, state):
        if self.CurrentState is not None:
            self.CurrentState.exit(self)
        self.CurrentState = self.states[state]
        self.CurrentState.enter(self)

    def getState(self, state):
        return self.states[state]

    def update(self):
        if self.CurrentState is not None:
            self.CurrentState.update(self)


    def handleAnimation(self):
        if self.Animationlist is not self.Animations[self.AnimationStart + self.AnimationDirection + self.AnimationAction]:
            self.Animationlist = self.Animations[self.AnimationStart + self.AnimationDirection + self.AnimationAction]
            # print(f"Animation changed, the current animation list is {self.AnimationStart + self.AnimationDirection + self.AnimationAction}")

        if pygame.time.get_ticks() > self.AnimationTime:
            self.AnimationTime += self.AnimationCooldown
            self.Frame += 1

            if self.Frame >= len(self.Animationlist):
                self.Frame = 0

            self.image = self.Animationlist[self.Frame]


    def handleDirection(self):
        printPrintStatements = False

        if self.direction.x > 0: # moving right
            self.AnimationDirection = 'Right'
            if printPrintStatements:print("Direction is right")
        elif self.direction.x < 0: # moving left
            self.AnimationDirection = 'Left'
            if printPrintStatements:print("Direction is left")
        elif self.direction.y > 0: #moving down
            self.AnimationDirection = 'Down'
            if printPrintStatements:print("Direction is down")
        elif self.direction.y < 0:
            self.AnimationDirection = 'Up'
            if printPrintStatements:print("Direction is up")
        else: # if no direction then face down
            self.AnimationDirection = 'Down'
            if printPrintStatements:print(f"direction has no magnitude, this is the direction {self.direction}")

    def changeDirection(self, newDirection=pygame.Vector2):
        self.direction = newDirection

    def loadEnemyStats(self):
        pass

    def drawHealthBar(self, offset = pygame.math.Vector2, internalSurface = pygame.Surface):
        self.healthBar.x = offset.x + (self.rect.width * 0.1)
        self.healthBar.y = offset.y
        pygame.draw.rect(internalSurface, ("white"), self.healthBar)
        red = self.healthBar.copy()
        red.width = self.currentHealth/(self.maxHealth/self.healthBar.width)
        pygame.draw.rect(internalSurface, ("red"), red)

    def Die(self): self.die(enemy=self) #self.die is a reference to the enemymanger remove function
    

    def UpdateData(self, enemyData=DataSystem.EnemyData):
        dataToSave = ['position', 'serializedNumber', 'AttackChargePercentage', 'currentHealth', 'typeID']

        for varName, varValue in self.__dict__.items():
            if varName in dataToSave:
                enemyData.setData(varName, varValue)


    
class Skelly(Enemy):
    def __init__(self, EnemyManager=EnemyManager, Position=pygame.Vector2, AnimationDictionary={}, z=LAYERS['ENEMY']):
        super().__init__(EnemyManager, Position, AnimationDictionary, z, 'SkeletonWithSword')
        self.typeID = '1'
        self.CurrentState = None
        self.states = {
            'IDLE': IdleState(),
            'FOLLOW': FollowState(),
            'ATTACK': AttackState(),
            'GOTO': GoToState(),
            'REST': RestState(),
            'HURT': HurtState(),
            'DIE': DeathState()
        }   
        self.changeState('IDLE')
        
        self.Attacks = {
            'BASE': BaseAttack()
        }
        

         #Attack charging
        self.AttackChargePercentage = 0



        self.currentAttack = self.Attacks['BASE']

        self.originalattackCooldown = 2000
        self.attackCooldown = 2000
        self.nextattackCooldown = 2000

    def loadEnemyStats(self):
        enemyStats = ENEMYSTATS['SKELETON']
        self.speed, self.maxHealth, self.currentHealth, self.damage, self.attackCooldown = enemyStats[0], enemyStats[1], enemyStats[2], enemyStats[3], enemyStats[4]

class Necromancer(Enemy):
    def __init__(self, EnemyManager=EnemyManager, Position=pygame.Vector2, AnimationDictionary={}, z=LAYERS['ENEMY']):
        super().__init__(EnemyManager, Position, AnimationDictionary, z, 'Necromancer')
        self.typeID = '2'
        self.CurrentState = None
        self.states = {
            'IDLE': IdleState(),
            'FOLLOW': FollowState(),
            'ATTACK': AttackState(),
            'GOTO': GoToState(),
            'REST': RestState(),
            'HURT': HurtState(),
            'DIE': DeathState()
        }   


        self.Attacks = {
            'BASE': MultileInferno(),
            'SPECIAL': SpecialAttack(),
            'FIREBALLS': InfernoConvergence()
        }

        self.AttacksPattern = [
            ('BASE', range(0, 15)),
            ('SPECIAL', range(15, 30)),
            ('BASE', range(30, 50)),
            ('FIREBALLS', range(50, 70)),
            ('BASE', range(70, 99)),
            ('FIREBALLS', range(100, 999))
            ]# if this is laggy I will make a custom range class
        
        #Attack charging
        self.AttackChargePercentage = 0

        self.Attacks['BASE'].chargePercentage = 20
        self.Attacks['SPECIAL'].chargePercentage = 15
        self.Attacks['FIREBALLS'].chargePercentage = 20


        #Adjustments to states
        self.originalattackCooldown = 2000
        self.attackCooldown = 2000
        self.nextattackCooldown = 2000
        #References to needed methods
        self.infernoConvergence = EnemyManager.game.GetProjectileManager().createTargetedTimedFireball
        self.inferno = EnemyManager.game.GetProjectileManager().createTargetTimedFireball

        self.getProjectilesOwnedBySelf = EnemyManager.game.GetProjectilesForOwner
        



        self.currentAttack = None

        self.changeState('IDLE')


    def changeState(self, state):
        super().changeState(state)
        
        #setting attack if there is a change
        attackName = None
        print(self.AttacksPattern)

        for pattern in self.AttacksPattern:
            print(f"calculating attack for Necromancer, current attackchargepercentage is {self.AttackChargePercentage}, and current pattern is {pattern}")
            if self.AttackChargePercentage in pattern[1]:
                attackName = pattern[0]
                print(f"attack chaned to {attackName}, current range is {self.AttackChargePercentage}")
                break
        
        if self.currentAttack is not self.Attacks[attackName]:
            self.currentAttack = self.Attacks[attackName]



    def loadEnemyStats(self):
        enemyStats = ENEMYSTATS['NECROMANCER']
        self.speed, self.maxHealth, self.currentHealth, self.damage, self.attackCooldown = enemyStats[0], enemyStats[1], enemyStats[2], enemyStats[3], enemyStats[4]


class State:

    def enter(self, enemy):
        pass

    def update(self, enemy):
        pass

    def exit(self, enemy):
        pass



class GoToState(State):

    def __init__(self):
        self.GoTo = None

    def setUp(self, PointToGoTo, StateToSwitchTo):
        self.GoTo = PointToGoTo
        self.StateToSwitchToAfterReachingPoint = StateToSwitchTo

    def enter(self, enemy=Enemy):
        pass

    def update(self, enemy=Enemy):
        enemy.changeDirection(pygame.Vector2(self.GoTo.x - enemy.position.x, self.GoTo.y - enemy.position.y).normalize())

        enemy.position += enemy.direction * enemy.speed * enemy.getDeltaTime()
        enemy.rect.center = enemy.position
        enemy.CollideRect.center = enemy.position

        if int(enemy.position.x) == int(self.GoTo.x) and int(enemy.position.y) == int(self.GoTo.y):
            print("Point reached")
            if self.StateToSwitchToAfterReachingPoint in enemy.states:
                enemy.changeState(self.StateToSwitchToAfterReachingPoint)

        enemy.handleAnimation()
        enemy.handleDirection()

    def exit(self, enemy=Enemy):
        pass

class IdleState(State):
    def __init__(self):
        self.Direction = pygame.Vector2()
        self.PatrolStartedAt = 0
        self.timeForSaidDirection = 0
        self.timeToCheckAgainst = 0
        self.IsPatroling = False
        self.maxDistanceFromSpawnPoint = 10

        self.distanceToSwitchToOtherState = ENEMYDISTANCES['SKELETON'][0]
        self.otherState = 'FOLLOW'

        self.target = None


    def RandomPatrol(self, enemy):
        
        self.timeForSaidDirection = random.randint(2000, 3000)
        
        direction = None

        while True:
            direction = pygame.Vector2(random.randint(-50, 50), random.randint(-50,50))
            if not direction: #this is just to ensure that it doesnt crash when that 1/10000 time it generats 0 and 0 for the x y directions
                continue # as unlucky that is, it happened to me when I was testing
            direction.normalize() #it crashes cuz you cant normalize a vector with 0 mag
            break
        
        distanceToSpawnPoint = enemy.position.distance_to(enemy.spawnPoint)
        print(f"distnace to spawn point is {distanceToSpawnPoint}, and max distance is {self.maxDistanceFromSpawnPoint}")
        print(f"enemy spawn point is {enemy.spawnPoint}, while their current position is {enemy.position}")
        if distanceToSpawnPoint > self.maxDistanceFromSpawnPoint:
            direction = (enemy.spawnPoint - enemy.position).normalize()
            print("too far from spawnpoint, going to spawn point")
        else:
            posToSpawn = (enemy.spawnPoint - enemy.position)
            if posToSpawn:
                posToSpawn.normalize()

            weightTowardSpawnPoint = distanceToSpawnPoint/self.maxDistanceFromSpawnPoint
            weightedDirection = (direction * (1 - weightTowardSpawnPoint)) + \
                  (posToSpawn * weightTowardSpawnPoint)


            direction = weightedDirection.normalize()

        enemy.changeDirection(direction)

        self.timeToCheckAgainst = self.timeForSaidDirection
        self.PatrolStartedAt = pygame.time.get_ticks()
        self.IsPatroling = True

    def enter(self, enemy=Enemy):
        self.target = enemy.target
        enemy.AnimationAction = 'Idle'
        enemy.handleDirection()
        enemy.Animationlist = enemy.Animations[enemy.AnimationStart+enemy.AnimationDirection+enemy.AnimationAction]
        if not self.IsPatroling: self.RandomPatrol(enemy) 

    def update(self, enemy=Enemy):

        if self.timeToCheckAgainst > 0: #Patrol
            self.timeToCheckAgainst = self.timeForSaidDirection - (pygame.time.get_ticks() - self.PatrolStartedAt)
            enemy.position += enemy.direction * enemy.speed * enemy.getDeltaTime()
            enemy.rect.center = enemy.position
            enemy.CollideRect.center = enemy.position
            # print(f"Current position is {enemy.position}")
            # print(f"patrol started at: {self.PatrolStartedAt}, current time is {pygame.time.get_ticks()}, time left for this patrol is {self.timeToCheckAgainst}")

        if self.timeToCheckAgainst <= 0:
            print(self.timeForSaidDirection)
            self.IsPatroling = False

        if not self.IsPatroling: 
            print("New patrol for enemy")
            self.RandomPatrol(enemy)

        if enemy.direction:
            if enemy.AnimationAction is not 'Run':
                enemy.AnimationAction = 'Run'
                print("Animation swapped to run")
                
        else:
            if enemy.AnimationAction is not 'Idle':
                print("Animation swapped to idle")
                enemy.AnimationAction = 'Idle'

        if enemy.position.distance_to(self.target.position) < self.distanceToSwitchToOtherState:
            print(f"enemy is {enemy.position.distance_to(self.target.position)} close to the target, checking if enemy has other state")
            if self.otherState in enemy.states:
                print(f"enemy has {self.otherState} this state, changing to it...")
                enemy.changeState(self.otherState) 
            else:
                print(f"error, the enemy doesn't have this state {self.otherState}")

        enemy.handleAnimation()
        enemy.handleDirection()

    def exit(self, enemy):
        self.timeForSaidDirection = 0
        self.PatrolStartedAt = 0
        self.target = None

class FollowState(State):

    def __init__(self):
        self.distanceToChangeBackIdleFromSpawnPoint = ENEMYDISTANCES['SKELETON'][1]
        self.distanceWhereTargetIsTooFar = ENEMYDISTANCES['SKELETON'][0]
        self.StateToGoWhenTargetIsTooFar = 'IDLE'
        self.roamBackWhenTooFar = True
        self.target = None

        self.distanceHasBeenSetToHalfTheWidthOfTheImage = False
        self.distanceToDetect = 1
        self.StateToGoToOnDetection = 'ATTACK'

    def setStateToGoToOnDetection(self, state): self.StateToGoToOnDetection = state
    def setStateToGoWhenTargetIsTooFar(self, state): self.StateToGoWhenTargetIsTooFar = state
    def setDistanceToDetect(self, distance): self.distanceToDetect = distance
    def setRoamBackWhenTooFar(self, do): self.roamBackWhenTooFar = do
    
    def enter(self, enemy=Enemy):
        if self.distanceToDetect is not enemy.image.get_width() // 3 and not self.distanceHasBeenSetToHalfTheWidthOfTheImage:
            self.distanceToDetect = enemy.image.get_width() // 3
            self.distanceHasBeenSetToHalfTheWidthOfTheImage = True
            print("set correct follow state variables")
        else:
            print(f"enemy has correct variable for follow variables which are {self.distanceToDetect}")

        if enemy.AnimationAction is not 'Run':
            enemy.AnimationAction = 'Run'

        self.target = enemy.target
        enemy.changeDirection(pygame.Vector2(self.target.position.x - enemy.position.x, self.target.position.y - enemy.position.y).normalize())

        if enemy.currentAttack:
            if hasattr(enemy.currentAttack,'AttackRange'):
                if enemy.currentAttack.AttackRange > 0:
                    self.distanceToDetect = enemy.currentAttack.AttackRange

    def update(self, enemy=Enemy):
        
        if self.target == None: self.target = enemy.target

        enemy.changeDirection(pygame.Vector2(self.target.position.x - enemy.position.x, self.target.position.y - enemy.position.y).normalize())
        # print(f"this is the enemy direction in the follow state {enemy.direction}")
        enemy.position += enemy.direction * enemy.speed * enemy.getDeltaTime()
        enemy.rect.center = enemy.position
        enemy.CollideRect.center = enemy.position
        # print(f"Current position is {enemy.position}")

        if enemy.position.distance_to(enemy.spawnPoint) > self.distanceToChangeBackIdleFromSpawnPoint:
            print(f"Too far from spawnpoint, choosing whether to go back or not, distance is {enemy.position.distance_to(enemy.spawnPoint)}")
            if self.roamBackWhenTooFar:
                print("Going back to idle, went too far away from spawnpoint")
                enemy.getState('GOTO').setUp(enemy.spawnPoint, 'IDLE')
                enemy.changeState('GOTO')
                return
            else:
                print("Enemy chose not to")

        if enemy.position.distance_to(self.target.position) > self.distanceWhereTargetIsTooFar:
            if self.StateToGoWhenTargetIsTooFar:
                if self.StateToGoWhenTargetIsTooFar in enemy.states:
                    enemy.changeState(self.StateToGoWhenTargetIsTooFar)
                    return
        enemy.handleAnimation()
        enemy.handleDirection()


        if enemy.position.distance_to(self.target.position) <= self.distanceToDetect:
            print(f"follow state detects in its {self.distanceToDetect} pixel zone, distance to target is {enemy.position.distance_to(self.target.position)}")
            if self.StateToGoToOnDetection:
                if self.StateToGoToOnDetection in enemy.states:
                    enemy.changeState(self.StateToGoToOnDetection)
                    return
    def setDetectionDistance(self, distance):self.distanceToDetect = distance
    def setStateOnDetection(self, state=str):self.StateToGoToOnDetection = state

    def exit(self, enemy):
        self.target = None

class RestState(State):
    def __init__(self):
        self.defaultState = 'IDLE'

    def enter(self, enemy=Enemy):
        enemy.attackCooldown = enemy.nextattackCooldown
        self.restTime = enemy.attackCooldown
        self.timeToCheck = pygame.time.get_ticks() + self.restTime

    def update(self, enemy=Enemy):
        enemy.handleAnimation()

        if pygame.time.get_ticks() > self.timeToCheck:
            enemy.changeState(self.defaultState)

    def exit(self, enemy=Enemy):
        self.restTime = None
        enemy.nextattackCooldown = enemy.originalattackCooldown


class HurtState(State):
    def __init__(self):
        self.damageTaken = 0
        self.damageApplied = False

    def enter(self, enemy=Enemy):
        enemy.AnimationAction = 'Hurt'
        enemy.changeDirection(pygame.Vector2(0,0))
        print("Hurt state entered")
        self.damageApplied = False

    def update(self, enemy=Enemy):
        
        enemy.handleAnimation()

        if enemy.Frame == len(enemy.Animationlist) // 2 and self.damageTaken is not 0 and self.damageApplied is False:
            enemy.takeHealth(self.damageTaken) 
            print(f"Damage taken Of hurt state, {self.damageTaken} has been taken from enemy, {enemy.currentHealth}/{enemy.maxHealth} is the enemies current health") 
            self.damageTaken = 0
            self.damageApplied = True
            
            if enemy.currentHealth <= 0:
                enemy.changeState("DIE")

        if enemy.Frame == 0 and self.damageApplied:
            enemy.changeState('IDLE')
            print("Exiting hurt state, going to default state")
            return
        
    def exit(self, enemy=Enemy):
        self.damageTaken = 0
        self.damageApplied = False

class AttackState(State):

    def __init__(self):
        self.attack = None
        self.Attacked = False
        self.RestState = 'REST'

    def changeAttack(self, newAttack):
        self.attack = newAttack

    def enter(self, enemy=Enemy):
        enemy.handleDirection()
        enemy.changeDirection(pygame.Vector2(0,0))
        self.attack = enemy.currentAttack
        enemy.AnimationAction = self.attack.AttackAnimation

        self.attack.enter(enemy)

        if enemy.AttackChargePercentage >= 100:
            enemy.AttackChargePercentage = 0

    def update(self, enemy=Enemy):
        
        if enemy.Frame == len(enemy.Animationlist) // 2 and not self.Attacked:
            self.attack.Attack(enemy.target, enemy.damage)
            self.Attacked = True

        enemy.handleAnimation()

        if self.Attacked and enemy.Frame == 0:
            enemy.changeState(self.RestState)

    def exit(self, enemy=Enemy):
        self.attack.exit(enemy)

        if hasattr(enemy, 'AttackChargePercentage'):
            if hasattr(self.attack, 'chargePercentage'):
                enemy.AttackChargePercentage += self.attack.chargePercentage
                print(f"enemy current charge {enemy.AttackChargePercentage}.")
        self.attack = None
        self.Attacked = False
        enemy.AnimationAction = 'Idle'

        if hasattr(enemy, 'getProjectilesOwnedBySelf'):
            print(enemy.getProjectilesOwnedBySelf(enemy))

# class SpellAttackState(AttackState):
#     def __init__(self):
#         super().__init__()

#     def enter(self, enemy=Enemy):
#         super().enter(enemy)
#         if enemy.currentProjectile is not None:
#             pass

class DeathState(State):

    def enter(self, enemy=Enemy):
        enemy.AnimationAction = 'Death'
        self.AnimationReachedHalf = False #This acts as a signal to check if the animation has been playing for the first time

    def update(self, enemy=Enemy):
        enemy.handleAnimation()
        if enemy.Frame == len(enemy.Animationlist) // 2: self.AnimationReachedHalf = True

        if enemy.Frame == 0 and self.AnimationReachedHalf:
            #HandleDeath
            enemy.Die()

    def exit(self, enemy=Enemy):
        pass

class Attack:
    def __init__(self):
        self.AttackAnimation = 'Attack'

    def Attack(self, target, damage):
        if hasattr(target, 'takeDamage'):
            target.takeDamage(damage)

    def enter(self, enemy=Enemy):
        pass

    def exit(self, enemy=Enemy):
        pass

class BaseAttack(Attack):
    def __init__(self):
        super().__init__()
        self.AttackAnimation = 'Attack01'
        self.chargePercentage = 20

class SpecialAttack(Attack):
    def __init__(self):
        super().__init__()
        self.AttackAnimation = 'Attack02'
        self.chargePercentage = 15
        self.AttackRange = 16

class UltimateAttack(Attack):
    def __init__(self):
        super().__init__()
        self.AttackAnimation = 'Attack03'
        self.chargePercentage = 25

class MultileInferno(BaseAttack):
    def __init__(self):
        super().__init__()
        self.AttackRange = 200

        self.distanceFromSelf = 20
        self.infernos = [
            (10, pygame.Vector2(1,0)),
            (10, pygame.Vector2(-1,0))
        ]

        self.stationaryFor = 1000
        self.intrevals = 300
        self.offset = 1000

    def enter(self, enemy=Enemy):
        self.oldAttackSpeed = enemy.attackCooldown

        highest = 0

        for inferno in self.infernos:
            timeStationary = self.stationaryFor
            offset = inferno[1].normalize() * self.distanceFromSelf
            position = pygame.Vector2(enemy.position + offset)
            if inferno[0] > highest:
                highest = inferno[0]
            for _ in range(inferno[0]):
                enemy.inferno(enemy, position, pygame.Vector2(enemy.target.position - enemy.position).normalize(), stationaryFor=timeStationary, Target=enemy.target)
                timeStationary += self.intrevals

        enemy.nextattackCooldown = (self.stationaryFor + (self.intrevals * highest)) + self.offset

    def exit(self, enemy=Enemy):
        enemy.attackCooldown = self.oldAttackSpeed

    def setInfernos(self, infernos): self.infernos = infernos

class InfernoConvergence(UltimateAttack):
    def __init__(self):
        super().__init__()
        self.distanceFromSelf = 20
        self.AttackRange = 100
    def Attack(self, target, damage):
        pass

    def enter(self, enemy=Enemy):
        directions = [
        pygame.math.Vector2(1, 0),   # Right
        pygame.math.Vector2(0, 1),   # Down
        pygame.math.Vector2(-1, 0),  # Left
        pygame.math.Vector2(0, -1),  # Up
        pygame.math.Vector2(1, 1),   # Down-Right (Diagonal)
        pygame.math.Vector2(-1, 1),  # Down-Left (Diagonal)
        pygame.math.Vector2(-1, -1), # Up-Left (Diagonal)
        pygame.math.Vector2(1, -1),  # Up-Right (Diagonal)
        ] # copied this -_-

        for dire in directions:

            position = enemy.position + (dire.normalize() * self.distanceFromSelf)

            targetDirection = enemy.target.position - position

            targetDirection.normalize()
            
            enemy.infernoConvergence(enemy,enemy.target, pygame.Vector2(position.x, position.y), targetDirection.normalize())
            print(f"{enemy.__class__.__name__} has fire a fire ball toward this direction ({dire})")

    def exit(self, enemy=Enemy):
        # if hasattr(enemy, 'getProjectilesOwnedBySelf'):
        #     projectiles = enemy.getProjectilesOwnedBySelf(enemy)
        #     if projectiles is not None:
        #         for projectile in projectiles:
        #             if hasattr(projectile, 'target'):
        #                 projectile.direction = projectile.target.position - projectile.position
        #                 projectile.direction = pygame.Vector2(projectile.direction).normalize()

        #this all becomes unnecessary if the projectiles themselves redirect themselves towards their target if they have a target
        #im going to do it like that
        pass







#region old
class NewEnemy(pygame.sprite.Sprite): #stats are given in a tuple as follows (health, speed, damage)
    def __init__(self,Type,pos=pygame.math.Vector2,game=Game.Game,stats=tuple, z = LAYERS['ENEMY']):

        super().__init__(game.GetAllSpriteGroup())
        self.type = Type # type is a string to the name of the enemy
        self.game = game
        self.game.addToEnemyGroup(self)
        self.state = "IDLE" #state can be idle and following
        self.maxHealth =int(stats[0])
        self.currentHealth = self.maxHealth
        self.speed = int(stats[1])
        self.damage = int(stats[2])

        self.position = pos
        self.z = z

        self.currentDirection = ""
        self.currentAction = ""
        self.currentAnimationList = []

        self.TimeBeforeChangingToNextAnimationFrame = pygame.time.get_ticks()
        self.CooldownToChangeToNextAnimationFrame = 80
        self.AnimationFrame = 0
        self.directionsList = [pygame.math.Vector2(0,-1).normalize(),
                           pygame.math.Vector2(1,-1).normalize(),
                           pygame.math.Vector2(1,0).normalize(),
                           pygame.math.Vector2(1,1).normalize(),
                           pygame.math.Vector2(0,1).normalize(),
                           pygame.math.Vector2(-1,1).normalize(),
                           pygame.math.Vector2(-1,0).normalize(),
                           pygame.math.Vector2(-1,-1).normalize()]
        #smart ai, this did not go as good as i thought it would -_-
        self.directions = {"up":pygame.math.Vector2(0,-1).normalize(),
                           "down":pygame.math.Vector2(1,-1).normalize(),
                           "left":pygame.math.Vector2(1,0).normalize(),
                           "right":pygame.math.Vector2(1,1).normalize(),
                           "upright":pygame.math.Vector2(0,1).normalize(),
                           "downright":pygame.math.Vector2(-1,1).normalize(),
                           "downleft":pygame.math.Vector2(-1,0).normalize(),
                           "upleft":pygame.math.Vector2(-1,-1).normalize()}
        self.dangeList = [0,0,0,0,0,0,0,0]    
        self.interestList = []

        self.pathfindingTime = pygame.time.get_ticks()
        self.pathfindingCooldown = 2000


        self.allAnimations = {}
        self.LoadActionSpriteSheet()

        randomImage = random.choice(list(self.allAnimations.values()))
        self.image = randomImage[0].convert()
        self.rect = randomImage[0].get_rect(center=(self.position))
        #rayCasts
        self.raycaster = Raycast.Raycaster(self.position,self.game)
        #Collision
        self.CollideRect = self.rect.copy().inflate(self.rect.width * -0.8,self.rect.height * -0.3)
        self.DetectionRect = self.rect.copy().inflate(5, 5)
        self.game.addToCollideGroup(self)
        #idle logic variables
        self.radiusIdle = 100 #radius at which the Skeleton will chose another point in the circle to go to
        self.PointToRoamTo: pygame.math.Vector2
        self.spawnPoint = pos
        self.TimeBeforeChanginPointToRoamTo = pygame.time.get_ticks()
        self.CooldownToLookForAnotherPoint = 30000
        #following logive variables
        self.PlayerPos = pygame.math.Vector2()
        self.TimeBeforeRayCasting = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2()
        #flags
        self.isRoaming = False
        self.isDying = False
        #ui
        self.healthBar = pygame.rect.Rect(self.rect.x,self.rect.y, self.rect.width * 0.8, self.rect.height * 0.05)
        self.healthBarRatio = self.maxHealth/self.healthBar.width
    
    
    def drawHealthBar(self, offset = pygame.math.Vector2, internalSurface = pygame.Surface):
        self.healthBar.x = offset.x + (self.rect.width * 0.1)
        self.healthBar.y = offset.y
        pygame.draw.rect(internalSurface, ("white"), self.healthBar)
        red = self.healthBar.copy()
        red.width = self.currentHealth/(self.maxHealth/self.healthBar.width)
        pygame.draw.rect(internalSurface, ("red"), red)

    def checkDirections(self):
        self.raycaster.resetPos(self.position)
        result = self.raycaster.checkDirections()
        if result is not None: 
            self.dangeList = [0,0,0,0,0,0,0,0]
            count = 0
            for value in result.values():
                onelesscount = count - 1
                onemorecount = count + 1
                if onelesscount < 0:
                    onelesscount = 7
                if onemorecount > 7:
                    onemorecount = 0                    
                if value == True:
                    self.dangeList[count] = 5
                    if self.dangeList[onelesscount] < 2:
                        self.dangeList[onelesscount] = 2
                    if self.dangeList[onemorecount] < 2:
                        self.dangeList[onemorecount] = 2
                count += 1
        return

    def checkRectCollisions(self):
         for sprite in self.game.GetCollideGroup().sprites():
            if self == sprite or type(sprite) == Skeleton:
                #print("found self, code:003")
                continue

            if self.DetectionRect.colliderect(sprite.CollideRect):
                print(self.position)
                print("collision detected")
                print(sprite.rect.center)
                print(type(sprite))


                angle = math.atan2(sprite.CollideRect.centerx - self.position.x, sprite.CollideRect.centery - self.position.y)  * (180 / math.pi)
                print(angle)
    def update(self):
        self.HandleAnimations()
        if self.isDying == False:
            if self.state == "IDLE":
                self.IdleLogic()
                self.HandleIdleMovement()
                self.checkDistanceToPlayer()
            elif self.state == "FOLLOWING":
                self.FollowingLogic()
                self.HandleFollowingMovement()
                self.checkDirections()
    def takeDamage(self, damage):
        self.currentHealth -= damage
        print("enemy took damage:"+ str(self.currentHealth))
        if self.currentHealth <= 0:
            self.die()


    def die(self):
        self.currentAction = "Death"
        self.isDying = True
        self.AnimationFrame = 0
        self.CooldownToChangeToNextAnimationFrame = 150
        print("enemy died")


    def nextLevel(self):
        if len(self.game.GetEnemies()) <= 0:
            #Tiles.LevelFinished(self.game)
            pass 
        return

    def getGridLocation(self):
        return getGridLoc(self.game, self.position)

    def Pathfinding(self, targetLoc = pygame.Vector2):
        pass        

    def FollowingLogic(self):
        return
    def IdleLogic(self):
        
        if pygame.time.get_ticks() > self.TimeBeforeChanginPointToRoamTo:
            self.TimeBeforeChanginPointToRoamTo += self.CooldownToLookForAnotherPoint
            #print("Timer Ticked-Code002")
            self.isRoaming = False
        
        
        if self.isRoaming == True:
            return
        
        pointFound = False
        while pointFound == False:
            startx = int(self.spawnPoint.x - self.radiusIdle)
            endx = int(self.spawnPoint.x + self.radiusIdle)
            starty = int(self.spawnPoint.y - self.radiusIdle)
            endy = int(self.spawnPoint.y + self.radiusIdle)
            #print (startx, endx, starty, endy)
            #a being x b being y and c being the length to it
            #a^2 + b^2 = c^2

            x = random.randint(startx, endx)
            y = random.randint(starty,endy)
            # if (x*x) + (y*y) < (self.radiusIdle*self.radiusIdle):
            pointFound = True
            #print("NewRoamPoint")
            self.PointToRoamTo = pygame.math.Vector2(x, y)
        self.isRoaming = True
        return
#region handles
#false is x true is y
    def HandleCollision(self, whichDirectionToCheckForFirst=bool):
        for sprite in self.game.GetCollideGroup().sprites():
            if self == sprite:
                #print("found self, code:003")
                continue

            
            if self.CollideRect.colliderect(sprite.CollideRect):
                #print("collision detected")
                if whichDirectionToCheckForFirst == False: #do horizontal collision
                    if self.direction.x > 0: #moving right
                        self.CollideRect.right = sprite.CollideRect.left
                        #self.dangeList = [0,2,5,2,0,0,0,0]    
                        #print("collisiom while moving right")
                    if self.direction.x < 0: #moving left
                        self.CollideRect.left = sprite.CollideRect.right
                        #self.dangeList = [0,0,0,0,0,2,5,2]                            
                        #print("collisiom while moving left")
                    self.rect.centerx = self.CollideRect.centerx
                    self.position.x = self.CollideRect.centerx
                if whichDirectionToCheckForFirst:
                    if self.direction.y > 0: #moving down
                        self.CollideRect.bottom = sprite.CollideRect.top
                        #self.dangeList = [0,0,0,2,5,2,0,0]    
                        #print("collisiom while moving down")
                    if self.direction.y < 0: #moving up
                        self.CollideRect.top = sprite.CollideRect.bottom
                        #self.dangeList = [5,2,0,0,0,0,0,2]    
                        #print("collisiom while moving up")

                    self.rect.centery = self.CollideRect.centery
                    self.position.y = self.CollideRect.centery
    def HandleAnimations(self):
        name = self.type
        if self.currentAction == "Death":
            if pygame.time.get_ticks() > self.TimeBeforeChangingToNextAnimationFrame:
                if self.currentAnimationList is not self.allAnimations[name+self.currentDirection+self.currentAction]:
                    self.currentAnimationList = self.allAnimations[name+self.currentDirection+self.currentAction]

                self.TimeBeforeChangingToNextAnimationFrame += self.CooldownToChangeToNextAnimationFrame 
                
                self.AnimationFrame += 1
                self.image = self.currentAnimationList[self.AnimationFrame]

                if self.AnimationFrame >= len(self.currentAnimationList) - 1 :
                    self.AnimationFrame = 0
                    if self.currentAction == "Death":
                        self.kill()
                        self.game.GetPlayer().addGold(int(self.maxHealth/5) * random.randint(1,4))
                        self.nextLevel()
    
            return
        if self.direction.x > 0: 
            self.currentDirection = "Right"
        elif self.direction.x < 0:
            self.currentDirection = "Left"
        elif self.direction.y > 0:
            self.currentDirection = "Down"
        elif self.direction.y < 0:
            self.currentDirection = "Up"
        else:
            #no direction for the first few frames or when the skeleton is idle
            self.currentDirection = "Up"

        if self.direction:
            self.currentAction = "Walk"
        else:
            self.currentAction = "Idle"

        if pygame.time.get_ticks() > self.TimeBeforeChangingToNextAnimationFrame:
            if self.currentAnimationList is not self.allAnimations[name+self.currentDirection+self.currentAction]:
                self.currentAnimationList = self.allAnimations[name+self.currentDirection+self.currentAction]

            self.TimeBeforeChangingToNextAnimationFrame += self.CooldownToChangeToNextAnimationFrame 
            
            self.AnimationFrame += 1
            self.image = self.currentAnimationList[self.AnimationFrame]

            if self.AnimationFrame >= len(self.currentAnimationList) - 1 :
                self.AnimationFrame = 0
                if self.currentAction == "Death":
                    self.kill()
    def HandleFollowingMovement(self):
        self.direction = pygame.math.Vector2(self.game.GetPlayer().position.x - self.position.x, self.game.GetPlayer().position.y - self.position.y)
        if self.direction: self.direction = self.direction.normalize()
        self.interestList = giveDot(self.direction, self.directions.values())

        contextMap = []
        for i in range(0,8):
            contextMap.append(self.interestList[i] - self.dangeList[i])
        #print("printing interestlist dangelist contextmap")
        #print(self.interestList)
        #print(self.dangeList)
        #print(contextMap)
        directions = self.directions.values()
        self.direction = self.directionsList[contextMap.index(max(contextMap))]
        
        self.position += self.direction * self.speed * self.game.GetDeltaTime()

        #horizontal
        self.rect.centerx = round(self.position.x)
        self.CollideRect.centerx = round(self.position.x)
        self.DetectionRect.centerx = round(self.position.x)
        self.HandleCollision(False)

        #vertical
        self.rect.centery = round(self.position.y)
        self.CollideRect.centery = round(self.position.y)
        self.DetectionRect.centery = round(self.position.y)        
        self.HandleCollision(True)

    def HandleIdleMovement(self):

        #check collision against point to roam
        if abs(self.position.x - self.PointToRoamTo.x) < 1 and abs(self.position.y - self.PointToRoamTo.y) < 1:
            #print("roam point reached, recalculating roam point")
            #print(self.position, self.PointToRoamTo)
            self.isRoaming = False
            self.TimeBeforeChanginPointToRoamTo += self.CooldownToLookForAnotherPoint
            self.IdleLogic()

        self.direction = pygame.math.Vector2(self.PointToRoamTo.x - self.position.x, self.PointToRoamTo.y - self.position.y)
        if self.direction: self.direction = self.direction.normalize()
        self.position += self.direction * self.speed * self.game.GetDeltaTime()
        
        #horizontal
        self.rect.centerx = round(self.position.x)
        self.CollideRect.centerx = round(self.position.x)
        self.HandleCollision(False)
        #vertical
        self.rect.centery = round(self.position.y)
        self.CollideRect.centery = round(self.position.y)
        self.HandleCollision(True)

        #print(self.position)
#endregion
    def LoadActionSpriteSheet(self):
        #width and height are both 48
        pixelSize = 48
        mainSubDirectory = "/Enemies/"+self.type 
        subDirectories = [mainSubDirectory+"/Down",mainSubDirectory+"/Up",mainSubDirectory + "/Right", mainSubDirectory + "/Left"]
        currentDirectory = os.getcwd()
        for i in range(len(subDirectories)):
            for file in os.listdir(currentDirectory + subDirectories[i]):
                #print(file)
                image = pygame.image.load(currentDirectory+subDirectories[i]+"/"+file).convert()
                width = image.get_width()
                height = image.get_height()

                framesWidth = int(width/pixelSize)
                framesHeight = height/pixelSize
                
                fileName = file.removesuffix(".png")
                #print(framesWidth)
                fromx = 0
                listOfFrames = []
                for frame in range(framesWidth):
                    fromx += 1
                    surface = pygame.surface.Surface((pixelSize, pixelSize)).convert()
                    surface.blit(image, (0,0), ((fromx * pixelSize) - pixelSize,0, pixelSize, pixelSize))
                    # surface = pygame.transform.scale(surface, (pixelSize*3, pixelSize*3))
                    surface.set_colorkey((255,0,255))
                    listOfFrames.append(surface)

                self.allAnimations[fileName] = listOfFrames

        #print(self.allAnimations)

    def checkDistanceToPlayer(self):
        distanceToCheck = 500
        if abs(self.position.x - self.game.GetPlayer().position.x) < distanceToCheck and abs(self.position.y - self.game.GetPlayer().position.y) < distanceToCheck:
            self.state = "FOLLOWING"
            self.raycaster.TimeBeforeRayCasting = pygame.time.get_ticks()
            #need to check if enemy has line of sight to the player otherwise dont set state


        return
class Skeleton(NewEnemy): 
    def __init__(self,Position=pygame.math.Vector2, game=Game.Game):
        super().__init__("Skeleton", Position, game,(random.randint(15,30), 100, random.randint(2,4)))
        self.scalingOnAttackCooldown = 500
        self.cooldownToHitTarget = 2000

        self.timeBeforeAttacking = pygame.time.get_ticks()

        self.rangeX = self.CollideRect.width/1.2
        self.rangeY = self.CollideRect.height * 1.2

        self.TackleStrength = 100 

        

    def LowerAttackCooldown(self, amount):
        self.cooldownToHitTarget -= amount
        # if self.cooldownToHitTarget < 1000:
        #     self.cooldownToHitTarget = 1000
        #     name = ""
    def HandleAnimations(self):
        name = "SkeletonWithSword"
        if self.currentAction == "Death":
            if pygame.time.get_ticks() > self.TimeBeforeChangingToNextAnimationFrame:
                if self.currentAnimationList is not self.allAnimations[name+self.currentDirection+self.currentAction]:
                    self.currentAnimationList = self.allAnimations[name+self.currentDirection+self.currentAction]

                self.TimeBeforeChangingToNextAnimationFrame += self.CooldownToChangeToNextAnimationFrame 
                
                self.AnimationFrame += 1
                self.image = self.currentAnimationList[self.AnimationFrame]

                if self.AnimationFrame >= len(self.currentAnimationList) - 1 :
                    self.AnimationFrame = 0
                    if self.currentAction == "Death":
                        self.kill()
                        if random.randint(1, 100) > 80:
                            SmallHealthPoition(getPosToGrid(self.game, self.position), self.game)
                        elif random.randint(1,100) > 96: 
                            BigHealthPoition(getPosToGrid(self.game, self.position), self.game)
                        self.game.GetPlayer().addGold(int(self.maxHealth/2) * random.randint(1,4))
                        self.nextLevel()
            return
        if self.currentAction == "Attack01":
            if pygame.time.get_ticks() > self.TimeBeforeChangingToNextAnimationFrame:
                if self.currentAnimationList is not self.allAnimations[name+self.currentDirection+self.currentAction]:
                    self.currentAnimationList = self.allAnimations[name+self.currentDirection+self.currentAction]

                self.TimeBeforeChangingToNextAnimationFrame += self.CooldownToChangeToNextAnimationFrame 
                
                self.AnimationFrame += 1
                self.image = self.currentAnimationList[self.AnimationFrame]

                if self.AnimationFrame == round(len(self.currentAnimationList)/2):
                    self.Attack()

                if self.AnimationFrame >= len(self.currentAnimationList) - 1 :
                    self.AnimationFrame = 0
                    self.currentAction = "Idle"
            return
        
        if self.direction.x > 0: 
            self.currentDirection = "Right"
        elif self.direction.x < 0:
            self.currentDirection = "Left"
        elif self.direction.y > 0:
            self.currentDirection = "Down"
        elif self.direction.y < 0:
            self.currentDirection = "Up"
        else:
            #no direction for the first few frames or when the skeleton is idle
            self.currentDirection = "Up"

        if self.direction:
            self.currentAction = "Run"
        else:
            self.currentAction = "Idle"

        if pygame.time.get_ticks() > self.TimeBeforeChangingToNextAnimationFrame:
       
            
            if self.currentAnimationList is not self.allAnimations[name+self.currentDirection+self.currentAction]:
                self.currentAnimationList = self.allAnimations[name+self.currentDirection+self.currentAction]

            self.TimeBeforeChangingToNextAnimationFrame += self.CooldownToChangeToNextAnimationFrame 
            
            self.AnimationFrame += 1
            self.image = self.currentAnimationList[self.AnimationFrame]

            if self.AnimationFrame >= len(self.currentAnimationList) - 1 :
                self.AnimationFrame = 0


            #print("animation frame is bigger than animation frame")
    

    def FollowingLogic(self):
        self.IsSkeletonInRange()

    def Attack(self):
        if abs(self.position.x - self.game.GetPlayer().position.x) < self.rangeX and abs(self.position.y - self.game.GetPlayer().position.y) < self.rangeY:
            if "Attack" in self.currentAction:
                self.game.GetPlayer().takeDamage(self.damage)


    def IsSkeletonInRange(self):
        if abs(self.position.x - self.game.GetPlayer().position.x) < self.rangeX and abs(self.position.y - self.game.GetPlayer().position.y) < self.rangeY:
            if pygame.time.get_ticks() > self.timeBeforeAttacking:
                self.timeBeforeAttacking += self.cooldownToHitTarget
                self.currentAction = "Attack01"
        return 
class SpawnerSkeleton(Skeleton):
    def __init__(self, Position=pygame.math.Vector2, game=Game.Game, spawner=any):
        print(Position, game, spawner)
        super().__init__(Position, game)
        self.ParentSpawner = spawner

    def die(self):
        self.currentAction = "Death"
        self.isDying = True
        self.AnimationFrame = 0
        self.CooldownToChangeToNextAnimationFrame = 150
        print("enemy died")
        #check for parent spawner
        self.CheckParentSpawner()

    def CheckParentSpawner(self):
        self.ParentSpawner.numOfEnemies -= 1
        if self.ParentSpawner.numOfEnemies <= 0:
            print("Spawner to be removed")
            self.game.removeSpawner(self.ParentSpawner)
            print("spawner removed from spawner list")
        else:
            print("skeletons left in this spawner: " + str(self.ParentSpawner.numOfEnemies))
        return
#endregion





