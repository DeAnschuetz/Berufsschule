class GameDifficulty:
    """
    A Configuration Class that Defines Parameters for Game Difficulty.

    Attributes:
        __percentageToCollect__ (float): Percentage of the Total Ore to be Collected.
        __totalOre__ (int): Total Amount of Ore in the Game.
        __transporterCapacity__ (float): Maximum Capacity of the Transporter.
        __fuelConsumption__ (float): Fuel Consumption Rate per Movement Unit.
        __helicopterMaxSpeed__ (float): Maximum Speed of the Helicopter.
        __transporterMaxSpeed__ (float): Maximum Speed of the Transporter.
    """
    __percentageToCollect__ : float
    __totalOre__ : int
    __transporterCapacity__ : float
    __fuelConsumption__ : float
    __helicopterMaxSpeed__ : float
    __transporterMaxSpeed__ : float

    def __init__(self, percentageToCollect : float, totalOre : int, transporterCapacity : float, fuelConsumption : float, helicopterMaxSpeed: float, transporterMaxSpeed : float):
        """
        Initialize the GameDifficulty Configuration.

        Args:
            percentageToCollect (float): Percentage of Ore Required to Win (0–100).
            totalOre (int): Total Amount of Ore in the Game World.
            transporterCapacity (float): Maximum Capacity of the Transporter.
            fuelConsumption (float): Fuel Usage Rate per Unit of Movement.
            helicopterMaxSpeed (float): Maximum Speed of the Helicopter.
            transporterMaxSpeed (float): Maximum Speed of the Transporter.
        """
        self.__percentageToCollect__ = percentageToCollect
        self.__totalOre__ = totalOre
        self.__transporterCapacity = transporterCapacity
        self.__fuelConsumption__ = fuelConsumption
        self.__helicopterMaxSpeed__ = helicopterMaxSpeed
        self.__transporterMaxSpeed__= transporterMaxSpeed

    def getOreToCollect(self) -> float:
        """Return ore Amount to collect."""
        return self.__percentageToCollect__ / 100 * self.__totalOre__

    def getTransporterCapacity(self) -> float:
        """Return Transporter Capacity."""
        return self.__transporterCapacity

    def getTotalOre(self) -> int:
        """Return total Ore."""
        return self.__totalOre__

    def getFuelConsumption(self) -> float:
        """Return Fuel Consumption."""
        return self.__fuelConsumption__

    def getHelicopterMaxSpeed(self) -> float:
        """Return Helicopter max speed."""
        return self.__helicopterMaxSpeed__

    def getTransporterMaxSpeed(self) -> float:
        """Return Transporter max speed."""
        return self.__transporterMaxSpeed__

    def __str__(self):
        return (
            f"GameDifficulty (oreToCollect={self.getOreToCollect()}, totalOre={self.__totalOre__}, "
            f"percentageToCollect={self.__percentageToCollect__}, transporterCapacity={self.__transporterCapacity}, "
            f"fuelConsumption={self.__fuelConsumption__}, helicopterMaxSpeed={self.__helicopterMaxSpeed__}, "
            f"transporterMaxSpeed={self.__transporterMaxSpeed__})"
        )