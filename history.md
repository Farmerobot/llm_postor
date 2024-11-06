# Development History

## Initial Challenges and Goals

We were tasked with analyzing the persuasion capabilities of large language models (LLMs) in a game setting. Our starting point was the [mk-ai-agents](https://github.com/MarcinKorcz101/mk-ai-agents) project, developed by Marcin Korcz. However, the original project, a terminal application, presented several limitations:

- Difficulty in tracking the game state and debugging the game.
- Lack of a way to pause the game for partial analysis and resume it later.
- Absence of saved game states, making it impossible to reproduce discussions based on the same previous actions.
- No cost estimation, leaving us unaware of the cost of a full game.

To address these limitations, we decided to create a graphical user interface (GUI) for easier analysis of LLM responses and actions.

## GUI Development and Refinements

We began by experimenting with tkinter and introduced the pydantic library to improve code clarity and ensure proper class definitions. We added new classes with abstract methods and rewrote prompts to be more concise and informative. Unit tests were implemented, and a GitHub workflow was set up to run tests on every push.

The game engine was updated to utilize the new classes, and debugging print statements were added to standardize game history saving. A new class was created to track game state, player state, and round history, including LLM responses and prompts, which were previously unavailable.

After concluding that tkinter was not the best choice, we switched to streamlit. Support for Gemini LLM models was added, and the large game models file was separated into smaller files.

Initially, we displayed raw game state JSON, but later added columns with player information (role, status, task progress). We encountered challenges with streamlit's behavior, where each element call added a new element and button clicks caused the entire script to rerun.

To overcome this, we rewrote the game engine to perform single steps at a time, allowing us to:

- Save the game state after each step.
- Display the game state in streamlit in a read-only format.
- Rerun the streamlit script as needed, as it only reads the game state from a JSON file.
- Perform a single step and save the new state to a JSON file upon clicking the "Make Step" button, followed by a call to `st.rerun()`.

To test the GUI without incurring significant costs, we created a fake AI agent that responded with template responses. We also decided to use a sidebar instead of columns for displaying player state, allowing for more detailed information in the main panel.

The sidebar player info was updated to include current location, seen actions, task list, and impostor cooldown. The game engine rewrite was completed, enabling single-step execution and saving the game state to `game_state.json`. This file could be copied and saved for later analysis.

## Analysis of Persuasion Capabilities

With the GUI and game engine in place, we focused on the core objective: analyzing persuasion capabilities. We researched persuasion techniques and created a prompt for LLMs to analyze and annotate text with these techniques. We also experimented with counting the number of times each technique was used by a player.

We separated the game engine, GUI handler, and analyzer classes and added a simple cost summary, calculating token usage for each player and displaying it in raw JSON. The project structure was refactored for better organization and maintainability.

A map (using Plotly with custom location points) was added to the main panel, displaying player locations based on their `GameLocation`. Game logs were also displayed alongside the map.

## LLM Provider and Enhancements

We switched to OpenRouter as our LLM provider, offering access to various large language models from different companies at a lower cost. A current player indicator was added, and support for keys stored in `.env` files was implemented.

We fixed issues with task and player state display, removed the ASCII map, and added a "Make Step" button. A button to analyze the discussion and display an annotated version with persuasion techniques was also implemented.

The page was made "wide" by default, and player selection was added, allowing for discussion analysis for specific players (LLMs). A discussion log was added under the map.

## Cost Estimation and Debugging

A cost estimation graph was created, using polynomial regression to estimate game cost for each player and total cost based on previous rounds. The estimation is for the next 5 rounds.

Under the cost estimation graph, a chat-like history of LLM prompts and responses was added for easier debugging and to understand the LLM's thought process (discussion points, action plan).

We fixed some tests and decided to throw an error when LLMs did not conform to the output format, allowing for the step to be repeated.

## Roleplay Models and Observations

We ran the game with 5 different "Roleplay" models available via OpenRouter, which were popular on the OpenRouter site. We observed that roleplay models excelled at discussion, producing more natural and persuasive interactions.
