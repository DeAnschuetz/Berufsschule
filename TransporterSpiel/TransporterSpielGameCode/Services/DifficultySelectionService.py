import pygame

from Model.GameObjects.Base.ImageGameObject import ImageGameObject
from Model.GameObjects.MenuElements.BorderBox import BorderOnlySurfaceFactory
from Model.GameObjects.Messages.ErrorMessage import ErrorTextGameObject
from Model.GameObjects.Game.GameDifficulty import GameDifficulty
from Model.GameObjects.Messages.TextGameObject import TextGameObject
from Model.GameObjects.Exceptions.QuitException import QuitException
from Services.ConfigService import getConfig


def getDefaultFields(presetValues) -> list[tuple[str, str]]:
    """
    Generate a list of default fields with their corresponding preset values.

    Args:
        presetValues (dict[str, str]): Preset values for each field.

    Returns:
        list[tuple[str, str]]: List of field names and their corresponding values.
    """
    return [
        ("Total Ore", presetValues["Total Ore"]),
        ("Percentage to Collect", presetValues["Percentage to Collect"]),
        ("Ore to Collect", presetValues["Ore to Collect"]),
        ("Transporter Capacity", presetValues["Transporter Capacity"]),
        ("Fuel Consumption", presetValues["Fuel Consumption"]),
        ("Helicopter Max Speed", presetValues["Helicopter Max Speed"]),
        ("Transporter Max Speed", presetValues["Transporter Max Speed"])
    ]

class DifficultySelectionService:
    """
    A Class to manage the Difficulty Selection Screen, allowing users to input and confirm game difficulty settings.

    Attributes:
        __screen__ (pygame.display): The Pygame display surface.
        __clock__ (pygame.time.Clock): The Pygame clock object.
        __smallFont__ (int): Font size for small text.
        __bigFont__ (int): Font size for large text.
        __fields__ (list[tuple[str, str]]): List of field labels and their current values.
        __lastInputFieldMessage__ (TextGameObject): The last input field message displayed.
        __inputFields__ (list[ImageGameObject]): List of input field game objects.
        __gameDifficulty__ (GameDifficulty): The configured game difficulty object.
        __presetValues__ (dict[str, str]): Preset values for each field.
        __inputActive__ (bool): Flag indicating if input is currently active.
        __currentField__ (int): Index of the currently active input field.
        __confirmMode__ (bool): Flag indicating if the confirmation mode is active.
    """
    __screen__ : pygame.display
    __clock__ : pygame.time.Clock
    __smallFont__ : int
    __bigFont__ : int
    __fields__: list[tuple[str, str]]
    __lastInputFieldMessage__: TextGameObject
    __inputFields__: list[ImageGameObject]
    __gameDifficulty__: GameDifficulty

    __presetValues__: dict[str, str]
    __inputActive__: bool
    __currentField__: int
    __confirmMode__: bool

    def __init__(self, screen : pygame, clock : pygame.time.Clock):
        """
        Initialize the DifficultySelectionService with the given screen and clock.

        Args:
            screen (pygame.Surface): The Pygame display surface.
            clock (pygame.time.Clock): The Pygame clock object.
        """
        config = getConfig()
        difficultySelectionConfig = config.getScreenConfig().getHudConfig().getDifficultySelectionConfig()
        difficultyConfig = config.getGameConfig().getDifficultyConfig()
        self.__screenWidth__ = config.getScreenConfig().getScreenWidth()
        self.__presetValues__ = {
            "Total Ore": str(difficultyConfig.getTotalOre()),
            "Percentage to Collect": str(difficultyConfig.getPercentageToCollect()),
            "Ore to Collect": str(difficultyConfig.getTotalOre() * difficultyConfig.getPercentageToCollect()/100),
            "Transporter Capacity": str(difficultyConfig.getTransporterCapacity()),
            "Fuel Consumption": str(difficultyConfig.getFuelConsumption()),
            "Helicopter Max Speed": str(difficultyConfig.getHelicopterMaxSpeed()),
            "Transporter Max Speed": str(difficultyConfig.getTransporterMaxSpeed())
        }
        self.__screen__ = screen
        self.__clock__ = clock
        self.__smallFont__ = difficultySelectionConfig.getSmallFont()
        self.__bigFont__ = difficultySelectionConfig.getBigFont()
        self.__fields__ = getDefaultFields(self.__presetValues__)
        self.__initInputFields__()

    def selectDifficulty(self) -> GameDifficulty:
        """
        Launch the Difficulty Selection Screen and handle user input.

        Returns:
            GameDifficulty: The configured game difficulty object.
        """
        self.__currentField__ = 0
        self.__inputActive__ = True
        self.__confirmMode__ = False
        self.__resetInputFields__()

        while self.__inputActive__:
            self.__updateFieldValues__()

            self.__screen__.fill((0, 0, 0))
            if self.__currentField__ == 2:
                self.__currentField__ += 1
                continue
            if not self.__confirmMode__:
                self.__drawInputFields__()
            else:
                self.__drawConfirmFields__()

            pygame.display.flip()
            self.__handleInput__()

        return self.__gameDifficulty__

    def __resetInputFields__(self):
        """
        Reset the input fields to their default preset values.
        """
        self.__fields__ = getDefaultFields(self.__presetValues__)

    def __updateFieldValues__(self):
        """
        Update the 'Ore to Collect' field based on 'Total Ore' and 'Percentage to Collect' inputs.
        """
        try:
            totalOre = float(self.__fields__[0][1])
        except ValueError as e:
            totalOre = 0
            if totalOre < 500:
                totalOre = 500
            if totalOre > 10000:
                totalOre = 10000
        try:
            percentageToCollect = float(self.__fields__[1][1])
        except ValueError as e:
            percentageToCollect = 0
        if percentageToCollect < 0:
            percentageToCollect = 0
        elif percentageToCollect > 100:
            percentageToCollect = 100
        newOreToCollect: str = str(int(percentageToCollect * totalOre / 100))
        self.__presetValues__["Ore to Collect"] = newOreToCollect
        self.__fields__[2] = ("Ore to Collect", str(newOreToCollect))

    def __handleInput__(self):
        """
        Handle user input events for navigating and editing fields, confirming settings, or quitting.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitException()

            if event.type == pygame.KEYDOWN:
                if not self.__confirmMode__:

                    if event.key == pygame.K_RETURN:
                        # If no change was made, use the preset value
                        if self.__fields__[self.__currentField__][1] == self.__presetValues__[self.__fields__[self.__currentField__][0]]:
                            if self.__currentField__ < len(self.__fields__) - 1:
                                self.__currentField__ += 1
                            else:
                                self.__confirmMode__ = True
                        else:
                            if self.__currentField__ < len(self.__fields__) - 1:
                                self.__currentField__ += 1
                            else:
                                self.__confirmMode__ = True
                    elif event.key == pygame.K_BACKSPACE:
                        label, text = self.__fields__[self.__currentField__]
                        self.__fields__[self.__currentField__] = (label, text[:-1])
                    elif event.key == pygame.K_ESCAPE:
                        self.__confirmMode__ = True
                    else:
                        label, text = self.__fields__[self.__currentField__]
                        self.__fields__[self.__currentField__] = (label, text + event.unicode)
                else:
                    if event.key == pygame.K_RETURN:
                        # Confirm and create difficulty
                        try:
                            self.__createGameDifficultyFromFields__()
                        except ValueError:
                            error: ErrorTextGameObject = ErrorTextGameObject(
                                screen=self.__screen__,
                                message="Invalid input! Please enter valid numbers."
                            )
                            error.draw()

                            self.__resetInputFields__()
                            self.__currentField__ = 0
                            self.__confirmMode__ = False

                    if event.key == pygame.K_ESCAPE:
                        self.__resetInputFields__()
                        self.__currentField__ = 0
                        self.__confirmMode__ = False
                    if event.key == pygame.K_q:
                        raise QuitException()
        return self.__currentField__

    def __createGameDifficultyFromFields__(self):
        """
        Create a GameDifficulty object from the current field values and deactivate input.
        """
        print(self.__fields__)
        totalOre = int(self.__fields__[0][1])
        percentageToCollect = float(self.__fields__[1][1])
        transporterCapacity = float(self.__fields__[3][1])
        fuelConsumption = float(self.__fields__[4][1])
        helicopterMaxSpeed = float(self.__fields__[5][1])
        transporterMaxSpeed = float(self.__fields__[6][1])
        self.__gameDifficulty__ = GameDifficulty(
            percentageToCollect=percentageToCollect,
            totalOre=totalOre,
            transporterCapacity=transporterCapacity,
            fuelConsumption=fuelConsumption,
            helicopterMaxSpeed=helicopterMaxSpeed,
            transporterMaxSpeed=transporterMaxSpeed
        )
        self.__inputActive__ = False

    def __drawConfirmFields__(self):
        """
        Draw the confirmation screen displaying all current settings and instructions.
        """
        # Confirm screen
        textMessage: TextGameObject = TextGameObject(
            screen=self.__screen__,
            message="Confirm the following settings?",
            xCoordinate=self.__screenWidth__ / 2,
            yCoordinate=50,
            fontSize=self.__smallFont__,
        )
        textMessage.draw()
        for idx, (label, text) in enumerate(self.__fields__):
            text_line = f"{label}: {text}"
            textMessage: TextGameObject = TextGameObject(
                screen=self.__screen__,
                message=text_line,
                xCoordinate=self.__screenWidth__ / 2,
                yCoordinate=150 + idx * 60,
                fontSize=self.__smallFont__,
                color=(0, 255, 0)
            )
            textMessage.draw()
        textMessage: TextGameObject = TextGameObject(
            screen=self.__screen__,
            message="Press ENTER to Confirm or ESCAPE to Restart and Q to Quit.",
            xCoordinate=self.__screenWidth__ / 2,
            yCoordinate=630,
            fontSize=self.__smallFont__,
            color=(200, 200, 200)
        )
        textMessage.draw()

    def __drawInputFields__(self):
        # Create all input self.__fields__
        textMessage: TextGameObject
        textField: TextGameObject
        labelField: TextGameObject
        textFields: list[TextGameObject] = [obj for obj in self.__inputFields__ if isinstance(obj, TextGameObject)]
        entryFieldBorder: ImageGameObject = next(
            (obj for obj in self.__inputFields__ if isinstance(obj, ImageGameObject)), None)
        for idx, (label, text) in enumerate(self.__fields__):
            if text is None or text == '':
                text = ' '
            yPos = 100 + idx * 80
            textField: TextGameObject = next((obj for obj in textFields if obj.getIdentifier() == label), None)
            textField.updateMessage(text)

            if self.__currentField__ == 2:
                continue
            if idx == self.__currentField__:
                entryFieldBorder.setYCoordinate(yPos)
        inputFields: list[ImageGameObject] = self.__inputFields__
        inputFields.sort(key=lambda obj: obj.getLayer())
        for inputField in inputFields:
            inputField.draw()
        confirmMessage: TextGameObject = next((obj for obj in textFields if obj.getIdentifier() == "confirmMessage"), None)
        confirmMessage.draw()

    def __initInputFields__(self):
        """
        Creates all the Input Fields needed for the Difficulty Selection Service.
        """
        self.__inputFields__ = []
        inputFieldObject: TextGameObject
        for idx, (label, text) in enumerate(self.__fields__):
            if text is None or text == '':
                text = ' '
            yPos = 100 + idx * 80
            inputFieldObject = TextGameObject(
                screen=self.__screen__,
                message=label,
                xCoordinate=self.__screenWidth__ / 2 - 150,
                yCoordinate=yPos,
                fontSize=self.__smallFont__,
                color=(0, 255, 0)
            )
            self.__inputFields__.append(inputFieldObject)
            inputFieldObject = TextGameObject(
                screen=self.__screen__,
                message=text,
                identifier=label,
                xCoordinate=self.__screenWidth__ / 2 + 150,
                yCoordinate=yPos,
                fontSize=self.__smallFont__,
            )
            self.__inputFields__.append(inputFieldObject)

        entryFieldBorderImage: pygame.Surface = pygame.Surface((200, 50))
        borderBox: BorderOnlySurfaceFactory = BorderOnlySurfaceFactory(
            base_surface=pygame.Surface((200, 50)),
            border_color=(255, 255, 255),
            border_thickness=2

        )
        entryFieldBorderImage.fill((255, 255, 255))
        entryFieldBorder = ImageGameObject(
            screen=self.__screen__,
            image=borderBox.getBorderBox(),
            xCoordinate=self.__screenWidth__ / 2 + 150,
            yCoordinate=0,
        )
        self.__inputFields__.append(entryFieldBorder)
        inputFieldObject = TextGameObject(
            screen=self.__screen__,
            message="Press ENTER to confirm each field. Or ESCAPE to Start a Game with the current Settings",
            identifier="confirmMessage",
            xCoordinate=self.__screenWidth__ / 2,
            yCoordinate=630,
            fontSize=self.__smallFont__,
            color=(0, 255, 0)
        )
        self.__inputFields__.append(inputFieldObject)