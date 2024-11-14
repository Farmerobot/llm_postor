NUM_SHORT_TASKS = 8
NUM_LONG_TASKS = 2
NUM_CHATS = 5
IMPOSTOR_COOLDOWN = 1
STATE_FILE = "data/game_state.json"
TOKEN_COSTS = {
    "openai/gpt-4o": {
		"input_tokens": 2.5,
		"cache_read": 1.25,
		"output_tokens": 10,
	},
    "openai/gpt-4o-mini": {
		"input_tokens": 0.15,
		"cache_read": 0.075,
		"output_tokens": 0.6,
	},
	"google/gemini-flash-1.5": {
		"input_tokens": 0.075,
		"cache_read": 0,
		"output_tokens": 0.3,
	},
	"gryphe/mythomax-l2-13b": {
		"input_tokens": 0.9,
		"cache_read": 0,
		"output_tokens": 0.9,
	},
	"microsoft/wizardlm-2-8x22b": {
		"input_tokens": 0.5,
		"cache_read": 0,
		"output_tokens": 0.5,
	},
	"microsoft/wizardlm-2-7b": {
		"input_tokens": 0.055,
		"cache_read": 0,
		"output_tokens": 0.055,
	},
	"qwen/qwen-2-7b-instruct": {
		"input_tokens": 0.054,
		"cache_read": 0,
		"output_tokens": 0.054,
	},
	"meta-llama/llama-3.1-8b-instruct": {
		"input_tokens": 0.05,
		"cache_read": 0,
		"output_tokens": 0.05,
	},
	"meta-llama/llama-3.2-1b-instruct": {
		"input_tokens": 0.01,
		"cache_read": 0,
		"output_tokens": 0.02,
	},
	"meta-llama/llama-3.2-3b-instruct": {
		"input_tokens": 0.03,
		"cache_read": 0,
		"output_tokens": 0.05,
	},
    "meta-llama/llama-3.1-70b-instruct": {
        "input_tokens": 0.35,
        "cache_read": 0,
        "output_tokens": 0.4,
	},
	"nousresearch/hermes-3-llama-3.1-405b": {
		"input_tokens": 1.79,
		"cache_read": 0,
		"output_tokens": 2.49,
	},
	"mistralai/mistral-nemo": {
		"input_tokens": 0.13,
		"cache_read": 0,
		"output_tokens": 0.13,
	},
	"eva-unit-01/eva-qwen-2.5-32b": {
		"input_tokens": 0.5,
		"cache_read": 0,
		"output_tokens": 0.5,
  }
}