import pygame

from Model.GameObjects.Buildings.Building import Building
from Services.ConfigService import getConfig

class GasStation(Building):
    """
    A Class representing a Gas Station Building that provides Fuel Resources.

    Inherits from:
        Building (Model.GameObjects.Buildings.Building): Base Class for all Building Objects.

    """

    def __init__(self, image : pygame.Surface, screen : pygame.Surface, xCoordinate : float = 0.0, yCoordinate : float = 0.0):
        """
        Initialize a GasStation Object using Configuration Parameters.

        Args:
            image (pygame.Surface): The Image used for displaying the Gas Station.
            screen (pygame.Surface): The Game Screen Surface where the Gas Station is rendered.
            xCoordinate (float): The X-Coordinate of the Gas Station.
            yCoordinate (float): The Y-Coordinate of the Gas Station.
        """
        gasStationConfig = getConfig().getGameConfig().getGasStationConfig()
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=False,
            image=image,
            screen=screen,
            totalResourceStored=0.0,
            transferRate=gasStationConfig.getTransferRate()
        )
        # Increase Collision Radius to simplify Refueling by nearby Vehicles
        super().setCollisionRadius(super().getCollisionRadius() * 1.5)

    def giveResource(self) -> float:
        """
        Provide the Amount of Resource (Fuel) transferred per Operation.

        Returns:
            float: The Transfer Rate defined in the Configuration.
        """
        return self.__transferRate__