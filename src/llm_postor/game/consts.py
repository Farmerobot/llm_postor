NUM_MAX_PLAYERS = 10
NUM_SHORT_TASKS = 8
NUM_LONG_TASKS = 2
NUM_CHATS = 5
MIN_NAME = 2
IMPOSTOR_COOLDOWN = 1
STATE_FILE = "data/game_state.json"
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
    "openai/gpt-4o": {
		"input_tokens": 2.5 / million,
		"cache_read": 1.25 / million,
		"output_tokens": 10 / million,
	},
    "openai/gpt-4o-mini": {
		"input_tokens": 0.15 / million,
		"cache_read": 0.075 / million,
		"output_tokens": 0.6 / million,
	},
	"google/gemini-flash-1.5-exp": {
		"input_tokens": 0.075,
		"cache_read": 0,
		"output_tokens": 0.3,
	},
	"gryphe/mythomax-l2-13b": {
		"input_tokens": 0.9 / million,
		"cache_read": 0,
		"output_tokens": 0.9 / million,
	},
	"microsoft/wizardlm-2-8x22b": {
		"input_tokens": 0.5 / million,
		"cache_read": 0,
		"output_tokens": 0.5 / million,
	},
	"meta-llama/llama-3.1-8b-instruct": {
		"input_tokens": 0.05 / million,
		"cache_read": 0,
		"output_tokens": 0.05 / million,
	},
    "meta-llama/llama-3.1-70b-instruct": {
        "input_tokens": 0.35 / million,
        "cache_read": 0,
        "output_tokens": 0.4 / million,
	},
	"nousresearch/hermes-3-llama-3.1-405b": {
		"input_tokens": 1.79 / million,
		"cache_read": 0,
		"output_tokens": 2.49 / million,
	},
	"mistralai/mistral-nemo": {
		"input_tokens": 0.13 / million,
		"cache_read": 0,
		"output_tokens": 0.13 / million,
	},
}