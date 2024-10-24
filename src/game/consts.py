NUM_MAX_PLAYERS = 10
NUM_SHORT_TASKS = 8
NUM_LONG_TASKS = 2
NUM_CHATS = 5
MIN_NAME = 2
IMPOSTOR_COOLDOWN = 1
STATE_FILE = "game_state.json"
PLAYER_COLORS = [
    "red",
    "blue",
    "green",
    "yellow",
    "purple",
    "orange",
    "pink",
    "brown",
    "cyan",
    "lime",
]
ASCII_MAP = """
    |\\----------------|--------------|----------------|-------------\\
	|                                                                 \\
	| UPPER ENGINE                        CAFETERIA       WEAPONS      \\
	|                 |-     --------|                |                 \\
	|/--------|    |--|       MEDBAY |                |                  \\
	          |    |                 |                |                   \\-----\\
	/---------|    |-------\\        |                |----------|        |       \\
	|         |    |        \\       |---|     |------|          |                 |
	|                        \\      |                |                            |
	| REACTOR        SECURITY |      |  ADMIN OFFICE  |   O2           NAVIGATION  |
	|                         |      |                |          |                 |
	|         |    |          |      |---|     |----|-|----------|                 |
	\\--------|    |----------|------|              |                     |       /
	          |    |                 |                                    /------/
	|\\-------|    |--|              |                                   /
	|                 |              |              |--    --|          /
	| LOWER ENGINE       ELECTRICAL       STORAGE   | COMMS  | SHIELDS /
	|                                               |        |        /
	|/----------------|--------------|--------------|--------|-------/
    """
million = 1000000
TOKEN_COSTS = {
    "gpt-4o": {
		"input_tokens": 2.5 / million,
		"cache_read": 1.25 / million,
		"output_tokens": 10 / million,
	},
    "gpt-4o-mini": {
		"input_tokens": 0.15 / million,
		"cache_read": 0.075 / million,
		"output_tokens": 0.6 / million,
	},
	"gemini-1.5-flash": {
		"input_tokens": 0,
		"cache_read": 0,
		"output_tokens": 0,
	},
}