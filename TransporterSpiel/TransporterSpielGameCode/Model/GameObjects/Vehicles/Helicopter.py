import math
import random
import pygame


from Model.GameObjects.Vehicles.OreTransport import OreTransport
from Model.GameObjects.Vehicles.Vehicle import Vehicle
from Services.ConfigService import getConfig


class Helicopter(Vehicle):
    """
    A Class representing a Helicopter Vehicle which Steals Ore from OreTransport objects.

    Inherits from:
        Vehicle (Model.GameObjects.Vehicles.Vehicle)

    Attributes:
        __oreCapacity__ (float): Maximum Ore Capacity that can be carried.
        __loadedOreAmount__ (float): Current Amount of Ore Loaded.
        __isEscaping__ (bool): Flag indicating whether the Helicopter is escaping.
        __escapeTarget__ (tuple[float, float]): Coordinates of the Escape Target.
        __targetChangeTimer__ (int): Timer tracking when to change target after stopping.
        __targetChangeTime__ (int): Duration before retargeting.
        __isStopped__ (bool): Flag indicating if Helicopter is currently stopped.
        __target__ (OreTransport): Current Target OreTransport to steal from.
        __amountStolen__ (float): Total Amount of Ore stolen so far.
        __randomDerivation__ (float): Random deviation factor to avoid movement loops.
    """
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
        """
        Initialize a Helicopter Instance.

        Args:
            screen (pygame.Surface): The Screen Surface to draw the Helicopter.
            image (pygame.Surface): The Image representing the Helicopter.
            maxSpeed (float): Maximum Speed of the Helicopter.
        """
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
        self.__escapeTarget__ = (self.getXCoordinate(),self.getYCoordinate())
        self.__targetChangeTimer__ = 0
        self.__targetChangeTime__ = 0
        self.__isStopped__ = False
        self.__amountStolen__ = 0

    def stealOre(self, target: OreTransport) -> float:
        """
        Steal Ore from the Target OreTransport up to Helicopter's Capacity and Transfer Rate.

        This method decreases Ore from the Target, adds it to the Helicopter's load,
        and starts the escape sequence if capacity is full.

        Args:
            target (OreTransport): The OreTransport to steal Ore from.

        Returns:
            float: The Amount of Ore stolen in this call.
        """
        availableOre: float = target.getLoadedOreAmount()
        freeCapacity: float = self.__oreCapacity__ - self.__loadedOreAmount__
        stolenAmount: float = min(freeCapacity, availableOre, self.getTransferRate())

        # Transfer ore
        target.unloadOre(stolenAmount)
        self.__loadedOreAmount__ += stolenAmount
        self.__amountStolen__ += stolenAmount
        if self.__loadedOreAmount__ >= self.__oreCapacity__:
            self.__startEscape__()
        return stolenAmount

    def getStatus(self):
        """
        Return the Current Status of the Helicopter.

        Returns:
            str: One of "Waiting" (stopped escaping), "Escaping" (currently escaping), or "Attacking".
        """
        if self.__isEscaping__:
            if self.__isStopped__:
                return "Waiting"
            else:
                return "Escaping"
        else:
            return "Attacking"

    def update(self) -> None:
        """
        Update the Helicopter State.

        If the Target Change Timer has expired and the Helicopter is stopped,
        it wakes up. Then moves towards the current target or escape point.
        """
        if self.__targetChangeTimer__ and pygame.time.get_ticks() > self.__targetChangeTimer__ and self.__isStopped__:
            self.__wakeUp__()
        self.__moveTowards__()

    def __startTargetChangeTimer__(self):
        """
        Start a Random Target Change Timer (3-10 seconds) after which the Helicopter
        can retarget its OreTransport after stopping.
        """
        # Set a random delay (3-10 seconds) before the helicopter targets the ore transport again
        self.__targetChangeTime__ = random.randint(3, 10) * 1000
        self.__targetChangeTimer__ = pygame.time.get_ticks() + self.__targetChangeTime__

    def __moveTowards__(self):
        """
        Move the Helicopter towards the current Target OreTransport or Escape Target.

        Controls acceleration, steering direction with random deviation to avoid loops,
        and moves the Helicopter. Stops when reaching the Escape Target.
        """
        self.accelerate()
        if self.__isEscaping__:
            targetX, targetY = self.__escapeTarget__
            dx = targetX - self.getXCoordinate()
            dy = targetY - self.getYCoordinate()
            angleToTarget = math.degrees(math.atan2(-dy, dx))

            # Move towards escapeTarget if not stopped
            if not self.__isStopped__:
                currentAngle =  self.getOrientation()
                angleDif = (angleToTarget - currentAngle) % 360

                if angleDif > 180:
                    self.steer("left")
                else:
                    self.steer("right")
                self.__move__()

                # Check if Helicopter reached the escape location
                self.__checkEscapeLocation__()
        else:
            targetX, targetY = self.__target__.getXCoordinate(), self.__target__.getYCoordinate()
            dx = targetX -  self.getXCoordinate()
            dy = targetY -  self.getYCoordinate()

            # Introduce randomness in angle calculation to avoid loops
            random_deviation = random.uniform(-20, self.__randomDerivation__)
            angleToTarget = math.degrees(math.atan2(-dy, dx)) + random_deviation
            currentAngle =  self.getOrientation()
            angleDif = (angleToTarget - currentAngle) % 360

            if angleDif > 180:
                self.steer("left")
            else:
                self.steer("right")

            self.__move__()

    def __checkEscapeLocation__(self):
        """
        Check if the Helicopter has reached its Escape Target Location.

        If within 3 units of the target, the Helicopter stops, resets loaded Ore,
        starts the Target Change Timer, and stops movement.
        """
        # Check if the helicopter has reached the escape target location
        target_x, target_y = self.__escapeTarget__
        distance_to_target = math.sqrt((target_x - self.getXCoordinate()) ** 2 + (target_y - self.getYCoordinate()) ** 2)
        if distance_to_target < 3:
            self.__isStopped__ = True
            self.__loadedOreAmount__ = 0.0
            self.__startTargetChangeTimer__()
            self.__stop__()
            print("Helicopter has reached the escape target and has stopped.")

    def __wakeUp__(self):
        """
        Wake the Helicopter from a Stopped State, allowing it to move and attack again.
        """
        # Wake the helicopter up, allowing it to move again
        self.__isStopped__ = False
        self.__isEscaping__ = False
        print("Helicopter is awake and ready to move again.")

    def __startEscape__(self):
        """
        Set the Helicopter into Escaping Mode.
        """
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

    def __str__(self) -> str:
        """
        Return a detailed String Representation of the Helicopter Instance,
        including important attributes and current state.
        """
        return (
            f"{type(self).__name__}("
            f"xCoordinate={self.getXCoordinate()}, "
            f"yCoordinate={self.getYCoordinate()}, "
            f"loadedOreAmount={self.__loadedOreAmount__}, "
            f"oreCapacity={self.__oreCapacity__}, "
            f"isEscaping={self.__isEscaping__}, "
            f"isStopped={self.__isStopped__}, "
            f"targetChangeTimer={self.__targetChangeTimer__}, "
            f"amountStolen={self.__amountStolen__}, "
            f"target={self.__target__}, "
            f"randomDerivation={self.__randomDerivation__})"
        )