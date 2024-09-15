import pygame,Game, Enemy, Player

class Raycaster:
    def __init__(self, pos, game=Game.Game):
        self.position = pos  
        self.directions =         self.directions = {
            'N': pygame.math.Vector2(0, -1),
            'NE': pygame.math.Vector2(1, -1).normalize(),
            'E': pygame.math.Vector2(1, 0),
            'SE': pygame.math.Vector2(1, 1).normalize(),
            'S': pygame.math.Vector2(0, 1),
            'SW': pygame.math.Vector2(-1, 1).normalize(),
            'W': pygame.math.Vector2(-1, 0),
            'NW': pygame.math.Vector2(-1, -1).normalize()
        } #done like this cuz for some reason vector 2s cant be keys in a dictionary  
        
        self.game = game
        
        
        self.TimeBeforeRayCasting = 0
        self.cooldownToCheck = 500 + (20 * len(self.game.GetEnemies()))  
        print(self.cooldownToCheck)

        self.distanceToRayCast = 100  

    def resetPos(self, pos):
        self.position = pos

    def castRay(self, direction, distance):
        ray_end = self.position + direction * distance
        return ray_end

    def checkDirections(self):

        if pygame.time.get_ticks() > self.TimeBeforeRayCasting:
            self.TimeBeforeRayCasting += self.cooldownToCheck
            # print("began ray casting to check")
            collision_results = {direction: False for direction in self.directions}
            
            for direction, vector in self.directions.items():
                for distance in range(1, self.distanceToRayCast + 1, 15):
                    ray_end = self.castRay(vector, distance)
                    ray_rect = pygame.Rect(ray_end.x, ray_end.y, 1, 1)
                    
                    for sprite in self.game.GetCollideGroup().sprites():
                        if sprite == self or type(sprite) == Enemy.Skeleton or type(sprite) == Player.Player:
                            continue
                        
                        if ray_rect.colliderect(sprite.CollideRect):
                            collision_results[direction] = True
                            #print(type(sprite))
                            break
            
            return collision_results
        
        return None  
