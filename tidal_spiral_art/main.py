import pygame
import math
import random

# Placeholder tidal data (replace with real data as needed)
tidal_data = [random.uniform(0.5, 2.0) for _ in range(360)]

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
angle_offset = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 30))
    points = []
    for i, tide in enumerate(tidal_data):
        angle = math.radians(i + angle_offset)
        radius = 100 + tide * 200 + i * 0.5
        x = CENTER[0] + math.cos(angle) * radius
        y = CENTER[1] + math.sin(angle) * radius
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.aalines(screen, (0, 200, 255), False, points)
    angle_offset = (angle_offset + 1) % 360
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
