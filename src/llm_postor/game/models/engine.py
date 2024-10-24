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

ROOM_COORDINATES = {
    GameLocation.LOC_CAFETERIA: (2.2, 1.8),
    GameLocation.LOC_REACTOR: (0.4, 1.2),
    GameLocation.LOC_UPPER_ENGINE: (0.75, 1.75),
    GameLocation.LOC_LOWER_ENGINE: (0.75, 0.6),
    GameLocation.LOC_SECURITY: (1.1, 1.2),
    GameLocation.LOC_MEDBAY: (1.5, 1.4),
    GameLocation.LOC_ELECTRICAL: (1.5, 0.8),
    GameLocation.LOC_STORAGE: (2.1, 0.5),
    GameLocation.LOC_ADMIN: (2.7, 0.9),
    GameLocation.LOC_COMMUNICATIONS: (2.7, 0.3),
    GameLocation.LOC_O2: (2.8, 1.3),
    GameLocation.LOC_WEAPONS: (3.1, 1.8),
    GameLocation.LOC_SHIELDS: (3.1, 0.6),
    GameLocation.LOC_NAVIGATION: (3.8, 1.3),
}
