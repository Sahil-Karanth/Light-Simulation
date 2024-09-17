    if hit:
        pygame.draw.circle(screen, (0, 0, 255), (int(hit.x * CELL_SIZE), int(hit.y * CELL_SIZE)), 5)
        pygame.draw.line(screen, (0, 0, 255), (player.pos.x * CELL_SIZE, player.pos.y * CELL_SIZE), (hit.x * CELL_SIZE, hit.y * CELL_SIZE), 2)
