from typing import List, Optional

from game.players.base_player import Player


class HumanPlayer(Player):

    def prompt_action(self, actions: List[str]) -> int:
        self.state.actions = actions
        
        action_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(actions)]
        )
        self.state.prompt = f"Your turn {self.name}: Choose an action\n{action_prompt}"
        self.state.prompt += "========================================"
        task_str = "\n".join([str(task) for task in self.tasks])
        self.state.prompt += f"Here are your tasks: \n{task_str}"
        self.state.prompt += "========================================"
        print(self.state.prompt)

        while True:
            try:
                choosen_action = int(input("Choose action (enter the number): "))
                if 0 <= choosen_action < len(actions):
                    self.state.response = str(choosen_action)
                    return choosen_action
                else:
                    print(f"Please enter a number between 0 and {len(actions) - 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")
            self.state.action_taken = "Invalid action"

    def prompt_discussion(self) -> str:
        history = self.history.get_history_str()
        messages = self.get_message_str()
        print(history)
        print(messages)
        print(f"{self.name} it's your turn to discuss")
        answer = input("")
        self.state.response = answer
        return answer

    def prompt_vote(self, voting_actions: List[str]) -> int:
        voting_prompt = "\n".join(
            [f"{i}: {action}" for i, action in enumerate(voting_actions)]
        )
        self.state.prompt = voting_prompt
        self.state.actions = voting_actions
        answer = input("Choose player to banish: ")
        if answer.isdigit():
            self.state.response = str(answer)
            return int(answer)
        else:
            return self.prompt_vote(voting_actions)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
