import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.Vehicles.Vehicle import Vehicle
from Services.ConfigService import getConfig


class OreTransport(Vehicle):
    """
    Represents an Ore Transport Vehicle capable of carrying Ore.

    Inherits from:
        Vehicle (Model.GameObjects.Vehicles.Vehicle) which provides movement,
        orientation, and fuel mechanics.

    Attributes:
        __oreCapacity__ (float): Maximum Ore capacity of the Transport.
        __loadedOreAmount__ (float): Current loaded Ore amount.
    """
    __oreCapacity__ : float
    __loadedOreAmount__ : float

    def __init__(
            self,
             screen: pygame.Surface,
             image: pygame.Surface,
             xCoordinate: float = 0,
             yCoordinate: float = 0,
             fuelConsumption: float = 0.05,
             maxSpeed: float = 4.5,
             oreCapacity: float  = 100
     ):
        """
        Initialize an OreTransport with given parameters and default Vehicle properties.

        Args:
            screen (pygame.Surface): Screen surface to draw on.
            image (pygame.Surface): Image representing the vehicle.
            xCoordinate (float): Initial X coordinate.
            yCoordinate (float): Initial Y coordinate.
            fuelConsumption (float): Fuel consumed per unit distance.
            maxSpeed (float): Maximum movement speed.
            oreCapacity (float): Maximum Ore capacity.
        """
        config = getConfig()
        oreTransportConfig = config.getGameConfig().getOreTransportConfig()
        # Initialize the base Vehicle class
        super().__init__(
            xCoordinate,
            yCoordinate,
            collision=True,
            image=image,
            layer=5,
            fuelCapacity=100,
            fuelConsumption=fuelConsumption,
            turningSpeed=oreTransportConfig.getTurningSpeed(),
            maxSpeed=maxSpeed,
            acceleration=oreTransportConfig.getAcceleration(),
            screen=screen
        )
        # OreTransport-specific attributes
        self.__oreCapacity__ = oreCapacity
        self.__loadedOreAmount__ = 0

    def loadOre(self, amount: float) -> float:
        """
        Load Ore into the Transport, returning any surplus Ore that could not be loaded.

        Args:
            amount (float): Amount of Ore to load.

        Returns:
            float: Surplus Ore amount that exceeds capacity (0 if none).
        """
        surplus = max(0.0, self.__loadedOreAmount__ + amount - self.__oreCapacity__)
        self.__loadedOreAmount__ = min(self.__oreCapacity__, self.__loadedOreAmount__ + amount)
            
        if surplus > 0:
            return surplus
        else:
            return 0

    def unloadOre(self, amount: float) -> float:
        """
        Unload a specified amount of Ore from the Transport.

        Args:
            amount (float): Amount of Ore to unload.

        Returns:
            float: Actual unloaded Ore amount (cannot exceed loaded amount).
        """
        unloadedAmount = min(self.__loadedOreAmount__, amount)
        self.__loadedOreAmount__ = max(0.00, self.__loadedOreAmount__ - amount)
        return unloadedAmount

    def oreIsFull(self) -> bool:
        """
        Check if the Ore Transport is fully loaded.

        Returns:
            bool: True if loaded Ore equals capacity, False otherwise.
        """
        return self.__loadedOreAmount__ == self.__oreCapacity__

    def isEmpty(self) -> bool:
        """
        Check if the Ore Transport is empty.

        Returns:
            bool: True if no Ore is loaded, False otherwise.
        """
        return self.__loadedOreAmount__ == 0

    def handleCollisionWithWall(self, direction: str) -> None:
        """
        Handle collision with a wall by bouncing off and adjusting position and orientation.

        Args:
            direction (str): Direction of the wall hit ('top', 'bottom', 'left', 'right').

        Notes:
            Bounces the vehicle back by pushing it away from the wall,
            flips orientation by 180 degrees, and reduces speed to simulate impact.
        """
        bounce_strength = 10

        # Turn the vehicle around by changing its orientation
        self.setOrientation((self.getOrientation() + 180) % 360)
        if direction == 'top':
            self.setYCoordinate(self.getYCoordinate() + bounce_strength)
        elif direction == 'bottom':
            self.setYCoordinate(self.getYCoordinate() - bounce_strength)
        elif direction == 'left':
            self.setXCoordinate(self.getXCoordinate() + bounce_strength)
        elif direction == 'right':
            self.setXCoordinate(self.getXCoordinate() - bounce_strength)

        # Slightly reduce speed to simulate a turn around while keeping momentum
        if self.getSpeed() > 0:
            self.setSpeed(self.getSpeed() * 0.8)
        else:
            self.setSpeed(self.getSpeed() * 0.8)

    def handleCollisionWithObject(self, collisionObject : ImageGameObject) -> None:
        """
        Handle collision with another ImageGameObject by pushing away and reversing orientation.

        Args:
            collisionObject (ImageGameObject): The object this OreTransport collided with.

        Notes:
            Calculates the normalized direction vector between self and the other object,
            moves the OreTransport away to avoid overlap,
            reverses orientation by 180 degrees,
            and reduces speed by 20% to simulate impact.
        """
        # Calculate direction vector between vehicles
        dx : float = self.getXCoordinate() - collisionObject.getXCoordinate()
        dy : float= self.getYCoordinate() - collisionObject.getYCoordinate()

        # Normalize vector to get direction
        distance : int = max(1, int((dx ** 2 + dy ** 2) ** 0.5))
        nx: float = dx / distance
        ny: float = dy / distance

        # Push transport away a bit along the normalized direction
        bounce_strength = 10  # Strength of the bounce
        self.setXCoordinate(int(self.getXCoordinate() + nx * bounce_strength))
        self.setYCoordinate(int(self.getYCoordinate() + ny * bounce_strength))

        # Reflect the orientation (turn around)
        # Reverse the orientation by 180 degrees (reflect the direction of movement)
        self.setOrientation((self.getOrientation() + 180) % 360)

        # Slightly reduce speed to simulate a turn around while keeping momentum
        if self.getSpeed() > 0:
            self.setSpeed(self.getSpeed() * 0.8)  # Keep 90% of the current speed
        else:
            self.setSpeed(self.getSpeed() * 0.8)  # Ensure it doesn't reverse the speed if already negative

    def getLoadedOreAmount(self) -> float:
        return self.__loadedOreAmount__

    def getOreCapacity(self) -> float:
        return self.__oreCapacity__

    def __str__(self) -> str:
        """
        Return a detailed string representation of the OreTransport instance.

        Includes position, orientation, speed, ore load status, and base Vehicle attributes.
        """
        return (
            f"{type(self).__name__}("
            f"xCoordinate={self.getXCoordinate()}, "
            f"yCoordinate={self.getYCoordinate()}, "
            f"orientation={self.getOrientation()}, "
            f"speed={self.getSpeed()}, "
            f"oreCapacity={self.__oreCapacity__}, "
            f"loadedOreAmount={self.__loadedOreAmount__}, "
            f"fuelLevel={self.getFuelLevel()}, "
            f"maxSpeed={self.getMaxSpeed()})"
        )