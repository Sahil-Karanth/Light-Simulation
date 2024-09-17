import pygame
from classes import Player, Vector

# Define the game map
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")

# Define movement speed
MOVEMENT_SPEED = 0.1

# Create player instance
player = Player([4.5, 4.5], [1, 0])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(Vector([0, -MOVEMENT_SPEED]))
    if keys[pygame.K_DOWN]:
        player.move(Vector([0, MOVEMENT_SPEED]))
    if keys[pygame.K_LEFT]:
        player.move(Vector([-MOVEMENT_SPEED, 0]))
    if keys[pygame.K_RIGHT]:
        player.move(Vector([MOVEMENT_SPEED, 0]))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw map
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw player
    pygame.draw.circle(screen, (255, 0, 0), (int(player.pos.x * CELL_SIZE), int(player.pos.y * CELL_SIZE)), 5)

    # Update the display
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)  # Cap the frame rate

pygame.quit()
