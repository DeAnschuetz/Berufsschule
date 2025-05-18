import math
import random
import pygame


from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Model.GameObjects.Vehicles.Vehicle import Vehicle
from Services.ConfigService import getConfig


class Helicopter(Vehicle):

    __oreCapacity__ : float
    __loadedOreAmount__ : float
    __isEscaping__ : bool
    __escapeTarget__ : tuple[float, float]
    __targetChangeTimer__ : int
    __targetChangeTime__ : int
    __isStopped__ : bool
    __target__ : OreTransport
    __amountStolen__: float
    __randomDerivation__: float

    def __init__(self, screen: pygame.Surface, image: pygame.Surface, maxSpeed: float = 5.0) -> None:
        config = getConfig()
        screenWidth: int = config.getScreenConfig().getScreenWidth()
        helicopterConfig = config.getGameConfig().getHelicopterConfig()
        self.__randomDerivation__ = helicopterConfig.getHelicopterRandomDeviation()
        super().__init__(
            xCoordinate=screenWidth / 2,
            yCoordinate= helicopterConfig.getHelicopterEscapeY(),
            collision=True,
            image=image,
            layer=100,
            fuelCapacity=100.00,
            fuelConsumption=0.00,
            turningSpeed=1.5,
            maxSpeed=maxSpeed,
            acceleration=0.05,
            screen=screen,
            transferRate=helicopterConfig.getOreCapacity()
        )
        self.__oreCapacity__ = helicopterConfig.getOreCapacity()
        self.__loadedOreAmount__ = 0.0
        self.__isEscaping__ = False
        self.__escapeTarget__ = (super().getXCoordinate(),super().getYCoordinate())
        self.__targetChangeTimer__ = 0
        self.__targetChangeTime__ = 0
        self.__isStopped__ = False
        self.__amountStolen__ = 0

    def stealOre(self, target: OreTransport) -> float:
        availableOre: float = target.getLoadedOreAmount()
        freeCapacity: float = self.__oreCapacity__ - self.__loadedOreAmount__
        stolenAmount: float = min(freeCapacity, availableOre, super().getTransferRate())

        # Transfer ore
        target.unloadOre(stolenAmount)
        self.__loadedOreAmount__ += stolenAmount
        self.__amountStolen__ += stolenAmount
        if self.__loadedOreAmount__ >= self.__oreCapacity__:
            self.__startEscape__()
        return stolenAmount

    def __startTargetChangeTimer__(self):
        # Set a random delay (3-10 seconds) before the helicopter targets the ore transport again
        self.__targetChangeTime__ = random.randint(3, 10) * 1000
        self.__targetChangeTimer__ = pygame.time.get_ticks() + self.__targetChangeTime__

    def __moveTowards__(self):
        super().accelerate()
        if self.__isEscaping__:
            targetX, targetY = self.__escapeTarget__
            dx = targetX -  super().getXCoordinate()
            dy = targetY -  super().getYCoordinate()
            angleToTarget = math.degrees(math.atan2(-dy, dx))

            # Move towards escapeTarget if not stopped
            if not self.__isStopped__:
                currentAngle =  super().getOrientation()
                angleDif = (angleToTarget - currentAngle) % 360

                if angleDif > 180:
                    super().steer("left")
                else:
                    super().steer("right")
                super().move()

                # Check if we have reached the escape target
                self.__checkEscapeLocation__()
        else:
            targetX, targetY = self.__target__.getXCoordinate(), self.__target__.getYCoordinate()
            dx = targetX -  super().getXCoordinate()
            dy = targetY -  super().getYCoordinate()

            # Introduce randomness in angle calculation to avoid loops
            random_deviation = random.uniform(-20, self.__randomDerivation__)
            angleToTarget = math.degrees(math.atan2(-dy, dx)) + random_deviation
            currentAngle =  super().getOrientation()
            angleDif = (angleToTarget - currentAngle) % 360

            if angleDif > 180:
                super().steer("left")
            else:
                super().steer("right")

            super().move()

    def __checkEscapeLocation__(self):
        # Check if the helicopter has reached the escape target location
        target_x, target_y = self.__escapeTarget__
        distance_to_target = math.sqrt((target_x - self.getXCoordinate()) ** 2 + (target_y - self.getYCoordinate()) ** 2)
        if distance_to_target < 3:
            self.__isStopped__ = True
            self.__loadedOreAmount__ = 0.0
            self.__startTargetChangeTimer__()
            super().stop()
            print("Helicopter has reached the escape target and has stopped.")

    def __wakeUp__(self):
        # Wake the helicopter up, allowing it to move again
        self.__isStopped__ = False
        self.__isEscaping__ = False
        print("Helicopter is awake and ready to move again.")

    def __startEscape__(self):
        self.__isEscaping__ = True

    def getLoadedOreAmount(self) -> float:
        return self.__loadedOreAmount__

    def getOreCapacity(self) -> float:
        return self.__oreCapacity__

    def getIsEscaping(self) -> bool:
        return self.__isEscaping__

    def setIsEscaping(self, isEscaping: bool):
        self.__isEscaping__ = isEscaping

    def setTarget(self, target: OreTransport):
        self.__target__ = target

    def getStolenAmount(self) -> float:
        return self.__amountStolen__

    def getStatus(self):
        if self.__isEscaping__:
            if self.__isStopped__:
                return "Waiting"
            else:
                return "Escaping"
        else:
            return "Attacking"

    def update(self) -> None:
        if self.__targetChangeTimer__ and pygame.time.get_ticks() > self.__targetChangeTimer__ and self.__isStopped__:
            self.__wakeUp__()
        self.__moveTowards__()
