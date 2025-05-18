# OreUnloadStation.py
import pygame
from Model.GameObjects.Buildings.Building import Building

class OreUnloadStation(Building):
    def __init__(self, image: pygame.Surface,screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0) -> None:
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