import os

import pygame

from Model.GameObjects.Game.GameDifficulty import GameDifficulty
from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Buildings.GasStation import GasStation
from Model.GameObjects.Vehicles.Helicopter import Helicopter
from Model.GameObjects.Buildings.OreMine import OreMine
from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Model.GameObjects.Buildings.OreUnloadStation import OreUnloadStation

class GameObjectCreationService:

    __oreTransportImg__ : pygame.Surface
    __helicopterImg__ : pygame.Surface

    __gasStationImg__ : pygame.Surface
    __oreUnloadStationImg__ : pygame.Surface
    __oreMineImg__ : pygame.Surface

    __screen__ : pygame.Surface
    __gameWidth__ : int
    __gameHeight__: int

    def __init__(self, screen : pygame.Surface, gameWidth : int, gameHeight : int):
        self.__screen__ = screen
        self.__gameWidth__ = gameWidth
        self.__gameHeight__ = gameHeight
        self.__loadImages__()

    def __loadImages__(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        assetPath = os.path.join(os.path.dirname(baseDir), "Assets")

        self.__oreUnloadStationImg__ = pygame.transform.scale(
            pygame.image.load(os.path.join(assetPath, "unloadStation.png")).convert_alpha(), (120, 120)
        )
        self.__helicopterImg__ = pygame.transform.scale(
            pygame.image.load(os.path.join(assetPath, "heli.png")).convert_alpha(), (100, 100)
        )
        self.__oreTransportImg__ = pygame.transform.scale(
            pygame.image.load(os.path.join(assetPath, "transporter.png")).convert_alpha(), (80, 40)
        )
        self.__gasStationImg__ = pygame.transform.scale(
            pygame.image.load(os.path.join(assetPath, "gasStation.png")).convert_alpha(), (60, 120)
        )
        self.__oreMineImg__ = pygame.transform.scale(
            pygame.image.load(os.path.join(assetPath, "mine2.png")).convert_alpha(), (118, 100)
        )

    def createGameObjects(self, difficulty : GameDifficulty) -> list[ImageGameObject]:
        # Create the Helicopter object with difficulty setting
        helicopter : Helicopter = Helicopter(
            image=self.__helicopterImg__,
            maxSpeed=difficulty.getHelicopterMaxSpeed(),
            screen=self.__screen__
        )

        # Create the OreTransport object with difficulty settings
        oreTransport : OreTransport = OreTransport(
            xCoordinate=300,
            yCoordinate=300,
            image=self.__oreTransportImg__,
            fuelConsumption=difficulty.getFuelConsumption(),
            maxSpeed=difficulty.getTransporterMaxSpeed(),
            oreCapacity=difficulty.getTransporterCapacity(),
            screen=self.__screen__
        )
        # Set the Target of the Helicopter
        helicopter.setTarget(oreTransport)

        # Create the GasStation object
        gasStation : GasStation = GasStation(
            xCoordinate=(self.__gameWidth__ // 2),
            yCoordinate=(self.__gameHeight__ // 2) + self.__gameHeight__ // 4,
            image=self.__gasStationImg__,
            screen=self.__screen__,
        )

        # Create the OreMine object with total ore from the difficulty
        oreMine : OreMine= OreMine(
            xCoordinate=self.__gameWidth__ / 10,
            yCoordinate=self.__gameHeight__ // 2,
            image=self.__oreMineImg__,
            screen=self.__screen__,
            totalOre=difficulty.getTotalOre()
        )

        # Create the OreUnloadStation object
        oreUnloadStation : OreUnloadStation = OreUnloadStation(
            xCoordinate=self.__gameWidth__ - self.__gameWidth__ / 10,
            yCoordinate=self.__gameHeight__ // 2,
            image=self.__oreUnloadStationImg__,
            screen=self.__screen__
        )

        return [
            gasStation,
            oreMine,
            oreUnloadStation,
            helicopter,
            oreTransport
        ]