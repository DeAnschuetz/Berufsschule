import pygame
import math

from Model.GameObjects.Base.GameObject import GameObject

def distanceBetween(obj1: 'ImageGameObject', obj2: 'ImageGameObject') -> float:
    """
    Calculate the Euclidean Distance between two GameObject Instances.

    Args:
        obj1 (ImageGameObject): First Game Object.
        obj2 (ImageGameObject): Second Game Object.

    Returns:
        float: Distance between the two Objects.
    """
    # Calculate the x and y Distance between the 2 Objects and returns the Euclidean distance
    dx = obj1.getXCoordinate() - obj2.getXCoordinate()
    dy = obj1.getYCoordinate() - obj2.getYCoordinate()
    return math.hypot(dx, dy)

class ImageGameObject(GameObject):
    """
    A Class representing a Game Object with an associated Image and optional Collision.

    Inherits from:
        GameObject (Model.GameObjects.Base.GameObject): Base Class for all Game Objects.

    Attributes:
        __collision__ (bool): Whether the Object participates in Collision.
        __collisionRadius__ (float): Radius used for Collision Detection.
        __image__ (pygame.Surface): The Image representing the Object.
        __layer__ (int): Drawing Layer of the Object.
        __width__ (int): Width of the Image.
        __height__ (int): Height of the Image.
        __orientation__ (float): Rotation Angle in Degrees.
    """
    __collision__ : bool
    __collisionRadius__ : float
    __image__ : pygame.Surface
    __layer__ : int
    __width__: int
    __height__: int
    __orientation__ : float
    
    def __init__(self, image : pygame.Surface, screen: pygame.Surface, xCoordinate : float = 0.0, yCoordinate : float =0.0, collision : bool = True, layer : int = 0, identifier: str = "") -> None:
        """
        Initialize an ImageGameObject Instance.

        Args:
            image (pygame.Surface): The Image representing the Game Object.
            screen (pygame.Surface): Surface to draw the Object on.
            xCoordinate (float): Initial X Coordinate.
            yCoordinate (float): Initial Y Coordinate.
            collision (bool): Whether the Object can collide.
            layer (int): Drawing Layer.
            identifier (str): Optional Identifier for the Object.
        """
        super().__init__(
            screen=screen,
            xCoordinate=xCoordinate,
            yCoordinate=yCoordinate,
            baseLayer=layer,
            identifier=identifier
        )
        self.__collision__ = collision
        self.__image__ = image
        self.__layer__ = layer
        self.__width__ = image.get_width() if image else 0
        self.__height__ = image.get_height() if image else 0
        # Use the larger image dimension as the base for collision detection
        self.__collisionRadius__ = max(self.__width__, self.__height__) // 2
        self.__orientation__ = 0.00

    def draw(self) -> None:
        """
        Draw the Object on the Screen with its current Orientation.
        """
        # Rotate the Image around its center and draw it
        rotated_image = pygame.transform.rotate(self.__image__, self.__orientation__)
        new_rect = rotated_image.get_rect(center=(self.__xCoordinate__, self.__yCoordinate__))
        self.__screen__.blit(source=rotated_image, dest=new_rect.topleft)

    def areColliding(self, object2: 'ImageGameObject', ignoreLayer: bool=False, ignoreCollision: bool=True) -> bool:
        """
        Check whether this Object is colliding with another.

        Args:
            object2 (ImageGameObject): Another Game Object to check Collision with.
            ignoreLayer (bool): Whether to ignore the Layer during the check.
            ignoreCollision (bool): Whether to ignore the Collision Property during the check.

        Returns:
            bool: True if Colliding, otherwise False.
        """
        if ((self.getLayer() == object2.getLayer()) or ignoreLayer) and (ignoreCollision or (self.getCollision() and object2.getCollision())):
            # Compare the distance to the sum of both collision radii
            distance = distanceBetween(self, object2)
            return distance <= (self.getCollisionRadius() + object2.getCollisionRadius())
        else:
            return False

    def setTopLeft(self, topLeft: tuple[float, float]):
        """
        Set the Position using the Top-Left Corner of the Image.

        Args:
            topLeft (tuple[float, float]): (X, Y) Coordinates of the Top-Left Corner.
        """
        # Set the X and Y Coordinates of the Object to represent the given top-left Corner
        self.__xCoordinate__ = topLeft[0] + self.__width__ / 2
        self.__yCoordinate__ = topLeft[1] + self.__height__ / 2

    def getTopLeft(self) -> tuple[float, float]:
        """
        Get the Top-Left Position of the Image.

        Returns:
            tuple[float, float]: (X, Y) of the Top-Left Corner.
        """
        topLeftX = self.__xCoordinate__ - self.__width__ / 2
        topLeftY = self.__yCoordinate__ - self.__height__ / 2
        return topLeftX, topLeftY

    def getCollision(self) -> bool:
        return self.__collision__

    def setCollision(self, collision: bool) -> None:
        self.__collision__ = collision

    def getCollisionRadius(self) -> float:
        return self.__collisionRadius__

    def setCollisionRadius(self, collisionRadius: float) -> None:
        self.__collisionRadius__ = collisionRadius

    def getImage(self) -> pygame.Surface:
        return self.__image__

    def setImage(self, image : pygame.Surface):
        self.__image__ = image
        self.__width__ = image.get_width()
        self.__height__ = image.get_height()
        self.__collisionRadius__ = max(self.__width__, self.__height__) // 2

    def getLayer(self) -> int:
        return self.__layer__

    def setLayer(self, layer: int) -> None:
        self.__layer__ = layer

    def getWidth(self) -> int:
        return self.__width__

    def getHeight(self) -> int:
        return self.__height__

    def getOrientation(self) -> float:
        return self.__orientation__

    def setOrientation(self, orientation: float) -> None:
        """
        Set the orientation Angle (in degrees).
        Ensures it wraps around 360 degrees.
        """
        self.__orientation__ = orientation % 360

    def setAlpha(self, alpha: int) -> None:
        if self.__image__ is not None:
            self.__image__.set_alpha(alpha)

    def getAlpha(self) -> int:
        return self.__image__.get_alpha()

    def __str__(self) -> str:
        """
        Return a detailed String Representation of the ImageGameObject Instance,
        including all Attributes from this Class and the Superclass.
        """
        return (
            f"{type(self).__name__} (xCoordinate={self.getXCoordinate()}, yCoordinate={self.getYCoordinate()}, "
            f"collision={self.getCollision()}, collisionRadius={self.getCollisionRadius()}, "
            f"image=<{type(self.getImage()).__name__}>, layer={self.getLayer()}, width={self.getWidth()}, "
            f"height={self.getHeight()}, screen=<{type(self.getScreen()).__name__}>, orientation={self.getOrientation()})"
        )