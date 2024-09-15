import pygame, Enemy, Game, os
from Settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, PositionX, PositionY, group=pygame.sprite.Group, game=Game.Game, z = LAYERS['PLAYER']):
        super().__init__(group)
        self.z = z
        self.image = None
        self.game = game
        #self.image.set_colorkey((0,0,0))
        self.PositionX = PositionX
        self.PositionY = PositionY
        #stats
        self.maxHealth = 0
        self.currentHealth = self.maxHealth
        self.damage = 0
        self.gold = 0
        self.speed = 0
        self.MaxSpeed = 5000
        self.mapProgression = 0
        #load
        self.loadAllStats()
        #Collisions

        self.isGrounded = False
        self.direction = pygame.math.Vector2()
        #flags
        self.isAttacking = False
        self.isDead = False
        self.ContinuesAttack = False
        # -1 means left 0 means idle 1 means right 2 means top
        self.idleDirection = 0
        
        self.attackCounter = 1

        self.spriteSize = 48
        #Action Cooldowns
        self.attackInTime = 0
        self.attackCooldown = 1000
        self.LookForClosestSpawnerIn = 3000
        #Clock
        self.animationFrame = 0
        self.ConstantForAnimationAttackSpeed = 25000
        self.AnimationSpeedWhenAttacking = 200 - (self.ConstantForAnimationAttackSpeed / self.attackCooldown) 
        self.AnimationCooldown = 80 #this is in ms
        self.AnimationCooldownBackup = self.AnimationCooldown
        self.AnimationSpeedNMinimum = 120
        self.AnimationSpeedMaximum = 20 
        self.NextAnimationIn = pygame.time.get_ticks()
        self.CheckForSpawnerIn = pygame.time.get_ticks()
        self.HandleAnimationSpeed()
        #Animation
        self.name = "Warrior"
        self.currentDirection = "Down"
        self.currentAction = "Idle"
        self.current_AnimationList = []
        self.AllAnimations = {}
        self.loadAnimation()
        #limits
        self.maxx = 32 * 50
        self.minx = 0
        self.maxy = 32 * 50
        self.miny = 0
        #LISTS
        self.EnemiesToReset = [Enemy.Enemy]
        #region ui
        self.screen = pygame.display.get_surface()
        self.HealthBarRect = pygame.rect.Rect(self.screen.get_width() * 0.2, self.screen.get_height() *0.9,self.screen.get_width() * 0.6, 10)
        self.HealthBarRectOutline = pygame.rect.Rect((self.screen.get_width() * 0.2)-1, (self.screen.get_height() *0.9) - 1,(self.screen.get_width() * 0.6) + 2, 12)
        self.redHealthBarRect = pygame.rect.Rect(self.screen.get_width() * 0.2, self.screen.get_height() *0.9,self.screen.get_width() * 0.6, 10)
        self.healthBarRatio = self.maxHealth/ self.HealthBarRect.width
        self.font = pygame.font.Font("Font\ARCADECLASSIC.TTF", 50)
        self.textFont = pygame.font.Font("Font\TEXT.TTF", 11)
        self.font.set_bold(True)
        self.goldText = self.font.render(str(self.gold),True, (255, 215, 0))
        self.goldRect = self.goldText.get_rect(midbottom=self.HealthBarRect.midtop)
        self.hp = str(self.currentHealth) + '|' + str(self.maxHealth)
        self.hpText = self.textFont.render(self.hp, True, ("white"))
        self.textRect = self.hpText.get_rect(midtop= self.HealthBarRect.midtop)
        self.screen = pygame.display.get_surface()
        self.ClosestSpawnerVector = None
        #endregion ui

        #Player SURFACE
        self.image = self.AllAnimations[self.name+self.currentDirection+self.currentAction][self.animationFrame]
        self.rect = self.image.get_rect(center=(self.PositionX,self.PositionY))
        self.position = pygame.math.Vector2(self.PositionX, self.PositionY)
        self.mask = pygame.mask.from_surface(self.image)

        print("Player position " + str(self.position))
        #moreAccurateHitbox = 26
        #self.CollideRect = pygame.rect.Rect(self.rect.x + self.rect.width/4 + moreAccurateHitbox/2, self.rect.y + self.rect.height/2 - 15, self.rect.width/2 - moreAccurateHitbox, self.rect.height/2)
        self.CollideRect = self.rect.copy().inflate(self.rect.width * -0.8,self.rect.height * -0.3)

        self.CenterRect = pygame.rect.Rect(self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2), 5,5)
    def update(self):
        if self.isDead == False:
            if pygame.time.get_ticks() > self.CheckForSpawnerIn: 
                self.CheckForSpawnerIn += self.LookForClosestSpawnerIn
                self.game.setClosestSpawner()
            self.handleUI()
            self.input()
            self.AnimationUpdate()
            if self.checkPosition() and self.isAttacking == False:
                self.HandleMovement()                
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[KEYBINDS['WALKUP']]:
             self.direction.y = -1
             self.idleDirection = 2
        elif keys[KEYBINDS['WALKDOWN']]:
             self.direction.y = 1
             self.idleDirection = 0
        else:
             self.direction.y = 0
        if keys[KEYBINDS['WALKRIGHT']]:
             self.direction.x = 1
             self.idleDirection = 1
        elif keys[KEYBINDS['WALKLEFT']]:
             self.direction.x = -1
             self.idleDirection = -1
        else:
             self.direction.x = 0 
        if self.direction: self.direction = self.direction.normalize()

    #region handles
    def HandleMovement(self):
        
        self.position += self.direction * self.speed * self.game.GetDeltaTime()

        #handle horizontal
        self.rect.centerx = round(self.position.x)
        self.CollideRect.centerx = round(self.position.x)
        self.CenterRect.centerx = round(self.position.x) 
        self.HandleCollision(False)

        #handle vertical
        self.rect.centery = round(self.position.y)
        self.CollideRect.centery = round(self.position.y)
        self.CenterRect.centery = round(self.position.y)
        self.HandleCollision(True)
        #i am assigning the position of the collide rect like this to account for the player's head being drawn from the middle of the sprite not where the middle of the player
        #in short in the sprite sheet i am using, the player starts being drawn from the center of the sprite. so i have to assign this like this to account for that
        #self.CollideRect.midtop = round(self.position)

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
                        #print("collisiom while moving right")
                    if self.direction.x < 0: #moving left
                        self.CollideRect.left = sprite.CollideRect.right
                        #print("collisiom while moving left")
                    self.rect.centerx = self.CollideRect.centerx
                    self.CenterRect.centerx = self.CollideRect.centerx
                    self.position.x = self.CollideRect.centerx

                if whichDirectionToCheckForFirst:
                    if self.direction.y > 0: #moving down
                        self.CollideRect.bottom = sprite.CollideRect.top
                        #print("collisiom while moving down")
                    if self.direction.y < 0: #moving up
                        self.CollideRect.top = sprite.CollideRect.bottom
                        #print("collisiom while moving up")
                    self.rect.centery = self.CollideRect.centery
                    self.CenterRect.centery = self.CollideRect.centery
                    self.position.y = self.CollideRect.centery

    def getGame(self):
        return self.game

    #endregion 
    def AnimationUpdate(self):
        
        if self.direction.x > 0:
            self.currentDirection = "Right"
        elif self.direction.x < 0:
            self.currentDirection = "Left"
        elif self.direction.y > 0:
            self.currentDirection = "Down"
        elif self.direction.y < 0:
            self.currentDirection = "Up"

        if self.direction:
            self.currentAction = "Walk"
        else:
            self.currentAction = "Idle"


        if self.isAttacking:
            if self.attackCounter > 3:
                self.attackCounter = 1
            self.currentAction = "Attack0" + str(self.attackCounter)
        try:

            if self.current_AnimationList != self.AllAnimations[self.name+self.currentDirection+self.currentAction]: 
                self.current_AnimationList = self.AllAnimations[self.name+self.currentDirection+self.currentAction]
        except:
            print("Animation is not installed:" + str(self.current_action))


        if pygame.time.get_ticks() > self.NextAnimationIn:
            if self.animationFrame <= len(self.current_AnimationList) - 1:
                self.image = self.current_AnimationList[self.animationFrame]
            self.animationFrame += 1
            self.NextAnimationIn += self.AnimationCooldown

            if "Attack" in self.currentAction:
                if self.animationFrame == round(len(self.current_AnimationList)/2):
                    self.AttackEnemies()

        if self.animationFrame >= len(self.current_AnimationList) - 1:
            self.animationFrame = 0
            if self.isAttacking:
                self.isAttacking = False
                self.AnimationCooldown = self.AnimationCooldownBackup
    
    def checkPosition(self):
        if self.CollideRect.right > self.maxx:
            self.MovePlayer(-1,0)
            #print("player collided with boarder on the max x, player xy is:" + str(self.CollideRect.x) + ":" + str(self.CollideRect.y))
            return False
        if self.CollideRect.left <  self.minx:
            self.MovePlayer(1,0)
            #print("player collided with boarder on the min x, player xy is:" + str(self.CollideRect.x) + ":" + str(self.CollideRect.y))
            return False
        if self.CollideRect.bottom > self.maxy:    
            self.MovePlayer(0,1)
            #print("player collided with boarder on the max y, player xy is:" + str(self.CollideRect.x) + ":" + str(self.CollideRect.y))            
            return False
        if self.CollideRect.top < self.miny:
            self.MovePlayer(0,-1)

            #print("player collided with boarder on the min y, player xy is:" + str(self.CollideRect.x) + ":" + str(self.CollideRect.y))
            return False
        return True
   
    def createShockwaveForAttack(self, pixelSize, size):
        self.game.GetParticleSystem().createShockwave(self.position, pixelSize, size)
    
    def AttackEnemies(self):
        for enemy in self.game.GetEnemies().sprites():

            xRange = self.image.get_width()
            yRange = self.image.get_height()

            damageToBeApplied = self.damage

            if "02" in self.currentAction:
                damageToBeApplied *= 1.5
                # if self.currentDirection == "Up":
                #     yRange *= 1.2 
                #     #print("ATTACK 03 AMPD")
                # elif self.currentDirection == "Down":
                #     yRange *= 1.2
                #     #print("ATTACK 03 AMPD")
                # elif self.currentDirection == "Left":
                #     xRange *= 1.2
                #    # print("ATTACK 03 AMPD")
                # elif self.currentDirection == "Right":
                #     xRange *= 1.2
                #     #print("ATTACK 03 AMPD")

                

            if "03" in self.currentAction:
                damageToBeApplied *= 0.7
                if self.currentDirection == "Up":
                    yRange *= 1.5 
                    #print("ATTACK 03 AMPD")
                elif self.currentDirection == "Down":
                    yRange *= 1.5
                    #print("ATTACK 03 AMPD")
                elif self.currentDirection == "Left":
                    xRange *= 1.5
                   # print("ATTACK 03 AMPD")
                elif self.currentDirection == "Right":
                    xRange *= 1.5
                    #print("ATTACK 03 AMPD")




            if self.currentAction == "Attack01":
                xRange *= 1.3
                yRange *= 1.3

            if abs(self.position.x - enemy.position.x) < xRange and abs(self.position.y - enemy.position.y) < yRange:   
                facing = False
                directionVector = enemy.position - self.position
                if directionVector:
                    directionVector.normalize()

                vectorFacing = None
                if self.currentDirection in DIRECTIONS:
                    vectorFacing = DIRECTIONS[self.currentDirection]
                else:
                    print(f"{self.currentDirection} is not in the directions dic, fix it")
                    for _ in range(50):
                        print("Error in the players attack enemy method")
                        print(f"{self.currentDirection} is not in the directions dic, fix it")
                
                if vectorFacing:
                    print(f"Found a facing vector {vectorFacing}")
                    if vectorFacing.dot(directionVector) > (1 - PlayerFacingTolerance):
                        print(f"Player facing in the same direction as the enemy {vectorFacing.dot(directionVector)}")
                        facing = True                        

                if facing:
                    print("Player facing enemy")
                    try:
                        print("enemy attacked")
                        enemy.takeDamage(int(damageToBeApplied))
                    except:
                        print("")



    def Attack(self):
        if self.isAttacking == False and pygame.time.get_ticks() > self.attackInTime:
            self.animationFrame = 0    
            self.isAttacking = True
            self.AnimationCooldown = self.AnimationSpeedWhenAttacking
            self.attackCounter +=1
            self.attackInTime = pygame.time.get_ticks() + self.attackCooldown




    def getAnimationFrame(self, spritesheet, y, frames, width, height, animationNameInCaps, flip:bool):
        list = []
        for frame in range(frames):
            surface = pygame.Surface((width, height)).convert()
            surface.set_colorkey((0,0,0))
            surface.blit(spritesheet, (0,0), ((width * frame),(height * y), width, height))
            # surface = pygame.transform.scale(surface, (width * 3, height * 3))
            if flip:
                surface = pygame.transform.flip(surface, True, False)            
            surface.set_colorkey((0,0,0))
            list.append(surface)
        self.AllAnimations[animationNameInCaps] = list
        
    def ResetEnemyDamageVulnerability(self, enemy):
        if self.ContinuesAttack == False: self.EnemiesToReset.append(enemy)
    def moveGravity(self):
        self.direction.y = -1
    #region get and sets for player (encapsulation)
    def getSpeed(self):
        return self.speed
    def setSpeed(self, num):
        self.speed = num
    def addGold(self, num):
        self.gold += num
        self.goldText = self.font.render(str(self.gold),True, (255, 215, 0))
        self.goldRect = self.goldText.get_rect(midbottom=self.HealthBarRect.midtop)
    def getGold(self):
        return self.gold
    def takeGold(self, num):
        if self.gold < num:
            print("not enough gold")
            return
        self.gold -= num
        self.goldText = self.font.render(str(self.gold),True, (255, 215, 0))
        self.goldRect = self.goldText.get_rect(midbottom=self.HealthBarRect.midtop)
    def IncreaseAttackDamage(self, increase):
        if increase < 0:
            print(KeyError("Increase is negative on damage increase"))
            return
        self.damage += increase
    def IncreaseSpeed(self, increase):
        if increase < 0:
            print(KeyError("increase is negative on speed increase"))
            return
        self.speed += increase
        # if self.speed > self.MaxSpeed: self.speed = self.MaxSpeed
        self.HandleAnimationSpeed()

    def takeDamage(self, damage):
        if self.currentHealth <= 0:
            self.death()
            return
        self.currentHealth -= damage
        if self.currentHealth < 0:
            self.currentHealth = 0
            self.death()
        print("Player took damage:" + str(self.currentHealth) + "/" + str(self.maxHealth))
    def IncreaseMaxHealth(self, IncreaseOnMaxHealth):
        if IncreaseOnMaxHealth > 0:
            self.maxHealth += IncreaseOnMaxHealth
            self.currentHealth += IncreaseOnMaxHealth
            self.healthBarRatio = self.maxHealth/ self.HealthBarRect.width

            return
        else: 
            print("negative increase?")
        print("negative max health?")
    def getMaxHealth(self):
        return self.maxHealth    
    def getCurrentHealth(self):
        return self.currentHealth
    def heal(self, healAmount):
        if self.currentHealth + healAmount > self.maxHealth:
            self.currentHealth = self.maxHealth
            return
        self.currentHealth += healAmount
    def death(self):
        self.isDead = True
        #handle death
    #endregion
    def MovePlayer(self,x,y):
        self.position.x += x * self.speed * self.game.GetDeltaTime()
        self.position.y -= y * self.speed * self.game.GetDeltaTime()
        self.HandleMovement()
#region Load
    def loadAllStats(self):
        try:
            file = open(r"stats\stats.txt", "r")
            for line in file:
                lineSPlit = line.split(":")
                typeOfStats = str(lineSPlit[0])
                magOfStats = int(lineSPlit[1])

                if typeOfStats == "SPEED":
                    self.speed = magOfStats
                elif typeOfStats == "GOLD":
                    self.gold = magOfStats
                elif typeOfStats == "DAMAGE":
                    self.damage = magOfStats
                elif typeOfStats == "HEALTH":
                    self.maxHealth = magOfStats
                elif typeOfStats == "CURRENTHEALTH":
                    if magOfStats <= self.maxHealth: self.currentHealth = magOfStats
                else:
                    print("stat unknown: " + typeOfStats)

            file.close()
        except:
            
            try:
                file = open(r"stats\stats.txt", "x")
            except:
                print("file exists")
            #default stats
            file = open(r"stats\stats.txt", "a")
            file.write("DAMAGE:10\n")
            file.write("SPEED:250\n")
            file.write("HEALTH:100\n")
            file.write("CURRENTHEALTH:100\n")
            file.write("GOLD:0\n")
            try:
                file = open(r"stats\stats.txt", "r")
                for line in file:
                    lineSPlit = line.split(":")
                    typeOfStats = str(lineSPlit[0])
                    magOfStats = int(lineSPlit[1])

                    if typeOfStats == "SPEED":
                        self.speed = magOfStats
                    elif typeOfStats == "GOLD":
                        self.gold = magOfStats
                    elif typeOfStats == "DAMAGE":
                        self.damage = magOfStats
                    elif typeOfStats == "HEALTH":
                        self.maxHealth = magOfStats
                    elif typeOfStats == "CURRENTHEALTH":
                        if magOfStats <= self.maxHealth: self.currentHealth = magOfStats
                    else:
                        print("stat unknown: " + typeOfStats)

                file.close()
            except:
                print("Error loading stats")

    def HandleAnimationSpeed(self):

        self.AnimationSpeedWhenAttacking = 130 - (self.ConstantForAnimationAttackSpeed/self.attackCooldown)

        self.AnimationCooldown = self.AnimationSpeedNMinimum - (self.speed * 0.4)

        if self.AnimationSpeedWhenAttacking < 40: self.AnimationSpeedWhenAttacking = 40
        if self.AnimationCooldown < self.AnimationSpeedMaximum: self.AnimationCooldown = self.AnimationSpeedMaximum
        self.AnimationCooldownBackup = self.AnimationCooldown
        pass
    def loadAnimation(self):

        #this loads in the old player sprite sheet.
        #PlayerAnimationSpriteSheet = pygame.image.load('Images\Spritesheets\player.png')

        #self.getAnimationFrame(PlayerAnimationSpriteSheet,0,6,48,48,"IDLE", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,1,6,48,48,"IDLERIGHT", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,1,6,48,48,"IDLELEFT", True)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,2,6,48,48,"IDLEUP", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,3,6,48,48,"WALKUP", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,4,6,48,48,"WALKRIGHT", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,4,6,48,48,"WALKLEFT", True)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,5,6,48,48,"WALKDOWN", True)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,6,4,48,48,"ATTACK", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,7,4,48,48,"ATTACKRIGHT", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,7,4,48,48,"ATTACKLEFT", True)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,8,4,48,48,"ATTACKUP", False)
        #self.getAnimationFrame(PlayerAnimationSpriteSheet,9,3,48,48,"DEATH", False)

        self.LoadActionSpriteSheet()
    
    def saveGold(self):
        with open(r"stats\stats.txt", 'r') as file:
            lines = file.readlines()
        
        lineNum = 0
        for line in lines:
            lineSPlit = line.split(":")
            typeOfStats = str(lineSPlit[0])
            if typeOfStats == "GOLD":
                lineNum = lines.index(line)

        if 0 <= lineNum < len(lines):
            lines[lineNum] = "GOLD:" + str(self.gold) + '\n'  
            with open(r"stats\stats.txt", 'w') as file:
                file.writelines(lines)
                
    def saveMaxHealth(self):
        with open(r"stats\stats.txt", 'r') as file:
            lines = file.readlines()
        
        lineNum = 0
        for line in lines:
            lineSPlit = line.split(":")
            typeOfStats = str(lineSPlit[0])
            if typeOfStats == "HEALTH":
                lineNum = lines.index(line)

        if 0 <= lineNum < len(lines):
            lines[lineNum] = "HEALTH:" + str(self.maxHealth) + '\n'  
            with open(r"stats\stats.txt", 'w') as file:
                file.writelines(lines)
    def saveAllStats(self):
        with open(r"stats\stats.txt", 'w') as file:

            file.write("HEALTH:" + str(self.maxHealth) + '\n')
            file.write("CURRENTHEALTH:" + str(self.currentHealth) + '\n')            
            file.write("DAMAGE:" + str(self.damage) + '\n')
            file.write("SPEED:" + str(self.speed) + '\n')
            file.write("GOLD:" + str(self.gold) + '\n')
            
            file.close()
    #Custom method for loading in animations that are sparated by action in a folder
    def LoadActionSpriteSheet(self):
        #width and height are both 48
        pixelSize = 48
        subDirectories = ["/Animations/Down","/Animations/Up","/Animations/Right", "/Animations/Left"]
        currentDirectory = os.getcwd()
        for i in range(len(subDirectories)):
            for file in os.listdir(currentDirectory + subDirectories[i]):
                print(file)
                image = pygame.image.load(currentDirectory+subDirectories[i]+"/"+file).convert()
                width = image.get_width()
                height = image.get_height()

                framesWidth = int(width/pixelSize)
                framesHeight = height/pixelSize
                
                fileName = file.removesuffix(".png")
                print(framesWidth)
                fromx = 0
                listOfFrames = []
                for frame in range(framesWidth):
                    fromx += 1
                    surface = pygame.surface.Surface((pixelSize, pixelSize)).convert()
                    surface.blit(image, (0,0), ((fromx * pixelSize)- pixelSize,0, pixelSize, pixelSize))
                    # surface = pygame.transform.scale(surface, (pixelSize*3, pixelSize*3))
                    surface.set_colorkey((255,0,255))
                    listOfFrames.append(surface)

                self.AllAnimations[fileName] = listOfFrames

#endregion load
    def getClosestSpawner(self):
        self.game.setClosestSpawner()
        closest = self.game.getSpawner()

    
    def handleUI(self):
        self.redHealthBarRect.width = self.currentHealth/self.healthBarRatio
        pygame.draw.rect(self.screen, "black", self.HealthBarRectOutline, 1)
        pygame.draw.rect(self.screen,"white", self.HealthBarRect)
        pygame.draw.rect(self.screen,"red", self.redHealthBarRect)        
        
        
        hp = str(self.currentHealth) + "|" + str(self.maxHealth)
        self.hpText = self.textFont.render(hp, True, ("dark red"))
        self.textRect = self.hpText.get_rect(midbottom=self.HealthBarRect.midbottom)

        self.screen.blit(self.hpText, self.textRect)
        self.screen.blit(self.goldText, self.goldRect)

        #handle next target ui
        if self.ClosestSpawnerVector:
            direction = pygame.Vector2(self.ClosestSpawnerVector.x - self.position.x,self.ClosestSpawnerVector.y - self.position.y).normalize()
            startPoint = pygame.Vector2(self.screen.get_width() - 100, self.screen.get_height() - 100)
            length = 50
            endPoint = startPoint + direction * length
            colour = pygame.color.Color(255, 0,0)
            pygame.draw.line(self.screen, colour, startPoint, endPoint, 2)
            pygame.draw.circle(self.screen, colour, startPoint, 5)
            pygame.draw.circle(self.screen, colour, startPoint, length, width=1)
        return
