NUM_MAX_PLAYERS = 10
NUM_SHORT_TASKS = 8
NUM_LONG_TASKS = 2
NUM_CHATS = 5
IMPOSTOR_COOLDOWN = 1
STATE_FILE = "data/game_state.json"
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
	"google/gemini-flash-1.5": {
		"input_tokens": 0.075 / million,
		"cache_read": 0,
		"output_tokens": 0.3 / million,
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
	"microsoft/wizardlm-2-7b": {
		"input_tokens": 0.055 / million,
		"cache_read": 0,
		"output_tokens": 0.055 / million,
	},
	"qwen/qwen-2-7b-instruct": {
		"input_tokens": 0.054 / million,
		"cache_read": 0,
		"output_tokens": 0.054 / million,
	},
	"meta-llama/llama-3.1-8b-instruct": {
		"input_tokens": 0.05 / million,
		"cache_read": 0,
		"output_tokens": 0.05 / million,
	},
	"meta-llama/llama-3.2-1b-instruct": {
		"input_tokens": 0.01 / million,
		"cache_read": 0,
		"output_tokens": 0.02 / million,
	},
	"meta-llama/llama-3.2-3b-instruct": {
		"input_tokens": 0.03 / million,
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