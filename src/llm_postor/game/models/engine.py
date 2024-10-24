from enum import Enum

class GamePhase(str, Enum):
    MAIN_MENU = "Main Menu"
    ACTION_PHASE = "Action Phase"
    DISCUSS = "Discuss"


class GameLocation(str, Enum):
    LOC_CAFETERIA = "Cafeteria"
    LOC_REACTOR = "Reactor"
    LOC_UPPER_ENGINE = "Upper Engine"
    LOC_LOWER_ENGINE = "Lower Engine"
    LOC_SECURITY = "Security"
    LOC_MEDBAY = "Medbay"
    LOC_ELECTRICAL = "Electrical"
    LOC_STORAGE = "Storage"
    LOC_ADMIN = "Admin"
    LOC_COMMUNICATIONS = "Communications"
    LOC_O2 = "O2"
    LOC_WEAPONS = "Weapons"
    LOC_SHIELDS = "Shields"
    LOC_NAVIGATION = "Navigation"
    LOC_UNKNOWN = "Unknown"


DOORS: dict[GameLocation, list] = {
    GameLocation.LOC_CAFETERIA: [
        GameLocation.LOC_MEDBAY,
        GameLocation.LOC_ADMIN,
        GameLocation.LOC_WEAPONS,
    ],
    GameLocation.LOC_REACTOR: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_LOWER_ENGINE,
    ],
    GameLocation.LOC_UPPER_ENGINE: [
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_MEDBAY,
    ],
    GameLocation.LOC_LOWER_ENGINE: [
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_SECURITY,
        GameLocation.LOC_ELECTRICAL,
    ],
    GameLocation.LOC_SECURITY: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_REACTOR,
        GameLocation.LOC_LOWER_ENGINE,
    ],
    GameLocation.LOC_MEDBAY: [
        GameLocation.LOC_UPPER_ENGINE,
        GameLocation.LOC_CAFETERIA,
    ],
    GameLocation.LOC_ELECTRICAL: [
        GameLocation.LOC_LOWER_ENGINE,
        GameLocation.LOC_STORAGE,
    ],
    GameLocation.LOC_STORAGE: [
        GameLocation.LOC_ELECTRICAL,
        GameLocation.LOC_ADMIN,
        GameLocation.LOC_COMMUNICATIONS,
        GameLocation.LOC_SHIELDS,
    ],
    GameLocation.LOC_ADMIN: [GameLocation.LOC_CAFETERIA, GameLocation.LOC_STORAGE],
    GameLocation.LOC_COMMUNICATIONS: [
        GameLocation.LOC_STORAGE,
        GameLocation.LOC_SHIELDS,
    ],
    GameLocation.LOC_O2: [
        GameLocation.LOC_SHIELDS,
        GameLocation.LOC_WEAPONS,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_WEAPONS: [
        GameLocation.LOC_CAFETERIA,
        GameLocation.LOC_O2,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_SHIELDS: [
        GameLocation.LOC_STORAGE,
        GameLocation.LOC_COMMUNICATIONS,
        GameLocation.LOC_O2,
        GameLocation.LOC_NAVIGATION,
    ],
    GameLocation.LOC_NAVIGATION: [
        GameLocation.LOC_WEAPONS,
        GameLocation.LOC_O2,
        GameLocation.LOC_SHIELDS,
    ],
}
