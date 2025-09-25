import pygame

from Model.GameObjects.Buildings.Building import Building

class OreUnloadStation(Building):
    """
    A Class representing an Ore Unload Station where Vehicles can offload Ore Instantly.

    Inherits from:
        Building (Model.GameObjects.Buildings.Building): The Base Class for all Building Objects.

    """

    def __init__(self, image: pygame.Surface,screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0) -> None:
        """
        Initialize an OreUnloadStation Object.

        Args:
        image (pygame.Surface): The Image representing the Station.
        screen (pygame.Surface): The Surface on which the Station is drawn.
        xCoordinate (float): The X Position of the Station.
        yCoordinate (float): The Y Position of the Station.
        """
        super().__init__(
            xCoordinate=xCoordinate,
             yCoordinate=yCoordinate,
             collision=False,
             image=image,
             screen=screen,
             totalResourceStored=0.0,
             # TransferRate = 1000000 to ensure that the vehicle is Instantly empy
             transferRate=1000000
        )