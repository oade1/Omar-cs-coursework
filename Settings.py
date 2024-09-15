import pygame
from pygame import Vector2

LAYERS = {
    'WATER': 0,
    'BACKGROUND' : 1,
    'TILES': 2,
    'PATHWAY': 3,
    'OBSTACLES': 4,
    'ENEMYRING': 5,
    'COLLECTABLE': 6,
    'ENEMY': 7,
    'PROJECTILES': 8,
    'PLAYER': 9,
    'PARTICLES': 10
    }

CSVColliders = {
    '1': False,
    '2': False,
    '3': True,
    '4': False,
    '5': False,
    '6': False,
    '7': False,
    '8': True,
    '9': False,
    '10': False,
    '11': False,
    '12': False,
    '13': False,
   
}

CSVMaps = {
    '1': 'EXTERIOR',
    '2': 'EXTERIOR',
    '3': 'EXTERIOR',
    '4': 'EXTERIOR',
    '5': 'DUNGEON',
    '6': 'DUNGEON',
    '7': 'DUNGEON',
    '8': 'EXTERIOR',
    '9': 'DUNGEON',
    '10': 'EXTERIOR',
    '11': 'EXTERIOR',
    '12': 'EXTERIOR',
    '13': 'EXTERIOR',  
}

ENEMYSTATS = {
    'SKELETON': [int(50), int(100), int(100) ,int(20), int(500)],
    'NECROMANCER':  [int(50), int(100), int(100) ,int(20), int(500)]  
}

ENEMYDISTANCES = {
    'SKELETON': [int(200), int(500)] #first is distance to detect target from, second is distance to go back to spawn point from
}

ENEMYTYPES = {
    '1': "SKELETON" 
}

DIRECTIONS = {
    'Down': Vector2(0, 1),
    'Right': Vector2(1, 0),
    'Left': Vector2(-1, 0),
    'Up': Vector2(0, -1) 
}

PlayerFacingTolerance = 0.1

KEYBINDS = {
    'WALKUP': pygame.K_w,
    'WALKLEFT': pygame.K_a,
    'WALKDOWN': pygame.K_s,
    'WALKRIGHT': pygame.K_d,
    'SHOP': pygame.K_p
}

KEYSUSEDALREADY = [
    pygame.K_w,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_p
]
