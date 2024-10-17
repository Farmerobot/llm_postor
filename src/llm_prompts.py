# LLM Prompts for various agents and actions

ADVENTURE_PLAN_TEMPLATE = """
You are a game agent with the following state:

History of observations:
{history}

Current tasks: 
{tasks}
ASCII map of the game:
{ASCII_MAP}

Available actions: {actions}

Based on this information, create a plan to accomplish the current task.
Your plan should be a step-by-step approach, considering your past observations.

Plan:
"""

ADVENTURE_ACTION_TEMPLATE = """
You are a game agent with the following state:

History of observations:
{history}

Current task: {task}

Available actions: {actions}

You have created the following plan:
{plan}

Based on your plan and the available actions, choose the best action to take next.
Your response should be exactly one of the available actions.

Chosen action:
"""

DISCUSSION_TEMPLATE = """
You are {player_name}, a player in an Among Us-like game. You are participating in the discussion phase.
You are {player_role}.
Game history and your observations:
{history}

Based on the game history and your observations, create discussion points to share with other players.
Be strategic about what information you reveal. If you're an impostor, you might want to lie or misdirect.
If you're a crewmate, share your observations but be aware that others might be lying.

Your discussion points:
"""

DISCUSSION_RESPONSE_TEMPLATE = """
You are {player_name}, a player in an Among Us-like game. You are participating in the discussion phase.
This is turn-based game where players take turns making actions and responding to each other.
There are no actions like venting or sabotaging in this game.
You are {player_role}.

Game history and your observations:
{history}

Recent statements from other players:
{statements}

Respond to these statements based on the game history, your observations, and what you know about the game.
Be strategic in your response. If you're an impostor, you might want to support or cast doubt on certain statements.
If you're a crewmate, you might want to corroborate or question statements based on your observations.
Respond should be short and to the point. You don't need to respond to every statement.
You don't need write your name in brackets, it's already included in the prompt.
Your response:
"""

VOTING_TEMPLATE = """
You are {player_name}, a player in an Among Us-like game. It's time to vote on who to eject from the game.
You are {player_role}.
Game history and your observations:
{history}
Discusssion messages:
{discussion}
Available voting actions:
{actions}
Based on the game history and your observations, choose the best action to take.
If you're an impostor, try to avoid suspicion and protect your team.
If you're a crewmate, try to identify the most suspicious player based on the available information.
Your response should be exactly one of the available actions.
Chosen action:
"""
