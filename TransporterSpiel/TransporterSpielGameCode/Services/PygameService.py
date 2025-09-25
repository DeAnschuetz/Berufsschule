import pygame

from Model.GameObjects.Exceptions.QuitException import QuitException


def waitForKeyPress(key) -> bool:
    """
    Wait for a Specific Key Press Event.

    Loops until the specified Key is pressed. Raises a QuitException if the User closes the Window.

    Args:
        key (int): The Key Code to wait for.

    Returns:
        bool: True if the specified Key is pressed.
    """
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitException()

            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True
    return False