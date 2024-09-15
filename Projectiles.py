import pygame, math, random
from Settings import LAYERS

class ProjectileManager:
    def __init__(self, game):
        self.game = game
        self.game.SetProjectileManager(self)

        #spritesheets
        self.FireSpriteSheet = pygame.image.load("Projectiles\Fire\Grouped.png").convert_alpha()

        self.Animations = {} #name of thing gives its animations
        self.loadAllAnimations()

        self.Projectiles = pygame.sprite.Group()
        self.ownersAndProjectiles = {}

        self.timeToCheckCollision = pygame.time.get_ticks()
        self.cooldownToCheckCollision = 20

        self.game.addUpdateFunc(self.update)
    def update(self):
        self.checkCollisions()

    def loadAllAnimations(self):
        self.loadFireBall()


    def loadFromFireSpriteSheet(self, pixelSize, XPosition, YPosition, Frames, nameInDic):

        startX = pixelSize * XPosition
        startY = pixelSize * YPosition

    def loadFireBall(self):
        xFrame, yFrame = 0,8
        TileSize = 64
        totalFrames = 4

        listOfFrame = []
        for i in range(totalFrames):
            surface = pygame.surface.Surface((TileSize, TileSize)).convert_alpha()
            surface.blit(self.FireSpriteSheet, (0,0), ((xFrame + i) * TileSize,yFrame * TileSize, TileSize,  TileSize))
            surface = pygame.transform.scale(surface, (16,16))
            surface.set_colorkey((0,0,0))
            listOfFrame.append(surface)
        
        self.Animations['FIREBALL'] = listOfFrame

    def addProjectile(self, item):
        self.game.GetAllSpriteGroup().add(item)
        self.Projectiles.add(item)

    
    def removeProjectile(self, item):
        self.Projectiles.remove(item)
        self.game.GetAllSpriteGroup().remove(item)

    def createFireball(self, Owner, Position=pygame.Vector2, Direction=pygame.Vector2):
        self.addProjectile(FireBall(Position, Direction, self.Animations['FIREBALL'], self, animationCooldown=70, speed=300, owner=Owner))

    def createTimedFireball(self, Owner, Position=pygame.Vector2, Direction=pygame.Vector2, stationaryFor=1000):
        self.addProjectile(TimedFireBall(Position, Direction, self.Animations['FIREBALL'], self, animationCooldown=70, speed=200, owner=Owner,stationaryFor=stationaryFor))

    def createTargetedTimedFireball(self, Owner, target, Position=pygame.Vector2, Direction=pygame.Vector2, stationaryFor=1000):
        self.addProjectile(TargetedTimedFireBall(Position, Direction, self.Animations['FIREBALL'], self, \
                                                 animationCooldown=70, speed=200, owner=Owner,stationaryFor=stationaryFor,target=target))

    def createTargetTimedFireball(self, Owner, Position=pygame.Vector2,Direction=pygame.Vector2,Target=any, stationaryFor=1000):
        self.addProjectile(TargetTimedFireBall(Position, Direction, self.Animations['FIREBALL'], self, animationCooldown=70, speed=200, owner=Owner,stationaryFor=stationaryFor, target=Target))


    def checkCollisions(self):
        currentTime = pygame.time.get_ticks()
        if currentTime > self.timeToCheckCollision:
            self.timeToCheckCollision = currentTime + self.cooldownToCheckCollision 
            if self.Projectiles:
                for proj in self.Projectiles.sprites():
                    for collision in self.game.GetCollideGroup().sprites():
                        if proj.rect.colliderect(collision.CollideRect):
                            if collision is not proj.owner and collision not in self.Projectiles:
                                proj.Collided(collision)
                                print(f"{proj} projectile collided with {collision}, {collision} should not be a projectile itself.")


class Projectile(pygame.sprite.Sprite):
    def __init__(self, Position=pygame.Vector2, direction=pygame.Vector2,ListOfFrames=[],projectileManager=ProjectileManager,lifeSpan=100,animationCooldown=15,speed =50,owner=any, z = LAYERS['PROJECTILES']):
        super().__init__() 
        self.owner = owner
        self.position = Position
        self.direction = direction
        self.z = z
        self.lifeSpan = lifeSpan
        self.speed = speed

        #animation variables
        self.Animations = ListOfFrames
        self.timeForFrame = pygame.time.get_ticks()
        self.cooldownForFrame = animationCooldown
        self.frame = 0
        self.maxFrame = len(ListOfFrames)

        #sprite variables
        self.image = self.Animations[0]
        self.rect = self.image.get_rect(center=self.position)

        self.projectileManager = projectileManager
        self.game = self.projectileManager.game

        #add reference of projectile to the owner in the dic in projectilemanager
        if owner not in projectileManager.ownersAndProjectiles:
            listOfProjectiles = [self]
            projectileManager.ownersAndProjectiles[owner] = listOfProjectiles
        else: #owner is in the dic
            listOfProjectiles = projectileManager.ownersAndProjectiles[owner]
            listOfProjectiles.append(self)
            projectileManager.ownersAndProjectiles[owner] = listOfProjectiles


    def update(self):
        if pygame.time.get_ticks() > self.timeForFrame:
            self.timeForFrame += self.cooldownForFrame
            self.frame += 1
            self.lifeSpan -= 1
            if self.frame >= self.maxFrame:
                self.frame = 0
            if self.frame < self.maxFrame: 
                # print(self.frame)
                self.image = self.Animations[self.frame]

        self.MoveProjectile()
        

        if self.lifeSpan <= 0:
            self.killProjectile()

    def MoveProjectile(self):
        if type(self.direction) is not pygame.Vector2:
            print(f"Error, projectile direction is {self.direction}. not moving projectile. type is {type(self.direction)}")
            return
        self.position += self.direction * self.game.GetDeltaTime() * self.speed
        self.rect.center = self.position

    def Collided(self, collidedWith):

        try: 
            collidedWith.takeDamage(self.owner.damage)
        except:
            print(f"{self.owner} sent a projectile that collided with {collidedWith}, no damage to be calculated")
        
        self.killProjectile()

    def killProjectile(self):
        if self in self.projectileManager.ownersAndProjectiles[self.owner]:
            self.projectileManager.ownersAndProjectiles[self.owner].remove(self)
        self.projectileManager.removeProjectile(self)

class TimedProjectile(Projectile):
    def __init__(self, Position=pygame.Vector2, direction=pygame.Vector2, ListOfFrames=[], projectileManager=ProjectileManager, lifeSpan=100, animationCooldown=15, speed=50, owner=any, z=LAYERS['PROJECTILES'], stationaryFor=1000):
        super().__init__(Position, direction, ListOfFrames, projectileManager, lifeSpan, animationCooldown, speed, owner, z)
        self.projectileMadeAt = pygame.time.get_ticks()
        self.stationaryFor = stationaryFor
        self.timeToMove = self.projectileMadeAt + self.stationaryFor

        self.Stationary = True

    def update(self):
        if pygame.time.get_ticks() > self.timeForFrame:
            self.timeForFrame += self.cooldownForFrame
            self.frame += 1
            self.lifeSpan -= 1
            if self.frame >= self.maxFrame:
                self.frame = 0
            if self.frame < self.maxFrame: 
                # print(self.frame)
                self.image = self.Animations[self.frame]

        if pygame.time.get_ticks() > self.timeToMove:
            self.MoveProjectile()
            if self.Stationary is True: self.Stationary = False
            # print(f"{self} projectile is moving, its owner is {self.owner}, current position is {self.position}")

        if self.lifeSpan <= 0:
            self.killProjectile()



class FireBall(Projectile):
    def __init__(self, Position=pygame.Vector2, Direction=pygame.Vector2,ListOfFrames=[],ProjectileManager=ProjectileManager,lifeSpan=100,animationCooldown=15,speed = 100,z = LAYERS['PROJECTILES'], owner=any):
        super().__init__(Position, Direction, ListOfFrames, ProjectileManager, lifeSpan=lifeSpan, animationCooldown=animationCooldown,speed=speed, z=z, owner=owner)
        
class TimedFireBall(TimedProjectile):
    def __init__(self, Position=pygame.Vector2, Direction=pygame.Vector2,ListOfFrames=[],ProjectileManager=ProjectileManager,lifeSpan=100,animationCooldown=15,speed = 100,z = LAYERS['PROJECTILES'], owner=any, stationaryFor=1000):
        super().__init__(Position, Direction, ListOfFrames, ProjectileManager, lifeSpan=lifeSpan, animationCooldown=animationCooldown,speed=speed, z=z, owner=owner,stationaryFor=stationaryFor)

class TargetTimedFireBall(TimedFireBall):
    def __init__(self, Position=pygame.Vector2, Direction=pygame.Vector2,ListOfFrames=[],ProjectileManager=ProjectileManager,lifeSpan=100,\
                 animationCooldown=15,speed = 100,z = LAYERS['PROJECTILES'], owner=any, stationaryFor=1000,target=any):
        print("printing direction values")
        print(pygame.Vector2(target.position - Position).normalize())
        print(Direction)
        super().__init__(Position, Direction, ListOfFrames, ProjectileManager, lifeSpan=lifeSpan, animationCooldown=animationCooldown,speed=speed, z=z, owner=owner,stationaryFor=stationaryFor)
        self.target = target

        self.position = pygame.Vector2(Position)

        if self.target is not None:
            self.direction = pygame.Vector2(target.position - self.position).normalize()

    def update(self):
        super().update()
        if self.Stationary and self.target is not None:
            self.direction = pygame.Vector2(self.target.position - self.position).normalize() 
    

class TargetedTimedFireBall(TimedFireBall):
    def __init__(self, Position=pygame.Vector2, Direction=pygame.Vector2, ListOfFrames=[], ProjectileManager=ProjectileManager,lifeSpan=100, animationCooldown=15, speed=100, z=LAYERS['PROJECTILES'], owner=any, stationaryFor=1000, target=any, minStrafeAngle=math.pi/6, maxStrafeAngle=math.pi/3):
        super().__init__(Position, Direction, ListOfFrames, ProjectileManager, lifeSpan, animationCooldown, speed, z, owner, stationaryFor)
        self.target = target
        self.minStrafeAngle = minStrafeAngle #the default min strafe is 30 degrees, this can all be changed
        self.maxStrafeAngle = maxStrafeAngle # the default max strafe is 60 degrees
        self.strafeAngle = random.uniform(self.minStrafeAngle, self.maxStrafeAngle) 

        self.howOftenToUpdateDirection = 10
        self.lastTimeRedirected = pygame.time.get_ticks()
        
        self.stillStationary = True

    def update(self):
        super().update()

        if pygame.time.get_ticks() > self.lastTimeRedirected:
            targetDirection = pygame.Vector2(self.target.position - self.position).normalize()
            self.direction = self.calculateStrafeDirection(targetDirection)
            self.lastTimeRedirected += self.howOftenToUpdateDirection

    def calculateStrafeDirection(self, targetDirection):
        angle = random.uniform(-self.strafeAngle, self.strafeAngle)
        strafeDirection = pygame.Vector2(
            targetDirection.x * math.cos(angle) - targetDirection.y * math.sin(angle),
            targetDirection.x * math.sin(angle) + targetDirection.y * math.cos(angle)
        ).normalize()
        return strafeDirection
    
    def MoveProjectile(self):
        super().MoveProjectile()
        if self.stillStationary == True:
            self.stillStationary = False
            self.direction = pygame.Vector2(self.target.position - self.position).normalize()