import pygame
import math

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2D Raycasting')

# Define a simple wall structure (for demonstration)
walls = [
    pygame.Rect(300, 100, 10, 200),
    pygame.Rect(100, 200, 200, 10),
    pygame.Rect(400, 200, 200, 10)
]

# Player variables
player_pos = (100, 100)
player_angle = 0  # Facing right initially

# Ray parameters
num_rays = 60
fov = math.pi / 3  # 60 degrees field of view
ray_angle_increment = fov / num_rays

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player_pos[0] += 1

    # Raycasting loop
    ray_angle = player_angle - fov / 2  # Start from the leftmost ray
    for ray in range(num_rays):
        # Calculate ray direction
        ray_dx = math.cos(ray_angle)
        ray_dy = math.sin(ray_angle)

        # Find closest intersection point with walls
        closest_intersection = None
        closest_distance = float('inf')

        for wall in walls:
            if wall.colliderect((player_pos[0], player_pos[1], ray_dx, ray_dy)):
                intersection = wall.clipline(player_pos, (player_pos[0] + ray_dx, player_pos[1] + ray_dy))
                if intersection:
                    distance = math.sqrt((player_pos[0] - intersection[0])**2 + (player_pos[1] - intersection[1])**2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_intersection = intersection

        # Draw rays (optional for visualization)
        if closest_intersection:
            pygame.draw.line(screen, RED, player_pos, closest_intersection, 2)
        else:
            ray_end = (player_pos[0] + ray_dx * 1000, player_pos[1] + ray_dy * 1000)
            pygame.draw.line(screen, WHITE, player_pos, ray_end, 2)

        # Increment ray angle
        ray_angle += ray_angle_increment

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall)

    # Draw player (circle for now)
    pygame.draw.circle(screen, WHITE, (int(player_pos[0]), int(player_pos[1])), 5)

    pygame.display.flip()

pygame.quit()
