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

    __collision__ : bool
    __collisionRadius__ : float
    __image__ : pygame.Surface
    __layer__ : int
    __width__: int
    __height__: int
    __orientation__ : float
    
    def __init__(self, image : pygame.Surface, screen: pygame.Surface, xCoordinate : float = 0.0, yCoordinate : float =0.0, collision : bool = True, layer : int = 0, identifier: str = "") -> None:
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
        # Set the Collision Radius to the whole number maximum of the width and height of the Object Divided by 2
        self.__collisionRadius__ = max(self.__width__, self.__height__) // 2
        self.__orientation__ = 0.00

    def setTopLeft(self, topLeft: tuple[float, float]):
        """
        Set the Position using the top-left Corner of the Image.
        Args:
            topLeft (tuple[float, float]): (X, Y) of top-left Corner.
        """
        # Set the X and Y Coordinates of the Object to represent the given top-left Corner
        self.__xCoordinate__ = topLeft[0] + self.__width__ / 2
        self.__yCoordinate__ = topLeft[1] + self.__height__ / 2

    def getTopLeft(self) -> tuple[float, float]:
        """
        Get the top-left Position of the Image.

        Returns:
            tuple[float, float]: (X, Y) of top-left Corner.
        """
        topLeftX = self.__xCoordinate__ - self.__width__ / 2
        topLeftY = self.__yCoordinate__ - self.__height__ / 2
        return topLeftX, topLeftY

    def getCollision(self) -> bool:
        """Return whether Collision is enabled."""
        return self.__collision__

    def setCollision(self, collision: bool) -> None:
        """Enable or disable Collision."""
        self.__collision__ = collision

    def getCollisionRadius(self) -> float:
        """Return the Collision Radius."""
        return self.__collisionRadius__

    def setCollisionRadius(self, collisionRadius: float) -> None:
        """Set the Collision Radius."""
        self.__collisionRadius__ = collisionRadius

    def getImage(self) -> pygame.Surface:
        """Return the Image Surface."""
        return self.__image__

    def setImage(self, image : pygame.Surface):
        """Set the Image Surface and update Width, Height, and Collision Radius."""
        self.__image__ = image
        self.__width__ = image.get_width()
        self.__height__ = image.get_height()
        self.__collisionRadius__ = max(self.__width__, self.__height__) // 2

    def getLayer(self) -> int:
        """Return the drawing Layer."""
        return self.__layer__

    def setLayer(self, layer: int) -> None:
        """Set the drawing Layer."""
        self.__layer__ = layer

    def getWidth(self) -> int:
        """Return the Width of the Image."""
        return self.__width__

    def getHeight(self) -> int:
        """Return the Height of the Image."""
        return self.__height__

    def getOrientation(self) -> float:
        """Return the orientation Angle."""
        return self.__orientation__

    def setOrientation(self, orientation: float) -> None:
        """
        Set the orientation Angle (in degrees).
        Ensures it wraps around 360 degrees.
        """
        self.__orientation__ = orientation % 360

    def setAlpha(self, alpha: int) -> None:
        """Set the alpha transparency level of the image."""
        if self.__image__ is not None:
            self.__image__.set_alpha(alpha)

    def getAlpha(self) -> int:
        """Return the alpha transparency level of the Image."""
        return self.__image__.get_alpha()

    def draw(self) -> None:
        """Draw the Object on the Screen with its current Orientation."""
        # TODO Prüfen
        # Rotate the Image according to its current orientation
        rotated_image = pygame.transform.rotate(self.__image__, self.__orientation__)
        new_rect = rotated_image.get_rect(center=(self.__xCoordinate__, self.__yCoordinate__))
        self.__screen__.blit(source=rotated_image, dest=new_rect.topleft)

    def areColliding(self, object2: 'ImageGameObject', ignoreLayer: bool=False, ignoreCollision: bool=True) -> bool:
        """
        Check whether this Object is colliding with another.

        Args:
            object2 (ImageGameObject): Another game Object to check Collision with.
            ignoreLayer (bool): Whether to ignore the Layer during check.
            ignoreCollision (bool): Whether to ignore the Collision during check.

        Returns:
            bool: True if colliding, else False.
        """
        # Check if the Objects are on the same Layer or if the Layer should be ignored

        if ((self.getLayer() == object2.getLayer()) or ignoreLayer) and (ignoreCollision or (self.getCollision() and object2.getCollision())):
            # Get the distance between the 2 Objects
            distance = distanceBetween(self, object2)
            # Return weather the distance is smaller the combined Collision Radii
            return distance <= (self.getCollisionRadius() + object2.getCollisionRadius())
        else:
            return False