import pygame, sys, os, random, time, ParticleSystem, Projectiles
from UI import *
from Tiles import *
from Enemy import *
from Player import *
from Functions import *
from Game import * 
from SpriteGroups import *
from Objects import * 

pygame.init()

#Work on a way to tell the player where the closest spawner to them is
#spawn the enemies when the player is close enough to a spawner

#graphics 

#code

#add enemies left counter to let the player know how many are left
#Perfect the player attacking on each direction
#add player attack speed ui, a bar that appears when attacking is on cooldown
#make a boss and finish their animations
#Make the options page with what is said in the coursework
#Work on the inventory system and drops
#Make the campFireHeal the player when the player is directly above it


os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
Screen_width, Screen_height = info.current_w, info.current_h 

screen = pygame.display.set_mode((Screen_width, Screen_height), pygame.RESIZABLE)


def MainMenu():
    run = True


    cambirafont = pygame.font.Font(r"Font\MAINMENU.TTF", 50)
    buttonimg = pygame.image.load(r'Images/GUI\ButtonBackground.png').convert()
    buttonimg = pygame.transform.scale(buttonimg,(buttonimg.get_width() * 4,buttonimg.get_height() * 4))
    MMButton = button(Screen_width / 2,250,buttonimg,"Play", cambirafont, screen) 
    OptionsButton = button(Screen_width / 2,400,buttonimg,"Options", cambirafont, screen) 
    QuitButton = button(Screen_width / 2,550,buttonimg,"Quit", cambirafont, screen) 
    
    while run:    
        MousePosition = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                QuitGame()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if MMButton.CheckClick(MousePosition):
                    screen.fill('BLACK')
                    pygame.display.update()
                    MainGamePlayLoop()
                if OptionsButton.CheckClick(MousePosition):
                    OptionsPlayLoop()
                if QuitButton.CheckClick(MousePosition):
                    QuitGame()
        #end of events
        screen.fill("Light grey")

        pygame.display.set_caption("Main Menu - Omar Coursework")

        
        MMButton.draw()
        MMButton.CheckHover(MousePosition)
        
        OptionsButton.draw()
        OptionsButton.CheckHover(MousePosition)
        
        QuitButton.draw()
        QuitButton.CheckHover(MousePosition)
        
        pygame.display.update()
#start of one liners
def getIMG(imgName):
    img = pygame.image.load(imgName)
    return img

def getFONT(fontName,FontSize):
    font = pygame.font.Font(fontName,FontSize)
    return font

#end of one liners

#Functions8

#game loops
def MainGamePlayLoop():
    clock = pygame.time.Clock()
    run = True
    pygame.mouse.set_visible(False)
#delta time
    prev_time = time.time()
#Gamedd
    game = Game.Game()
#spriteGroupsdd
    allSprites = CameraGroup()
    enemyGroup = EnemyGroup()
    playerEnvironment = PlayerEnvironment()
    environment = EnvironmentGroup()
    collideGroup = pygame.sprite.Group()
#Playerdw
    player = Player(1000,1000,allSprites, game)
    player.TileEnvironment = environment
    player.EnemyEnvironment = enemyGroup
    player.screen = screen

    playerEnvironment.player = player
 
    game.SetAllSprites(allSprites)
    game.SetTileEnvironment(environment)
    game.SetEnemyEnvironment(enemyGroup)
    game.SetPlayer(player)
    game.SetCollideGroup(collideGroup)

    game.addToCollideGroup(player)

    #flags
    shopOpen = False

    #shop ui
    foozleFont = pygame.font.Font(r"Font\FOOZLE.ttf", 20)
    simplePanel4 = pygame.image.load(r"Shop\GenericPanel.png").convert_alpha()
    ButtonBackgroundShop = pygame.image.load(r"Shop\GenericTextField.png").convert_alpha()
    ButtonBackgroundShop = pygame.transform.scale_by(ButtonBackgroundShop, 3)
    ShopUi = pygame.surface.Surface((672 ,240))
    for y in range(5):
        for x in range(14):
            ShopUi.blit(simplePanel4, ((x * simplePanel4.get_width()), (y * simplePanel4.get_height())))

    shopX = (screen.get_width() - ShopUi.get_width())/2 
    shopY = (1.5 * (screen.get_height() - ShopUi.get_height())/2)
   
    UpgradeDamagePrice = game.getPriceForDamge()
    UpgradeDamageIncrease = game.getIncreaseOnDamge()

    UpgradeHealthPrice = game.getPriceForHealth()
    UpgradeHealthIncrease = game.getIncreaseOnHealth()

    UpgradeSpeedPrice = game.getPriceForSpeed()
    UpgradeSpeedIncrease = game.getIncreaseOnSpeed()


    print(ButtonBackgroundShop.get_width(), ButtonBackgroundShop.get_height())
    
    UpgradeDamageButton = DamageShopUi(game,pygame.math.Vector2((shopX + 100),(shopY+ (37))),pygame.color.Color("white"))
    UpgradeHealthButton = HealthShopUi(game,pygame.math.Vector2((shopX + 100),(shopY+ 48 + (37))),pygame.color.Color("white"))
    UpgradeSpeedButton = SpeedShopUi(game,pygame.math.Vector2((shopX + 100),(shopY+ 48 + 48 + (37))),pygame.color.Color("white"))

    # timeForDeletionQueue = pygame.time.get_ticks()
    # CooldownForDeletionQueue = 0

    #Particle system
    particleSystem = ParticleSystem.ParticleSystem(game)
    projectileManager = Projectiles.ProjectileManager(game)
    #createFireCamp((500,300),game)

    #enemy manager
    enemyManager = EnemyManager(game)
    mapManagerTwo = MapManagerTwo(game)
    StartLevels(game)




    pygame.event.clear() #so that any inputs made in the loading screen are discarded
    while run:
        #mouse position
        pos = pygame.mouse.get_pos()
        #clock
        clock.tick()
        dt = time.time() - prev_time
        prev_time = time.time()
        
        game.SetDeltaTime(dt)
        
                        
        #draw background
        screen.fill("black")

        if game.isDeletionQueueEmpty() == False:
            game.handleDeletionQueue()
            # timeForDeletionQueue = pygame.time.get_ticks() + CooldownForDeletionQueue
            print(pygame.time.get_ticks())

        if game.isSpawnQueueEmpty() == False:
            print(game.spawnQueue.items)
            game.handleSpawnQueue()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.onQuit()
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if UpgradeDamageButton.ShopButton.CheckClick(pos):
                    if player.getGold() >= UpgradeDamagePrice:
                        UpgradeDamageButton.ShopButton.IsClicked = True
                        UpgradeDamageButton.ShopButton.ClickDurationTime = pygame.time.get_ticks() + UpgradeDamageButton.ShopButton.ClickDuration 
                        player.takeGold(UpgradeDamagePrice)
                        player.IncreaseAttackDamage(UpgradeDamageIncrease)
                        game.IncreaseDamagePrice()
                        UpgradeDamageButton.UpdatePrice()
                        UpgradeDamagePrice = game.getPriceForDamge()
                if UpgradeHealthButton.ShopButton.CheckClick(pos):
                    if player.getGold() >= UpgradeHealthPrice:
                        player.takeGold(UpgradeHealthPrice)
                        player.IncreaseMaxHealth(UpgradeHealthIncrease)
                        game.IncreaseHealthPrice()
                        UpgradeHealthButton.UpdatePrice()
                        UpgradeHealthPrice = game.getPriceForHealth()
                if UpgradeSpeedButton.ShopButton.CheckClick(pos):
                    if player.getGold() >= UpgradeSpeedPrice:
                        player.takeGold(UpgradeSpeedPrice)
                        player.IncreaseSpeed(UpgradeSpeedIncrease)
                        game.IncreaseSpeedPrice()         
                        UpgradeSpeedButton.UpdatePrice()
                        UpgradeSpeedPrice = game.getPriceForSpeed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SavePlayerStats(game)
                    pygame.mouse.set_visible(True)
                    return
                if event.key == pygame.K_9:
                    # print(game.GetAllSpriteGroup())
                    # Pathway(player.position , "BRICKS", 10,30,game)
                    # EnemyRing(player.position, 40, 20, game)
                    # Collectables.BigHealthPoition(player.position, game)
                    # CustomSpawner('MapsTiled/custommap02.csv', game, player.position, csvNumberForSpawner='4', numOfEnemies=10)
                    # print(game.isDeletionQueueEmpty())


                    # enemyManager.createSkeleton(pygame.Vector2(player.position.x - 10, player.position.y))
                    enemyManager.createNecromancer(pygame.Vector2(player.position.x + 60, player.position.y))
                
                if event.key == pygame.K_8:
                    # print(player.position)
                    print(game.GetAllSpriteGroup())
                    print(game.GetCollideGroup())
                    print(game.GetEnemies())
                if event.key == pygame.K_7:
                    # print(game.GetCollideGroup())
                    # print(game.getClosestSpawner())
                    particleSystem.createShockwave(pygame.Vector2(player.position.x, player.position.y), '1', 'small')
                if event.key == pygame.K_6:
                    # print(particleSystem.listOfParticles)
                    # MapManagerTwo(game)
                    particleSystem.createWave(pygame.Vector2(player.position.x + player.image.get_width(), player.position.y), 'RoyalPurpleWaveBigRight')
                    particleSystem.createWave(pygame.Vector2(player.position.x - player.image.get_width(), player.position.y), 'RoyalPurpleWaveBigLeft')
                if event.key == pygame.K_5:
                    # SkeletonSpawner(50,50,1,game)
                    # listOfPixelSizes = ['0', '1', '2', '3']
                    # listOfSizes = ['small', 'middle', 'big']
                    # particleSystem.createShockwave(player.position, random.choice(listOfPixelSizes), random.choice(listOfSizes))
                    randX, randY = random.randint(-50,50),random.randint(-50,50) 
                    projectileManager.createTimedFireball(player, pygame.Vector2(player.position.x, player.position.y), pygame.Vector2(randX,randY).normalize())
                if event.key == pygame.K_4:
                    print(clock.get_fps())
                    enemyManager.createSkeleton(pygame.Vector2(player.position.x - 10, player.position.y))
                if event.key == pygame.K_p:
                    shopOpen = not shopOpen
                    pygame.mouse.set_visible(shopOpen)

            if pygame.mouse.get_pressed()[0] and pygame.mouse.get_visible() == False:
                player.Attack()

        # clock.tick()
        # print(clock.get_fps())



        game.update()


        allSprites.update()
        allSprites.customDraw(player)

        player.update()
        
        #handle shop ui
        if shopOpen:
            screen.blit(ShopUi, (shopX,shopY))

            #texts drawing
            UpgradeDamageButton.draw(pos)

            UpgradeHealthButton.draw(pos)

            UpgradeSpeedButton.draw(pos)
        pygame.display.update()

def OptionsPlayLoop():
    TICKS = 60
    run = True
    print("Options play loop started!!")
    font = pygame.font.Font(r"Font\MAINMENU.ttf", 20)

    #keybinds
    TakingInput = False
    TakingInputKeyPress = None
    TakingInputAction = None

    listOfButtons = getKeyBindButtons()

    while run:
        #mouse pos
        MousePosition = pygame.mouse.get_pos()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if TakingInput and TakingInputAction is not None:
                if event.type == pygame.KEYDOWN:
                    TakingInputKeyPress = event.key
                    print(f'changing {TakingInputAction} to key {pygame.key.name(event.key)}.')

            if event.type == pygame.MOUSEBUTTONDOWN:
                TakingInputAction = CheckKeyBindsPresses(MousePosition, listOfButtons)
                print(TakingInputAction)
                if TakingInputAction is not None:
                    TakingInput = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return            # to go back to main menu
                
                # if event.key == pygame.K_0:
                #     TakingInput = True

        screen.fill("Dark grey")



        DrawKeyBinds(listOfButtons)

        pygame.display.update()
    

        if TakingInput and TakingInputKeyPress is not None and TakingInputAction is not None:
            TakingInput = False

            #Logic to change keybinds in settings
            stateOfKeyBindChange = changeKeyBind(TakingInputAction, TakingInputKeyPress)
            if stateOfKeyBindChange:
                listOfButtons = getKeyBindButtons()

            TakingInputKeyPress = None
            TakingInputAction = None
            

def QuitGame():
    pygame.quit()
    sys.exit()

    return 
#functions
def changeKeyBind(Action, newKey):
    if KEYBINDS[Action] is not None:
        if newKey in KEYSUSEDALREADY: 
            print("Duplicate key")
            for action in KEYBINDS.keys():
                if KEYBINDS[action] == newKey:
                    KEYBINDS[action] = pygame.KMOD_NONE


        KEYBINDS[Action] = newKey
        print(KEYBINDS)
        return True # this is negligible, but it means that the key bind was updated correctly, you dont have to handle it when calling this function.
    else:
        print("Wrong  parameter passed`")
        return False

def DrawKeyBinds(listOfKeybindButtons):
    for keybindbutton in listOfKeybindButtons:
        keybindbutton.draw()

def CheckKeyBindsPresses(mousePos, ListOfButtons):
    # print("CheckKeyBindsPresses called")

    for Nbutton in ListOfButtons:
        # print(f"Looping throught this rect, {Nbutton.rect}, current mouse position is {mousePos}")
        if Nbutton.CheckClick(mousePos):
            # print(Nbutton.getText())
            oldText = Nbutton.getText()
            oldTextSplit = oldText.split(':')
            return oldTextSplit[0]

    return None

def getKeyBindButtons():
    screen = pygame.display.get_surface()

    listOfKeysUsed = []
    listToReturn = []
    
    xPos = -60
    yPos = 50
    yIncrement = 40

    fontForText = pygame.font.Font(r"Font\MAINMENU.ttf", 15)

    keybindButtonImage =  pygame.image.load(r'Images/GUI\ButtonBackground.png').convert()
    keybindButtonImage = pygame.transform.scale_by(keybindButtonImage, 2)

    xPos += keybindButtonImage.get_width()

    # print(keybindButtonImage.get_width(), keybindButtonImage.get_height())

    for keybindAction in KEYBINDS.keys():
        text = str(keybindAction) + ':' + str(pygame.key.name(KEYBINDS[keybindAction]))
        # print(text)
        Nbutton = button(xPos, yPos, keybindButtonImage, text, fontForText, screen)
        listToReturn.append(Nbutton)
        yPos += yIncrement

        listOfKeysUsed.append(KEYBINDS[keybindAction])

    KEYSUSEDALREADY = listOfKeysUsed
    print(KEYSUSEDALREADY)
    return listToReturn



def SavePlayerStats(game=Game):
    player = game.GetPlayer()
    # player.saveGold()
    # player.saveMaxHealth()
    player.saveAllStats()
    game.SavePricesAndUpgrades()



MainMenu()



