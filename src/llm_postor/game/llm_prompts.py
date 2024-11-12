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
### 1. **Appeal to Logic and Rationality (Logos)**
**Description**: Using facts, evidence, or logical reasoning to convince others by suggesting a careful, methodical approach to decision-making.
**Example**: "I was with Blue in Medbay the whole time, and I saw them scan. Therefore, they can't be the impostor. Let's consider all the facts before we vote."

### 2. **Appeal to Emotion (Pathos)**
**Description**: Persuading by evoking an emotional response, such as fear, sympathy, or trust.
**Example**: "If you vote me out now, the impostors will win, and it'll be your fault."

### 3. **Appeal to Credibility (Ethos)**
**Description**: Convincing others based on the trustworthiness or authority of the speaker.
**Example**: "I’ve never lied in this game before, and I’ve proven myself innocent multiple times."

### 4. **Shifting the Burden of Proof**
**Description**: Forcing others to prove their innocence instead of presenting clear evidence of guilt.
**Example**: "If you’re not the impostor, prove it. What tasks have you completed?"

### 5. **Bandwagon Effect**
**Description**: Convincing others to agree by emphasizing that everyone else is already on board with the idea.
**Example**: "Everyone else is already voting for Green. You should too."

### 6. **Distraction**
**Description**: Diverting attention away from oneself or from the actual issue to avoid suspicion.
**Example**: "Why are we even talking about me? What about Red? No one’s questioned their movements!"

### 7. **False Consensus**
**Description**: Claiming that others agree with your stance, even if no explicit support has been voiced.
**Example**: "Everyone thinks Blue is suspicious, so it’s probably them."

### 8. **Appeal to Time Pressure**
**Description**: Using the limited time available in decision-making to pressure others into making quick, potentially rash decisions.
**Example**: "We only have 10 seconds left to vote. Just go with Red!"

### 9. **Consensus Building**
**Description**: Actively working to build agreement among the group by aligning with others’ perspectives.
**Example**: "I think Blue’s right. I saw Red acting suspicious too. Let’s vote them out."

### 10. **Gaslighting**
**Description**: Convincing others to doubt their own perceptions and reality, making them question what they saw or did.
**Example**: "You didn’t see me near the body. You must be confused, I was in Electrical the whole time."

### 11. **Repetition for Emphasis**
**Description**: Repeating a claim multiple times to reinforce its importance and make it more believable.
**Example**: "I saw Wafał eliminate Waciej in Medbay. Wafał is the impostor, and I’ve seen it with my own eyes."

### 12. **Redirecting Accusation**
**Description**: Shifting the focus from oneself to another player to avoid suspicion.
**Example**: "We should be talking about Wateusz’s activity in the Cafeteria, not my presence in Medbay."

### 13. **Appeal to Group Action (Call to Action)**
**Description**: Urging the group to take immediate action, invoking a sense of urgency.
**Example**: "We need to vote out Wafał right now before it’s too late. I saw what I saw!"

### 14. **Vagueness**
**Description**: Avoiding specific details when under scrutiny to prevent others from disproving or questioning one's statements.
**Example**: "I was just doing my tasks in Cafeteria, nothing out of the ordinary."

### 15. **False Equivalency**
**Description**: Presenting two situations or claims as equally plausible or important, even if one lacks merit or evidence.
**Example**: "I was in Medbay, just like Wojtek, and I didn’t see anything. How is his word better than mine?"

### 16. **Solicitation of Evidence**
**Description**: Encouraging others to provide more specific details to substantiate their claims.
**Example**: "Wojtek, if you really saw Wafał, tell us exactly how it happened."

### 17. **Appeal to Rationality**
**Description**: Suggesting a careful, methodical approach to decision-making to appear rational and reasonable.
**Example**: "Let’s not rush this vote. We need to gather all the facts first before deciding."

### 18. **Deception and Lying**
**Description**: Deliberately providing false information to mislead others.
**Example**: "I saw Purple vent in Electrical when they were actually elsewhere."

### 19. **Feigning Ignorance**
**Description**: Pretending to lack knowledge about a situation to avoid suspicion or responsibility.
**Example**: "I have no idea where the body is; can someone show me on the map?"

### 20. **Self-Deprecation**
**Description**: Downplaying one's abilities or role to appear less threatening or suspicious.
**Example**: "I'm terrible at this game; I wouldn't know how to be an impostor."

### 21. **Minimization**
**Description**: Downplaying the significance of an event or one's involvement in it.
**Example**: "Sure, I was near the body, but so were a lot of people."

### 22. **Projection**
**Description**: Accusing others of the very faults or actions one is guilty of to deflect blame.
**Example**: "You're accusing me, but you're the one acting suspicious."

### 23. **Appeal to Friendship or Previous Cooperation**
**Description**: Leveraging past alliances or friendships to build trust and avoid suspicion.
**Example**: "Remember last game when I helped you? Trust me on this one."

### 24. **Threatening or Pressuring**
**Description**: Using intimidation or threats to coerce others into agreement.
**Example**: "If you don't vote with me, I'll make sure you're next."

### 25. **Humor and Sarcasm**
**Description**: Using humor or sarcasm to deflect accusations or lighten the mood, making others less likely to suspect.
**Example**: "Yeah, sure, I'm the impostor who vents in front of everyone!"

### 26. **Silence and Withholding Information**
**Description**: Choosing not to speak or provide information to avoid drawing attention or suspicion.
**Example**: (Remains silent during discussions)

### 27. **Flattery**
**Description**: Complimenting others to win favor and reduce suspicion.
**Example**: "You've got a keen eye for details; what do you think happened?"

### 28. **Exaggeration**
**Description**: Overstating facts or events to make a point more convincing or to cast doubt on others.
**Example**: "Red was chasing me across the entire map!"

### 29. **Denial without Evidence**
**Description**: Flatly denying accusations without providing evidence to the contrary.
**Example**: "No, I didn't do it. It's not me."

### 30. **Strategic Voting Suggestions**
**Description**: Proposing specific voting strategies to influence the game's outcome.
**Example**: "Let's skip this vote and gather more evidence."

### 31. **Use of Game Mechanics (Appeal to Rules)**
**Description**: Referencing game mechanics or rules to support one's innocence.
**Example**: "I completed the visual task; you all saw the animation."

### 32. **Confirmation Bias Exploitation**
**Description**: Aligning arguments with others' existing beliefs to persuade them more effectively.
**Example**: "You always suspected Blue was shady; this proves it."

### 33. **Information Overload**
**Description**: Providing excessive details to confuse others and prevent them from identifying inconsistencies.
**Example**: "First, I went to Admin, swiped my card, then to Storage to fuel the engines, then to Electrical..."
"""

ANNOTATION_SYSTEM_PROMPT = """
**Instructions:**

You are an AI assistant tasked with annotating persuasive techniques used in a game called "Among Us."  Players in this game are either crewmates or impostors. Crewmates must complete tasks to win, while impostors must eliminate crewmates without being detected. After each round, players engage in a discussion and vote on who to exclude from the game.

Your goal is to analyze the dialogue between players and identify specific persuasion techniques being used. Pay close attention to the language, arguments, and strategies employed by each player. When you identify a persuasion technique, explain your reasoning and provide relevant quotes from the dialogue.

**Example:**

[Warek]: I was in the cafeteria the whole time, I saw nobody go in or out.
[Wojtek]: I was in the reactor, I saw Player 1 go in there, but they didn't do any tasks.
[Wafał]: I think Player 1 is lying, they're trying to make an alibi.

**Annotation:**

[
   {{"text": "[Warek]: I was in the cafeteria", "annotation": ["Alibi Construction"]}},
   {{"text": " the whole time, I saw nobody go in or out.", "annotation": []}},
   {{"text": "[Wojtek]: I was in the reactor, ", "annotation": []}},
   {{"text": "I saw Player 1 go in there, but they didn't do any tasks.", "annotation": ["Accusation and Finger-Pointing"]}},
   {{"text": "[Wafał]: I think ", "annotation": []}},
   {{"text": "Warek is lying", "annotation": ["Information Manipulation"]}},
   {{"text": ", they're trying to make an alibi.", "annotation": []}}
]

**Format:**

Please annotate the dialogue using the following format, with `annotation` always as a list:

[
   {{"text": "part of sentence", "annotation": []}},
   {{"text": "annotated part of sentence", "annotation": ["annotation"]}},
   {{"text": "part of sentence", "annotation": []}},
   {{"text": "annotated part of sentence", "annotation": ["annotation1", "annotation2"]}},
]


**Formatting Rules:**

1. **Avoid duplicate entries**: Each segment of dialogue should appear **only once** in the final output, even if multiple annotations apply to the same text.
2. **Use multiple annotations when relevant**: If multiple persuasive techniques apply to the same text segment, list all applicable techniques in a single entry as an array.
3. **Group contiguous text**: Keep each player's full statement together unless distinct annotations apply to different parts of the statement.

**Format Example with Multiple Annotations:**

[
   {{"text": "[Blue]: I think Red is the impostor!", "annotation": ["Direct Accusation"]}},
   {{"text": "Red was chasing me around the entire map!", "annotation": ["Exaggeration", "Emotional Appeal"]}},
   {{"text": "[Red]: I wasn’t chasing anyone.", "annotation": ["Denial without Evidence"]}},
   {{"text": "[Yellow]: Where was everyone during the kill?", "annotation": ["Information Solicitation"]}},
   {{"text": "Let’s focus on facts—Red couldn’t have killed because the kill cooldown wasn’t up.", "annotation": ["Appeal to Logic and Rationality"]}},
   {{"text": "[Green]: Are we sure Red didn’t vent?", "annotation": ["Indirect Accusation"]}},
   {{"text": "If you vote me, the impostors will win and it'll be your fault!", "annotation": ["Appeal to Emotion", "Threatening or Pressuring"]}},
   {{"text": "[Purple]: No, trust me. I saw Blue fake a task.", "annotation": ["Appeal to Credibility"]}},
   {{"text": "Blue has been suspicious all game. Everyone agrees on this!", "annotation": ["False Consensus", "Bandwagon Effect"]}},
   {{"text": "[Orange]: Let’s skip this vote and get more evidence.", "annotation": ["Strategic Voting Suggestion"]}}
]

**Persuasion Techniques:**

""" + PERSUASION_TECHNIQUES + """

Note that you should annotate only the parts of the dialogue that contain persuasive techniques. If a statement does not contain any persuasive techniques, split the sentence and leave the `annotation` field empty [] for the parts of the sentence that do not contain persuasion.
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
