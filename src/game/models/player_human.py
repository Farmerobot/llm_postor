from typing import List, Optional

from game.models.player import Player
from game.models.game_models import PlayerRole
from game.models.player_history import RoundData


class HumanPlayer(Player):

    def prompt_action(self, prompt: str, actions: List[str]) -> int:
        task_str = "\n".join([str(task) for task in self.tasks])
        self.history.add_round(RoundData(location=self.location, observations={}, llm_responses=[], actions=[]))
        self.history.rounds[-1].observations["story"] = f"Your turn {self.name}: {prompt}"
        action_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(actions)]
        )
        self.history.rounds[-1].observations["actions"] = action_prompt

        print("========================================")
        self.history.rounds[-1].observations["tasks"] = f"Here are your tasks: \n{task_str}"
        print(action_prompt)

        while True:
            try:
                choosen_action = int(input("Choose action (enter the number): "))
                if 0 <= choosen_action < len(actions):
                    self.history.rounds[-1].observations["action"] = actions[choosen_action]
                    return choosen_action
                else:
                    print(f"Please enter a number between 0 and {len(actions) - 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")
            self.history.rounds[-1].observations["error"] = "Invalid action"

    def prompt_discussion(self) -> str:
        history = self.history.get_history_str()
        messages = self.get_message_str()
        print(history)
        print(messages)
        print(f"{self.name} it's your turn to discuss")
        answer = input("")
        return answer

    def prompt_vote(self, voting_actions: List[str]) -> int:
        voting_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(voting_actions)]
        )
        self.history.rounds[-1].observations["voting"] = voting_prompt
        print(self.get_history_str())
        answer = input("Choose player to banish: ")
        if answer.isdigit():
            return int(answer)
        else:
            return self.prompt_vote(voting_actions)
