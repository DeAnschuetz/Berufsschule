import pygame

from Model.GameObjects.Buildings.Building import Building
from Services.ConfigService import getConfig

class OreMine(Building):
    """
    A Class representing an Ore Mine Building that stores and provides Ore Resources.

    Inherits from:
        Building (Model.GameObjects.Buildings.Building): Provides Base Functionality for Buildings.
    """


    def __init__(self, image: pygame.Surface, screen: pygame.Surface, xCoordinate: float = 0, yCoordinate: float = 0, totalOre: int = 1000) -> None:
        """
        Initialize an OreMine Instance.

        Args:
            image (pygame.Surface): The Visual Representation of the Ore Mine.
            screen (pygame.Surface): The Surface to draw the Ore Mine on.
            xCoordinate (float): X-Coordinate for positioning.
            yCoordinate (float): Y-Coordinate for positioning.
            totalOre (int): Initial Amount of Ore Stored in the Mine.
        """
        oreMineConfig = getConfig().getGameConfig().getOreMineConfig()
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=False,
            image=image,
            layer=1,
            screen=screen,
            totalResourceStored=totalOre,
            transferRate=oreMineConfig.getTransferRate()
        )