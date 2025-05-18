import pygame


class BorderOnlySurfaceFactory:
    """
    A Class representing a Factory to create a Surface with only the Border drawn, based on a given Base Surface.

    Attributes:
        __borderColor__ (tuple): Color of the Border as an RGB Tuple.
        __baseSurface__ (pygame.Surface): The Base Surface to base the Border on.
        __borderThickness__ (int): Thickness of the Border in pixels.
        __surface__ (pygame.Surface): The Surface containing only the Border.
    """
    __borderColor__: tuple
    __baseSurface__: pygame.Surface
    __borderThickness__: int
    __surface__: pygame.Surface

    def __init__(self, base_surface: pygame.Surface, border_color=(255, 255, 255), border_thickness=2):
        """
        Initialize a BorderOnlySurface Object.

        Args:
            base_surface (pygame.Surface): The Base Surface to derive the Border size from.
            border_color (tuple): The RGB Color of the Border (default white).
            border_thickness (int): Thickness of the Border in pixels (default 2).
        """
        self.__baseSurface__ = base_surface
        self.__borderColor__ = border_color
        self.__borderThickness__ = border_thickness
        self.__surface__ = self.__creatBorderOnlySurface__()

    def __creatBorderOnlySurface__(self) -> pygame.Surface:
        """
        Create and return a Surface with only the Border drawn.

        Returns:
            pygame.Surface: Surface containing only the Border with transparency elsewhere.
        """
        width, height = self.__baseSurface__.get_size()
        thickness = self.__borderThickness__

        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw only border areas (leave everything else transparent)
        pygame.draw.rect(surface=surface, color=self.__borderColor__, rect=(0, 0, width, thickness))
        pygame.draw.rect(surface=surface, color=self.__borderColor__, rect=(0, height - thickness, width, thickness))
        pygame.draw.rect(surface=surface, color=self.__borderColor__, rect=(0, thickness, thickness, height - 2 * thickness))
        pygame.draw.rect(surface=surface, color=self.__borderColor__, rect=(width - thickness, thickness, thickness, height - 2 * thickness))

        return surface

    def getBorderBox(self) -> pygame.Surface:
        """Return the Surface containing only the Border."""
        return self.__surface__