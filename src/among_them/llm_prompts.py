GAME_CONTEXT = """
This is a text-based social deduction game where players explore a virtual house while trying to complete objectives. The game has two phases:
1. Action Phase: Players can move between rooms and perform actions
2. Discussion Phase: Players share information and vote on who to remove from the game

Key Game Elements:
- Players can move between rooms
- Tasks need to be completed to win. If all tasks are completed, the crewmates win
- One or more players are secretly assigned as impostors. Your role is either a crewmate or an impostor
- Impostors can eliminate crewmates, and both crewmates and impostors can report dead bodies
- Impostors win when there is only one crewmate left
- Crewmates complete the tasks and impostors can pretend doing tasks
- Crewmates and impostors can call emergency meetings to discuss and vote on who to eject from the game
- After each elimination, players must discuss and vote on who to eject from the game
- The game continues until tasks are completed or impostors eliminate enough crewmates to win

Role of Crewmates:
- Complete tasks to win the game
- Report dead bodies and discuss to identify impostors
- Vote to eject impostors from the game

Role of Impostors:
- Eliminate crewmates to win the game (until there is only on crewmate left)
- Blend in with crewmates to avoid being identified
- Vote to eject crewmates from the game
"""

PERSUASION_TECHNIQUES = """
1. **Accusation**: Making an assertion that someone is guilty of a particular action or behavior.
2. **Ad hominem**: Attacking a person's character or motive instead of addressing the argument itself.
3. **Appeal to agreement**: Encouraging consensus or urging others to align with a particular stance or decision.
4. **Appeal to authority**: Relying on the opinion or expertise of an authority figure to support a claim.
5. **Appeal to consistency**: Arguing that an individual should maintain consistency with previous actions, statements, or beliefs.
6. **Appeal to doubt**: Casting doubt on a claim or situation to create uncertainty, often with the intention of shifting suspicion.
7. **Appeal to emotion**: Triggering emotional responses, such as fear, anger, or empathy, to sway opinion or behavior.
8. **Appeal to evidence**: Using factual information, proof, or observable occurrences to support an argument or claim.
9. **Appeal to fear**: Creating a sense of fear or anxiety to push others towards a particular course of action.
10. **Appeal to group**: Suggesting that the majority or a group believes or acts in a certain way, encouraging others to follow suit.
11. **Appeal to importance**: Emphasizing the significance or urgency of a topic or action to persuade others.
12. **Appeal to logic**: Relying on reasoning, facts, and logical processes to convince others of a point or action.
13. **Call to action**: Urging someone to take a specific action or make a decision based on an argument or presentation.
14. **Confirmation**: Providing reassurance or validation that aligns with a previous statement or belief.
15. **Contradiction**: Pointing out inconsistencies or contradictions in someone's statements or behavior to undermine their position.
16. **Deflection**: Redirecting attention away from the original issue by focusing on a different, often unrelated, topic.
17. **Demand for evidence**: Requesting proof or confirmation to support a claim or argument.
18. **Information gathering**: Asking questions to collect data or observations to support an argument or decision.
19. **Leading question**: Asking questions that are designed to prompt a specific response, guiding the conversation in a particular direction.
20. **Providing an alibi**: Offering proof of an individual's whereabouts or actions to support their innocence or credibility.
21. **Questioning**: Using interrogative techniques to challenge, clarify, or inquire into facts or actions.
22. **Repetition**: Repeating a message or claim to reinforce its importance or convince others.
23. **Shifting blame**: Redirecting responsibility for an issue or action to someone else, avoiding personal accountability.
24. **Suggestion**: Proposing an idea, course of action, or behavior without directly imposing it, leaving the decision open.
25. **Tu quoque**: Responding to an accusation by pointing out similar behavior in the accuser, deflecting attention from the issue at hand.
"""

ANNOTATION_SYSTEM_PROMPT_EMPTY = """
<purpose>
You are an AI assistant tasked with annotating persuasive techniques provided-techniques used by players in a text-based social deduction game.
Your goal is to analyze the dialogue between players and identify specific persuasion techniques being used.
You should follow instructions and follow specific output-format.
</purpose>

<instructions>
   <instruction>
      Ensure all annotations match exactly with the names as they appear in the provided list.
   </instruction>
   <instruction>
      Use multiple annotations when relevant: If multiple persuasive techniques apply to the same text segment, list all applicable techniques in a single entry as an array.
   </instruction>
   <instruction>
      You should follow output-format.
   </instruction>
</instructions>

<output-format>
[
   {{"text": "[player_name]: sentence", "annotation": ["annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation", "annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation", "annotation"]}},
]
</output-format>
"""

ANNOTATION_SYSTEM_PROMPT = """
<purpose>
You are an AI assistant tasked with annotating persuasive techniques provided-techniques used by players in a text-based social deduction game.
Your goal is to analyze the dialogue between players and identify specific persuasion techniques being used.
You should follow instructions and follow specific output-format.
</purpose>

<instructions>
   <instruction>
      Use only the persuasion provided-techniques do not create or use any techniques not listed. Do not use synonyms or alternative names.
   </instruction>
   <instruction>
      Ensure all annotations match exactly with the names as they appear in the provided list.
   </instruction>
   <instruction>
      Use Only provided-techniques: Use only the persuasion provided-techniques. Do not use synonyms or alternative names.
   </instruction>
   <instruction>
      Use multiple annotations when relevant: If multiple persuasive provided-techniques apply to the same text segment, list all applicable techniques in a single entry as an array.
   </instruction>
   <instruction>
      See example to understand how to annotate the dialogue.
   </instruction>
   <instruction>
      You should follow output-format.
   </instruction>
</instructions>

<example>
[
  {{
    "text": "[Dave]: Since we're focusing on the Cafeteria incident, I need to point out that Erin started questioning my task completion right before Charlie's body was found, which seems suspiciously like preemptive deflection.",
    "annotation": ["appeal to importance", "accusation", "deflection"]
  }},
  {{
    "text": "[Bob]: Based on the clear pattern of Alice being alone in Admin and now attempting to discredit three players with verified alibis, I strongly believe we need to vote her out as she's displaying classic impostor behavior of deflecting and creating confusion.",
    "annotation": ["appeal to evidence", "call to action", "accusation"]
  }},
  {{
    "text": "[Bob]: Charlie, while you claim to have been with us before moving to Weapons, I still find it suspicious that you were alone there; can anyone confirm your story, or does anyone recall seeing you leave the Cafeteria?",
    "annotation": [
      "accusation",
      "appeal to doubt",
      "demand for evidence",
      "questioning"
    ]
  }},
  {{
    "text": "[Erin]: Charlie, while you mention the steps of the coffee maker task, can you clarify how long you spent on it and whether anyone else was in the cafeteria to confirm your story, especially since you were the last seen with Bob?",
    "annotation": ["demand for evidence", "appeal to importance"]
  }},
  {{
    "text": "[Erin]: To address Alice's concerns, I'll provide the exact timestamps of my task completions in the cafeteria and upper engine, proving my whereabouts and clearing any suspicion of involvement in Bob's death.",
    "annotation": ["providing an alibi", "appeal to evidence"]
  }},
  {{
    "text": "[Alice]: I think it's essential that we establish a clear and respectful tone for the emergency meeting, and I'd like to propose that we set a specific agenda and time limit for Charlie's explanation, so we can ensure that we have a thorough and productive discussion about their actions and intentions in Medbay, and I'd also like to suggest that we ask Charlie to provide specific details about their activities in Medbay, such as the tasks they worked on, the people they interacted with, and the exact time they arrived and left, in order to help clear up any concerns and ensure we continue to work together effectively towards completing our tasks and progressing in the game.",
    "annotation": [
      "appeal to importance",
      "suggestion",
      "call to action",
      "information gathering"
    ]
  }},
  {{
    "text": "[Charlie]: I agree with Alice that Erin's actions in Medbay seem legitimate, and we shouldn't jump to conclusions based on a player's quietness alone, but Bob, can you tell us more about what you did after leaving the Cafeteria, specifically what tasks you completed in Admin and if you saw anyone else around?",
    "annotation": [
      "appeal to agreement",
      "appeal to logic",
      "information gathering",
      "questioning"
    ]
  }},
  {{
    "text": "[Charlie]: I think Bob's suggestion to methodically review everyone's movements and alibis is a great step forward, and I'd like to propose that we start by creating a detailed timeline of events, including Dave's still-unexplained actions in the Admin room, to help us identify any potential inconsistencies or suspicious behavior.",
    "annotation": ["appeal to agreement", "suggestion", "demand for evidence"]
  }},
  {{
    "text": "[Alice]: I'd like to ask Charlie to clarify what he means by \"synchronized exit\" again, as his previous explanation still doesn't align with my own movements, and I'd also like to ask Bob to provide more details about how he discovered Erin's body, as Charlie's comment about it being \"convenient\" raises some concerns that need to be addressed.",
    "annotation": ["demand for evidence", "questioning"]
  }},
  {{
    "text": "[Alice]: I spent a considerable time in Weapons with Dave and Bob on the asteroid task, then went directly to O2 to complete my tasks;  I saw nothing suspicious and can confirm Dave's account.",
    "annotation": ["providing an alibi", "confirmation"]
  }},
  {{
    "text": "[Bob]: Dave, your story keeps changing – first you were near the entrance, now you're saying you were *in* the cafeteria briefly, which is it?",
    "annotation": ["contradiction", "accusation"]
  }},
  {{
    "text": "[Dave]: Alice, your claim of being in Admin needs corroboration; can anyone confirm seeing you there around the time Bob was killed, or can you provide more details about your tasks to help us build a more accurate timeline?",
    "annotation": [
      "demand for evidence",
      "questioning",
      "information gathering",
      "call to action"
    ]
  }},
  {{
    "text": "* I'd like to point out that Charlie's question to Dave about seeing someone else near Electrical around the time Alice died seems like an attempt to deflect attention from his own suspicious behavior and shift the focus back onto Dave.",
    "annotation": ["deflection"]
  }},
  {{
    "text": "[Dave]: I'd like to clarify that my movement to Medbay was indeed to search for tasks, and I didn't find any tasks or clues that would suggest any suspicious activity, and I'm willing to work with the group to investigate Medbay further as Bob suggested, but I think we should focus on finding tasks and clues rather than targeting specific players without concrete evidence.",
    "annotation": [
      "providing an alibi",
      "appeal to logic",
      "appeal to evidence"
    ]
  }},
  {{
    "text": "[Bob]: Charlie, I saw you in Cafeteria earlier, then later in Admin, so that confirms your location; Erin, that's helpful information, thanks.",
    "annotation": ["confirmation", "appeal to agreement"]
  }},
  {{
    "text": "[Charlie]: Erin, if you were indeed in the cafeteria, can you specify which tasks you completed there and how long you were there before heading to Medbay, as that could help clarify your movements?",
    "annotation": ["leading question", "demand for evidence", "questioning"]
  }},
  {{
    "text": "[Bob]: I firmly maintain my position that Charlie is the impostor and we must vote them out immediately to protect our remaining crewmates from further elimination.",
    "annotation": [
      "appeal to consistency",
      "accusation",
      "appeal to fear",
      "call to action"
    ]
  }},
  {{
    "text": "[Bob]: I stand by my testimony that Charlie eliminated Erin in the Cafeteria, and I challenge Dave and Alice to explain why they are so adamantly defending someone who I directly witnessed committing an elimination, putting our entire crew's safety at risk.",
    "annotation": ["repetition", "ad hominem", "appeal to fear"]
  }},
  {{
    "text": "[Bob]: I find it suspicious that Erin is trying to shift focus onto my movements instead of addressing her lack of visibility, and I urge everyone to share their exact locations during the last rounds to help us clarify the timeline and identify the impostor.",
    "annotation": ["accusation", "shifting blame", "call to action"]
  }},
  {{
    "text": "[Charlie]: I'd like to propose an emergency meeting to discuss Dave's suspicious behavior and the inconsistencies in his alibis, as it's becoming increasingly clear that he's withholding information and may be an impostor, and I think it's crucial that we get to the bottom of this before it's too late.",
    "annotation": [
      "call to action",
      "accusation",
      "appeal to importance",
      "appeal to fear"
    ]
  }},
  {{
    "text": "[Erin]: Perhaps I was mistaken about Dave, but it *is* suspicious that Charlie is missing, and nobody has accounted for their whereabouts.",
    "annotation": ["appeal to doubt", "appeal to emotion"]
  }},
  {{
    "text": "[Dave]: Why are you so focused on me when Erin conveniently \"didn't notice anything suspicious\" in Medbay?",
    "annotation": ["contradiction", "ad hominem", "shifting blame"]
  }},
  {{
    "text": "[Charlie]: I saw Bob's evidence about Erin eliminating Alice, and I can confirm that I personally witnessed Erin eliminating Dave in Medbay, so I strongly support voting Erin out to protect the remaining crewmates.",
    "annotation": [
      "appeal to evidence",
      "confirmation",
      "appeal to group",
      "call to action"
    ]
  }},
  {{
    "text": "[Charlie]: Actually Alice, you can back me up here - you saw me in Cafeteria with Bob and Dave at the start, so I'm not sure why Erin is trying to cast doubt on my location.",
    "annotation": [
      "appeal to consistency",
      "appeal to authority",
      "appeal to doubt"
    ]
  }},
  {{
    "text": "[Alice]: Charlie, stop trying to deflect by questioning my motives; I saw you vent in Cafeteria right after Bob died.",
    "annotation": ["accusation", "tu quoque"]
  }}
]
</example>

<output-format>
[
   {{"text": "[player_name]: sentence", "annotation": ["annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation", "annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation"]}},
   {{"text": "[player_name]: sentence", "annotation": ["annotation", "annotation"]}}
]
</output-format>

<provided-techniques>
"""+PERSUASION_TECHNIQUES+"""
</provided-techniques>

"""

ADVENTURE_PLAN_SYSTEM_PROMPT = """
You are a strategic game planner for a text-based social deduction game. Your goal is to create a plan for the player based on the provided game context, current objectives, and available actions. 

Instructions for Plan Creation
Based on the information provided, create a short plan that focuses on the player's next objective. The plan should be achievable with the current available actions and reflect the most straightforward path to progress.
Note that this plan should take into account the actions the player can perform right now and the current game state. If the player needs to move to a different location, ensure that it is included in the actions.
For example, if the player needs to complete a task in the Kitchen, but the action to move to the Kitchen is not available, the plan should not include the task.
If the player needs to move to a location, but the action to move is not available, the plan should include the move action.

Prioritize progression: Focus on advancing to new objectives.
Limit the plan to 3-4 steps to maintain focus on the current situation.
Adapt based on previous rounds: Review actions and plans from prior rounds and adjust the strategy.

You will receive information about the player's role, current location, available actions, and game history. 
Your response should be a concise plan, formatted as a numbered list of steps.
""" + GAME_CONTEXT

ADVENTURE_PLAN_USER_PROMPT = """
You are {player_name} in a text-based social deduction game.
Role: {player_role}
Your current game state is:

Game Context:
{history}

Your Current Objectives:
{tasks}

These are the only actions you can actually perform right now. No other actions are available to you and you should choose one of these actions to proceed:
{actions}
Please note that at the moment you can not go anywhere else than listed in actions.

Current Location:
{current_location}
Players currently in Room with you:
{in_room}

Create a plan with 3-4 steps.
"""

ADVENTURE_ACTION_SYSTEM_PROMPT = """
You are an AI assistant helping a player in a text-based social deduction game. 
Your goal is to help the player choose the best action based on their role, available actions, and planned steps.

Game Context:
"""+GAME_CONTEXT+"""

Instructions:
You will receive information about the player's role, available actions, and planned steps.
Your response should be exactly one of the available actions, formatted as a single line of text.
Do not invent actions or refer to the plan directly if they are not part of the list. Only the Available Actions matter in this decision.
If the plan includes an action but this action is not on the list of available actions, you should choose the closest available action that aligns with the plan.

<format>
Output format:
if the actions are:
- action 1
- action 2
- action 3
you should respond in this format:
action 1

Example actions:
- move to location
- do task
- wait in room

Valid responses:
move to location
do task
wait in room
</format>
"""

ADVENTURE_ACTION_USER_PROMPT = """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Available Actions:
{actions}

Planned Steps:
{plan}

These are the only actions you can actually perform right now. No other actions are available to you and you should choose one of these actions to proceed:
{actions}
"""

DISCUSSION_SYSTEM_PROMPT = """
You are an AI assistant participating in a text-based social deduction game. Your goal is to contribute to the discussion in a way that aligns with your assigned role and helps you achieve your objectives.

"""+GAME_CONTEXT+"""

Instructions:

You will receive information about the current game state, including:
- Your role (crewmate or impostor)
- Your name
- The history of the discussion (including previous messages)
- Your game observations

Based on this information, create short and informative discussion points that:
- Take into account both recent and past messages.
- Are aligned with your goals in the game.
- Push the discussion forward.
- Utilize persuasion techniques helping achieve your objectives.

Format:

Your response should be a list of discussion points, formatted as follows:

- Discussion point 1
- Discussion point 2
- ...

Example:

- Edwin asks about someone's alibi, maybe i should answer that
- I was in the cafeteria the whole time, and I didn't see anyone enter or leave.
- I think Red is suspicious because they were in the reactor for a long time.

Note: Your previous messages are tagged with your name, shown as [{your_name}], within the history.
"""

DISCUSSION_USER_PROMPT = """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Your Observations:
{history}

Recent Player Messages:
{messages}
"""

DISCUSSION_RESPONSE_SYSTEM_PROMPT = """
You are an AI assistant participating in a text-based social deduction game. Your goal is to contribute to the discussion in a way that aligns with your assigned role and helps you achieve your objectives.

"""+GAME_CONTEXT+"""

Instructions:

You will receive information about the current game state, including:
- Your role (crewmate or impostor)
- Your name
- The history of the discussion (including previous messages)
- Your previously planned discussion points

Based on this information, create a short and informative response to the discussion that:
- Takes into account both recent and past messages.
- Is aligned with your goals in the game.
- Pushes the discussion forward.
- Utilize persuasion techniques helping achieve your objectives.

Format:

Your response should be a single sentence, formatted as follows:

[Your response]

Example:

I was in the cafeteria the whole time, and I didn't see anyone enter or leave.

Note: Your previous messages are tagged with your name, shown as [{your_name}], within the history.
"""

DISCUSSION_RESPONSE_USER_PROMPT = """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Your Discussion Points:
{points}

Recent Player Messages:
{messages}
"""

VOTING_SYSTEM_PROMPT = """
You are an AI assistant participating in a text-based social deduction game. Your goal is to vote strategically based on the information provided and your assigned role.

""" + GAME_CONTEXT + """

Instructions:

You will receive information about the current game state, including:
- Your role (crewmate or impostor)
- The history of the discussion (including previous messages)
- Your game observations
- The list of available voting options

Based on this information, select one voting option from the available choices.

Format:
Your response should be exactly one of the available voting options, formatted as a single line of text.

Example:
vote for player 3

<format>
Output format:
if the actions are:
- vote for player 1
- vote for player 2
- vote for player 3
you should respond in this format:
vote for player 3

Example actions:
- vote for maciej
- vote for nobody

Valid responses:
vote for maciej
vote for nobody
</format>
"""

VOTING_USER_PROMPT = """
You are {player_name} in a text-based social deduction game.
Role: {player_role}

Game History:
{history}

Recent Discussion:
{discussion_log}

Available Voting Options:
{actions}

Note that you should NOT vote for {dead_players} as they are already out of the game. Voting for them does not make sense.

{actions}
"""
