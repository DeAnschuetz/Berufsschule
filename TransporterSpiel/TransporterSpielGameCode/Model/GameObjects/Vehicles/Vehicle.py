import pygame
import math

from Model.GameObjects.Base.ImageGameObject import ImageGameObject

class Vehicle(ImageGameObject):
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

    def __init__(self, xCoordinate: float, yCoordinate: float, collision: bool, image: pygame.Surface, layer: int, fuelCapacity: float, fuelConsumption: float, turningSpeed: float, acceleration : float, maxSpeed: float, screen: pygame.Surface, transferRate: float = 100):
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
        self.__fuelLevel__ = max(0.00, min(self.__fuelCapacity__, fuelLevel))
        
    def getSpeed(self) -> float:
        return self.__speed__
    
    def setSpeed(self, speed: float) -> None:
        self.__speed__ = speed

    def refuel(self, transferred : float):
        self.setFuelLevel(self.getFuelLevel() + transferred)

    def fuelIsFull(self):
        return self.__fuelLevel__ >= self.__fuelCapacity__ - 0.9

    def accelerate(self) -> None:
        if self.__fuelLevel__ > 0:
            # Increase speed until maxSpeed is reached
            self.__speed__ = min(self.__speed__ + self.__acceleration__, self.__maxSpeed__)

    def decelerate(self) -> None:
        if self.__fuelLevel__ > 0:
            # Increase speed until -maxSpeed is reached
            self.__speed__ = max(self.__speed__ - self.__acceleration__, -self.__maxSpeed__)

    def steer(self, direction: str) -> None:
        if direction == "left":
            self.__orientation__ -= self.__turningSpeed__
        elif direction == "right":
            self.__orientation__ += self.__turningSpeed__
        # Ensure orientation stays within 0-360 degrees
        self.__orientation__ = self.__orientation__ % 360

    def move(self) -> None:
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

    def stop(self):
        self.__speed__ = 0

    def getTransferRate(self) -> float:
        return self.__transferRate__

    def update(self) -> None:
        # Slow the vehicle slightly
        if self.__speed__ > 0.01:
            self.__speed__ = max(0.00, self.__speed__ - 0.001)
        elif self.__speed__ < -0.01:
            self.__speed__ = min(0.00, self.__speed__ + 0.001)
        else:
            self.__speed__ = 0

        # Call move to update fuel Level and Position
        self.move()

    def __str__(self):
        return f"{type(self).__name__} xCoordinate: {self.getXCoordinate()}, yCoordinate: {self.getYCoordinate()}, speed: {self.getSpeed()}, orientation: {self.getOrientation()}"