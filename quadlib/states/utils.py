import pygame

def txt(surface,x,y, message, color = (255, 255, 255)):
    fontobject=pygame.font.SysFont('Arial', 28)
    if len(message) != 0:
        surface.blit(fontobject.render(message, 1, color), (x, y))
