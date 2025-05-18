import pygame

from Model.GameObjects.Exceptions.QuitException import QuitException


def waitForKeyPress(key) -> bool:
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitException()

            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
    return False