import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Vehicles.Vehicle import Vehicle

class OreTransport(Vehicle):
    __oreCapacity__ : float
    __loadedOreAmount__ : float

    def __init__(self, screen: pygame.Surface, image: pygame.Surface, xCoordinate: float = 0, yCoordinate: float = 0, fuelConsumption: float = 0.05, maxSpeed: float = 4.5, oreCapacity: float  = 100):
        # Initialize the base Vehicle class
        super().__init__(
            xCoordinate,
            yCoordinate,
            collision=True,
            image=image,
            layer=5,
            fuelCapacity=100,
            fuelConsumption=fuelConsumption,
            turningSpeed=4.5,
            maxSpeed=maxSpeed,
            acceleration=0.05,
            screen=screen
        )
        # OreTransport-specific attributes
        self.__oreCapacity__ = oreCapacity
        self.__loadedOreAmount__ = 0

    def loadOre(self, amount: float) -> float:
        surplus = max(0.0, self.__loadedOreAmount__ + amount - self.__oreCapacity__)
        self.__loadedOreAmount__ = min(self.__oreCapacity__, self.__loadedOreAmount__ + amount)
            
        if surplus > 0:
            return surplus
        else:
            return 0

    def unloadOre(self, amount: float) -> float:
        unloadedAmount = min(self.__loadedOreAmount__, amount)
        self.__loadedOreAmount__ = max(0.00, self.__loadedOreAmount__ - amount)
        return unloadedAmount

    def getLoadedOreAmount(self) -> float:
        return self.__loadedOreAmount__

    def getOreCapacity(self) -> float:
        return self.__oreCapacity__

    def oreIsFull(self) -> bool:
        return self.__loadedOreAmount__ == self.__oreCapacity__

    def isEmpty(self) -> bool:
        return self.__loadedOreAmount__ == 0

    def handleCollisionWithWall(self, direction: str) -> None:
        bounce_strength = 10

        # Turn the vehicle around by changing its orientation
        super().setOrientation((super().getOrientation() + 180) % 360)
        if direction == 'top':
            super().setYCoordinate(super().getYCoordinate() + bounce_strength)
        elif direction == 'bottom':
            super().setYCoordinate(super().getYCoordinate() - bounce_strength)
        elif direction == 'left':
            super().setXCoordinate(super().getXCoordinate() + bounce_strength)
        elif direction == 'right':
            super().setXCoordinate(super().getXCoordinate() - bounce_strength)

        # Slightly reduce speed to simulate a turn around while keeping momentum
        if super().getSpeed() > 0:
            super().setSpeed(super().getSpeed() * 0.8)
        else:
            super().setSpeed(super().getSpeed() * 0.8)

    def handleCollisionWithObject(self, collisionObject : ImageGameObject) -> None:
        # Calculate direction vector between vehicles
        dx : float = super().getXCoordinate() - collisionObject.getXCoordinate()
        dy : float= super().getYCoordinate() - collisionObject.getYCoordinate()

        # Normalize vector to get direction
        distance : int = max(1, int((dx ** 2 + dy ** 2) ** 0.5))
        nx: float = dx / distance
        ny: float = dy / distance

        # Push transport away a bit along the normalized direction
        bounce_strength = 10  # Strength of the bounce
        super().setXCoordinate(int(super().getXCoordinate() + nx * bounce_strength))
        super().setYCoordinate(int(super().getYCoordinate() + ny * bounce_strength))

        # Reflect the orientation (turn around)
        # Reverse the orientation by 180 degrees (reflect the direction of movement)
        super().setOrientation((super().getOrientation() + 180) % 360)

        # Slightly reduce speed to simulate a turn around while keeping momentum
        if super().getSpeed() > 0:
            super().setSpeed(super().getSpeed() * 0.8)  # Keep 90% of the current speed
        else:
            super().setSpeed(super().getSpeed() * 0.8)  # Ensure it doesn't reverse the speed if already negative
