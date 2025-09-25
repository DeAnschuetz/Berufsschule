import pygame
import math

from Model.GameObjects.Base.ImageGameObject import ImageGameObject

class Vehicle(ImageGameObject):
    """
    A Class representing a generic Vehicle that can move, accelerate, steer, and consume Fuel.

    Inherits from:
        ImageGameObject (Model.GameObjects.Base.ImageGameObject)

    Attributes:
        __fuelCapacity__ (float): Maximum amount of Fuel the Vehicle can hold.
        __turningSpeed__ (float): Degrees the Vehicle turns per Steering Action.
        __baseFuelConsumption__ (float): Base Fuel Consumption Rate at full Speed.
        __currentFuelConsumption__ (float): Actual Fuel Consumption which can be modified dynamically.
        __acceleration__ (float): Acceleration per Update Cycle.
        __maxSpeed__ (float): Maximum Speed the Vehicle can reach.
        __currentMaxSpeed__ (float): Maximum Speed currently allowed (modifiable).
        __fuelLevel__ (float): Current Fuel Level.
        __speed__ (float): Current Speed.
        __transferRate__ (float): Fuel Transfer Rate used during Refueling.
    """
    __fuelCapacity__ : float
    __turningSpeed__ : float
    __baseFuelConsumption__ : float  
    __currentFuelConsumption__ : float
    __acceleration__ : float  
    __maxSpeed__ : float
    __currentMaxSpeed__ : float
    __fuelLevel__ : float
    __speed__ : float
    __transferRate__: float

    def __init__(
            self,
            xCoordinate: float,
            yCoordinate: float,
            collision: bool,
            image: pygame.Surface,
            layer: int,
            fuelCapacity: float,
            fuelConsumption: float,
            turningSpeed: float,
            acceleration : float,
            maxSpeed: float,
            screen: pygame.Surface,
            transferRate: float = 100
    ):
        """
        Initialize a Vehicle Object with Motion and Fuel-related Attributes.

        Args:
            xCoordinate (float): Initial X Position.
            yCoordinate (float): Initial Y Position.
            collision (bool): Whether the Object has Collision Detection.
            image (pygame.Surface): Image representing the Vehicle.
            layer (int): Drawing Layer.
            fuelCapacity (float): Maximum Fuel Capacity.
            fuelConsumption (float): Base Fuel Consumption Rate.
            turningSpeed (float): Turning Speed in Degrees.
            acceleration (float): Acceleration per Update.
            maxSpeed (float): Maximum Speed.
            screen (pygame.Surface): Game Screen to draw on.
            transferRate (float): Fuel Transfer Rate. Default is 100.
        """
        # TODO CONFIG
        # Initialize base GameObject class
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=collision,
            image=image,
            layer=layer,
            screen=screen
        )
        
        # Set vehicle-specific attributes
        self.__acceleration__ = acceleration
        self.__fuelCapacity__ = fuelCapacity
        self.__turningSpeed__ = turningSpeed
        self.__fuelConsumption__ = fuelConsumption
        self.__currentFuelConsumption__ = fuelConsumption
        self.__maxSpeed__ = maxSpeed
        self.__currentMaxSpeed__ = maxSpeed
        self.__fuelLevel__ = fuelCapacity  # Start with full fuel
        self.__speed__ = 0
        self.__orientation__ = 0
        self.__transferRate__ = transferRate

    def update(self) -> None:
        """
        Update the Vehicle each Frame:
        - Gradually slow down due to Friction.
        - Move based on current Speed and Orientation.
        """
        # Slow the vehicle slightly
        if self.__speed__ > 0.01:
            self.__speed__ = max(0.00, self.__speed__ - 0.001)
        elif self.__speed__ < -0.01:
            self.__speed__ = min(0.00, self.__speed__ + 0.001)
        else:
            self.__speed__ = 0

        # Call move to update fuel Level and Position
        self.__move__()

    def refuel(self, transferred : float):
        """
        Increase the current Fuel Level by the given transferred amount.
        """
        self.setFuelLevel(self.getFuelLevel() + transferred)

    def fuelIsFull(self):
        """
        Check if the Fuel Tank is considered Full.
        Returns True if Fuel Level is within 0.9 units of full Capacity.
        """
        return self.__fuelLevel__ >= self.__fuelCapacity__ - 0.9

    def accelerate(self) -> None:
        """
        Increase Speed based on Acceleration until Max Speed is reached.
        Only works if Fuel is available.
        """
        if self.__fuelLevel__ > 0:
            # Increase speed until maxSpeed is reached
            self.__speed__ = min(self.__speed__ + self.__acceleration__, self.__maxSpeed__)

    def decelerate(self) -> None:
        """
        Decrease Speed based on Acceleration until negative Max Speed is reached.
        Allows reversing.
        """
        if self.__fuelLevel__ > 0:
            # Increase speed until -maxSpeed is reached
            self.__speed__ = max(self.__speed__ - self.__acceleration__, -self.__maxSpeed__)

    def steer(self, direction: str) -> None:
        """
        Decrease Speed based on Acceleration until negative Max Speed is reached.
        Allows reversing.
        """
        if direction == "left":
            self.__orientation__ -= self.__turningSpeed__
        elif direction == "right":
            self.__orientation__ += self.__turningSpeed__
        # Ensure orientation stays within 0-360 degrees
        self.__orientation__ = self.__orientation__ % 360

    def __move__(self) -> None:
        """
        Decrease Speed based on Acceleration until negative Max Speed is reached.
        Allows reversing.
        """
        radians : float = math.radians(self.__orientation__)
        dx : float= math.cos(radians) * self.__speed__
        dy : float = -math.sin(radians) * self.__speed__
        newX : float = self.getXCoordinate() + dx
        newY: float = self.getYCoordinate() + dy

        # Update coordinates with new values after checking collisions
        self.setXCoordinate(newX)
        self.setYCoordinate(newY)

        # Reduce fuel based on speed
        self.__fuelLevel__ -= self.__fuelConsumption__ / 10 * abs(self.__speed__)
        if self.__fuelLevel__ < 0:
            self.__fuelLevel__ = 0

    def __stop__(self):
        """
        Immediately stop the Vehicle by setting Speed to 0.
        """
        self.__speed__ = 0

    def getTransferRate(self) -> float:
        return self.__transferRate__

    def getFuelCapacity(self) -> float:
        return self.__fuelCapacity__

    def getFuelLevel(self) -> float:
        return self.__fuelLevel__

    def getBaseFuelConsumption(self) -> float:
        return self.__baseFuelConsumption__

    def getAcceleration(self) -> float:
        return self.__acceleration__

    def getTurningSpeed(self) -> float:
        return self.__turningSpeed__

    def getCurrentFuelConsumption(self) -> float:
        return self.__currentFuelConsumption__

    def setCurrentFuelConsumption(self, fuelConsumption : float) -> None:
        self.__currentFuelConsumption__ = fuelConsumption

    def resetCurrentFuelConsumption(self) -> None:
        self.__currentFuelConsumption__ = self.__baseFuelConsumption__

    def getMaxSpeed(self) -> float:
        return self.__maxSpeed__

    def setFuelLevel(self, fuelLevel: float) -> None:
        # Clamp Fuel Level between 0 and Fuel Capacity
        self.__fuelLevel__ = max(0.00, min(self.__fuelCapacity__, fuelLevel))

    def getSpeed(self) -> float:
        return self.__speed__

    def setSpeed(self, speed: float) -> None:
        self.__speed__ = speed