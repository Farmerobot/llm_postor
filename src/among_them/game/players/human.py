from typing import List

from among_them.game.players.base_player import Player


class HumanPlayer(Player):
    def prompt_action(self, actions: List[str]) -> int:
        self.state.actions = actions

        action_prompt = "\n".join([
            f"{i}: {action}" for i, action in enumerate(actions)
        ])
        task_str = "\n".join([str(task) for task in self.state.tasks])
        self.state.prompts = []
        self.state.prompts.append(f"Here are your tasks: \n{task_str}")
        self.state.prompts.append("========================================")
        self.state.prompts.append(
            f"Your turn {self.name}: Choose an action\n{action_prompt}"
        )
        self.state.prompts.append("========================================")
        print("\n".join(self.state.prompts))

        while True:
            try:
                chosen_action = int(input("Choose action (enter the number): "))
                if 0 <= chosen_action < len(actions):
                    self.state.response = str(chosen_action)
                    return chosen_action
                else:
                    print(f"Please enter a number between 0 and {len(actions) - 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")
            self.state.action_result = "Invalid action"

    def prompt_discussion(self) -> str:
        history = self.history.get_history_str()
        messages = "\n".join(self.get_chat_messages())
        print(history)
        print(messages)
        print(f"=============/n{self.name} it's your turn to discuss:\n=============")
        answer = input("")
        self.state.response = answer
        return answer

    def prompt_vote(self, voting_actions: List[str], dead_players: List[str]) -> int:
        voting_prompt = "\n".join([
            f"{i}: {action}" for i, action in enumerate(voting_actions)
        ])
        self.state.prompts = ["========================================"]
        self.state.prompts += [voting_prompt]
        self.state.actions = voting_actions
        print("\n".join(self.state.prompts))
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
