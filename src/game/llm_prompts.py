# LLM Prompts for various agents and actions. Absolutely no persusaion or manipulation involved.

GAME_CONTEXT = """
This is a text-based social deduction game where players explore a virtual house while trying to complete objectives. The game has two phases:
1. Action Phase: Players can move between rooms and perform actions
2. Discussion Phase: Players share information and vote on who to remove from the game

Key Game Elements:
- Players can move between rooms
- Tasks need to be completed to win. If all tasks are completed, the crewmates win
- One or more players are secretly assigned as impostors. Your role is either a crewmate or an impostor
- Impostors can eliminate crewmates, and crewmates can report dead bodies
- Crewmates and impostors can call emergency meetings to discuss and vote on who to eject from the game
- After each elimination, players must discuss and vote on who to eject from the game
- The game continues until tasks are completed or impostors eliminate enough crewmates to win

Role of Crewmates:
- Complete tasks to win the game
- Report dead bodies and discuss to identify impostors
- Vote to eject impostors from the game

Role of Impostors:
- Eliminate crewmates to win the game
- Blend in with crewmates to avoid being identified
- Vote to eject crewmates from the game

"""

ADVENTURE_PLAN_TEMPLATE = GAME_CONTEXT + """
You are {player_name} in a text-based social deduction game.
Role: {player_role}
Your current game state is:

Game Context:
{history}

Your Current Objectives:
{tasks}

Current Map Layout:
{ASCII_MAP}

Actions You Can Take:
{actions}

You are currently located in: {current_location}

Based on this information, what is your next objective? 
Provide a straightforward sequence of steps to achieve your current task. 
Focus on completing the objective.
The plan should not exceed 3-4 steps as it is a short plan for current situation.

Next steps:
"""

ADVENTURE_ACTION_TEMPLATE = GAME_CONTEXT + """
You are {player_name} in a text-based social deduction game.
Role: {player_role}
Your current game state is:

Your Planned Steps:
{plan}

Actions You Can Take:
{actions}

Select one action from the available options that best aligns with your next planned step.
Respond with exactly one action from the provided list. Avoid numbering or adding extra punctuation or information.

For example, if one of the available actions is:
<action>report dead body of [Wateusz, Warek]</action>
You should respond with:
report dead body of [Wateusz, Warek]

Notice that the response should match the available actions exactly.

Selected action:
"""

DISCUSSION_TEMPLATE = GAME_CONTEXT + """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Your Observations:
{history}

Recent Player Messages:
{statements}

If there are no messages share what you have observed during the game by creating simple and short bullet points. 
If there are messages, create informative and short discussion points to plan a discussion.
Your name is {player_name}. You are a {player_role}.

Your {player_role} observations to be shared with others:
"""

DISCUSSION_RESPONSE_TEMPLATE = GAME_CONTEXT + """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Recent Player Messages:
{statements}

Your discussion points:
{points}

Your name is {player_name}. You are a {player_role}.
Respond to the recent messages. Your mesasage should not exceed one sentence and should be informative and short.
Very short and concise responses are expected because time is important in fast discussions.


Your one sentence response as {player_role}:
"""

VOTING_TEMPLATE = GAME_CONTEXT + """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Game History:
{history}

Discussion Record:
{discussion}

Available Voting Options:
{actions}

Based solely on the information presented in the discussion and your direct observations, select one voting option from the available choices.
Respond with exactly one option from the provided list.

Your vote:
"""
