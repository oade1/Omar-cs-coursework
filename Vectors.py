import pygame, numpy


# 0,-1 1,-1, 1,0 1,1 0,1 -1,1 -1,0 -1,-1

def giveDot(vector, listOfVectors):
    interestList = []
    for vectr in listOfVectors:
        num = numpy.dot(vector, vectr)
        num = float(num)
        interestList.append(num)

    return interestList



# directions = [pygame.math.Vector2(0,-1).normalize(),pygame.math.Vector2(1,-1).normalize(),pygame.math.Vector2(1,0).normalize(),pygame.math.Vector2(1,1).normalize(),
#               pygame.math.Vector2(0,1).normalize(),pygame.math.Vector2(-1,1).normalize(),pygame.math.Vector2(-1,0).normalize(),pygame.math.Vector2(-1,-1).normalize()]
# direction = pygame.Vector2(-2.3,2.6).normalize()

# print(giveDot(direction,directions))



