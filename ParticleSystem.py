import pygame, os
import random
from Settings import LAYERS

class ParticleSystem:
    def __init__(self, game):
        self.game = game
        game.SetParticleSystem(self)

        self.listOfParticles = []

        self.Animations = {}
        self.loadAllAnimations()
    def getListOfParticles(self):   return self.listOfParticles

    def addParticle(self, particle):
        self.game.GetAllSpriteGroup().add(particle)
        self.listOfParticles.append(particle)

    def removeParticle(self, particle):
        if particle in self.listOfParticles:            
            self.game.GetAllSpriteGroup().remove(particle)
            self.listOfParticles.remove(particle)
            particle.kill()
        else:
            print("Wrong particle object given to remove particle in particle system")
            

    def createShockwave(self,postion, pixelSize=str, size=str):#sizes are three, small, middle and big, pixelSizes are four, 0,1,2 and 3
        try:
            self.addParticle(ShockwaveParticleEffect(postion, self.Animations[pixelSize+size], particleSystem=self))
        except:
            print("effect animation isn't loaded correctly")

    def createWave(self, position, name):
        try:
            self.addParticle(colouredWave(position, self.Animations[name], particleSystem=self))
        except:
            print(f"Cant find {name} in animations dictionary")
            print(self.Animations)
    def loadAllAnimations(self):
        self.loadAllShockwaveAnimations()
        self.loadAllColouredWave()

    def loadAllShockwaveAnimations(self):
        listOfPixelSizes = ['0','1','2','3']
        listOfSizes = ['small', 'middle', 'big']

        for i in listOfPixelSizes:
            for ii in listOfSizes:
                self.loadShockwaveAnimation(i, ii)

    def loadAllColouredWave(self):

        for root,dirs,files in os.walk(os.path.join('Effects', 'Waves')):
            for file in files:
                if file.lower().endswith(('.png')):
                    path = os.path.join(root, file)
                    image = pygame.image.load(path)
                    print(f"Loading {file}...")
                    self.loadWaveAnimations(image.get_width()//3, image, file)

    def loadWaveAnimations(self, framePixelSize, image=pygame.image, name=str):
        x = 0
        listOfFrmaes = []
        for _ in range(3):
            surface = pygame.surface.Surface((framePixelSize, image.get_height()), pygame.SRCALPHA)
            surface.blit(image, (0,0), (x, 0, framePixelSize, image.get_height()))

            listOfFrmaes.append(surface)
            x += framePixelSize

        if '.png' in name:
            name = name.removesuffix('.png')

        self.Animations[name] = listOfFrmaes
        print(self.Animations[name])


    def loadShockwaveAnimation(self, pixelSize, size):
        listOfFrames = []
        mainDirectory = "/VisualEffects/"+"Shockwave/"+str(pixelSize)+"/"+str(size) 
        currentDirectory = os.getcwd()
        for file in os.listdir(currentDirectory+mainDirectory):
            surface = pygame.image.load(currentDirectory+mainDirectory+"/"+file).convert_alpha()
            listOfFrames.append(surface)
        print(str(pixelSize+size))
        self.Animations[str(pixelSize+size)] = listOfFrames


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, Position=pygame.Vector2, listOfAnimations=list,ParticleSystem=ParticleSystem, z = LAYERS['PARTICLES'], animationCooldown = 25):
        self.position = Position # center of the effect
        self.z = z
        #Animation variables
        self.Animations = listOfAnimations
        self.timeForFrame = pygame.time.get_ticks()
        self.cooldownForFrame = animationCooldown
        self.frame = 0
        self.maxFrame = len(listOfAnimations)

        self.image = self.Animations[0] 
        self.rect = self.image.get_rect(center=self.position)

        self.particleSystem = ParticleSystem

        super().__init__()

    def update(self):
        if pygame.time.get_ticks() > self.timeForFrame:
            self.timeForFrame += self.cooldownForFrame
            self.frame += 1
            if self.frame >= self.maxFrame:
                self.particleSystem.removeParticle(self)
            if self.frame < self.maxFrame: 
                # print(self.frame)
                self.image = self.Animations[self.frame]

class ShockwaveParticleEffect(ParticleEffect):
    def __init__(self, Position=pygame.Vector2, listOfFrames=list, animationCooldown = 25, particleSystem=ParticleSystem): 
        listOfFrames = listOfFrames
        # print(listOfFrames)
        # print("--------------------------------")
        super().__init__(Position, listOfFrames, animationCooldown=animationCooldown, ParticleSystem=particleSystem)
        # print(self.maxFrame)
        self.maxFrame -= 10 # for some reason this offset is needed, otherwise it loops around 

class colouredWave(ParticleEffect):
    def __init__(self, Position=pygame.Vector2, listOfFrames=list, animationCooldown = 100, particleSystem = ParticleSystem):
        super().__init__(Position, listOfFrames, particleSystem, animationCooldown=animationCooldown)




