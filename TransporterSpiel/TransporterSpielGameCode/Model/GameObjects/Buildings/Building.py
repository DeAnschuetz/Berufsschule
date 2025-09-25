import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject

class Building(ImageGameObject):
    """
    A Class representing a Building that can Store and Transfer Resources.

    Inherits from:
        ImageGameObject (Model.GameObjects.Base.ImageGameObject)

    Attributes:
        __transferRate__ (float): The Maximum Amount of Resource that can be Transferred per Call.
        __totalResourceStored__ (float): The Total Amount of Resource currently Stored in the Building.
    """
    __transferRate__: float
    __totalResourceStored__ : float

    def __init__(self,image: pygame.Surface, screen: pygame.Surface, xCoordinate: float = 0.0, yCoordinate: float = 0.0, collision: bool = False,  layer: int = 1, totalResourceStored : float = 0, transferRate: int = 100) -> None:
        """
        Initialize a Building Object.

        Args:
            image (pygame.Surface): The Image used to Visually Represent the Building.
            screen (pygame.Surface): The Surface on which to Draw the Building.
            xCoordinate (float): The X-Coordinate of the Building in the Game World.
            yCoordinate (float): The Y-Coordinate of the Building in the Game World.
            collision (bool): Whether the Building has Collision Enabled.
            layer (int): The Drawing Layer of the Building.
            totalResourceStored (float): The Initial Resource Amount Stored in the Building.
            transferRate (int): The Maximum Transfer Rate of the Building per Request.
        """
        super().__init__(
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            collision=collision,
            image=image,
            layer=layer,
            screen=screen
        )
        self.__transferRate__ = transferRate
        self.__totalResourceStored__ = totalResourceStored

    def giveResource(self) -> float:
        """
        Transfer Resources out of the Building up to the defined Transfer Rate.

        Returns:
            float: The Actual Amount of Resource Transferred. Returns 0 if no Resources are Available.
        """
        if self.__totalResourceStored__ <= 0:
            return 0
        # Only Transfer what is Available, limited by Transfer Rate
        amountTransferred =  min(self.__transferRate__, self.__totalResourceStored__)
        self.__totalResourceStored__ -= amountTransferred
        return amountTransferred

    def getTotalResourceStored(self) -> float:
        return self.__totalResourceStored__

    def takeResource(self, transferredAmount : float) -> None:
        """
        Add the given Amount of Resource to the Building's Storage.

        Args:
            transferredAmount (float): The Amount of Resource to Store.
        """
        self.__totalResourceStored__ += transferredAmount

    def getTransferRate(self):
        return self.__transferRate__

    def __str__(self) -> str:
        """
        Return a detailed String Representation of the Building Instance,
        including all Attributes from this Class and the Superclass.
        """
        return (
            f"{type(self).__name__} (xCoordinate={self.getXCoordinate()}, yCoordinate={self.getYCoordinate()}, "
            f"collision={self.getCollision()}, collisionRadius={self.getCollisionRadius()}, "
            f"image=<{type(self.getImage()).__name__}>, layer={self.getLayer()}, width={self.getWidth()}, "
            f"height={self.getHeight()}, screen=<{type(self.getScreen()).__name__}>, orientation={self.getOrientation()}, "
            f"transferRate={self.__transferRate__}, totalResourceStored={self.__totalResourceStored__})"
        )