from game.game_state import GameState
from game.models.game_models import (
    HUMAN_READABLE_LOCATIONS,
    GamePhase,
    PlayerState,
    GameLocation,
    PlayerRole,
    ShortTask,
    DOORS,
)
from game.models.player import Player
from game.models.player_human import HumanPlayer
from game.models.game_models import GameAction, GameActionType
from game.utils import get_random_tasks
from typing import Any, List, Callable, Optional
import random
from game import consts as game_consts
from collections import OrderedDict, Counter

from game.models.player_history import RoundData
from pydantic import BaseModel, Field, ConfigDict


class GameEngine(BaseModel):
    state: GameState = Field(default_factory=GameState)
    nobody: HumanPlayer = Field(default_factory=lambda: HumanPlayer(name="Nobody"))
    save_playthrough: str = ""
    DEBUG: bool = Field(default=False)
    gui: Optional[Any] = None

    def load_players(self, players: List[Player], impostor_count: int = 1) -> None:
        if len(players) < 3:
            raise ValueError("Minimum number of players is 3.")

        if impostor_count >= len(players) or impostor_count <= 0:
            raise ValueError("Invalid number of impostors")

        for player in players:
            self.state.add_player(player)

        # Count existing impostors
        existing_impostors = sum(
            1 for player in self.state.players if player.role == PlayerRole.IMPOSTOR
        )

        # Assign impostors randomly, only if needed
        impostors_to_assign = impostor_count - existing_impostors
        while impostors_to_assign > 0:
            available_players = [
                p for p in self.state.players if p.role != PlayerRole.IMPOSTOR
            ]
            if not available_players:
                break  # No more players to assign as impostors
            chosen_player = random.choice(available_players)
            chosen_player.role = PlayerRole.IMPOSTOR
            impostors_to_assign -= 1

        # Check for imbalanced team sizes AFTER role assignment
        crewmates_count = len(self.state.players) - impostor_count
        if impostor_count >= crewmates_count:
            raise ValueError(
                "Number of impostors cannot be greater than or equal to the number of crewmates."
            )

    def init_game(self) -> None:
        self.state.set_stage(GamePhase.ACTION_PHASE)

    def main_game_loop(self, freeze_stage: Optional[GamePhase] = None) -> None:
        """
        Main game loop that controls the flow of the game.

        :param freeze_stage: If set, the game will stay in this stage (used for testing).
        """
        check_game_over = self.set_game_stage(freeze_stage)

        print("Game started!")
        while not check_game_over():
            print(f"Game stage: {self.state.game_stage}")

            chosen_actions = self.get_player_actions()
            someone_reported = self.update_game_state(chosen_actions)

            if someone_reported and freeze_stage is None:
                self.discussion_loop()
                self.go_to_voting()

        # END OF GAME
        if freeze_stage is None:
            print("Game Over!")
            self.end_game()

    def set_game_stage(self, freeze_stage: Optional[GamePhase]) -> Callable[[], bool]:
        """Set the game stage and return the appropriate game over check function."""
        if freeze_stage:
            self.state.game_stage = freeze_stage
            return self.check_game_over_action_crewmate
        return self.check_game_over

    def get_player_actions(self) -> list[GameAction]:
        """Get actions from all alive players."""
        choosen_actions: list[GameAction] = []
        for player in self.state.players:
            if player.state.life == PlayerState.ALIVE:
                possible_actions = self.get_actions(player)
                possible_actions_str = [action.text for action in possible_actions]
                if self.DEBUG:
                    print(f"Player {player} actions: {possible_actions_str}")
                action_int = player.prompt_action(possible_actions_str)
                choosen_actions.append(possible_actions[action_int])
                if self.DEBUG:
                    print(f"Player {player} choosen action: {choosen_actions[-1]}")
        return choosen_actions

    def update_game_state(self, chosen_actions: list[GameAction]) -> bool:
        """
        Update game state based on actions
        actions are sorted by action type in way that actions with higher priority are first
        ex: REPORT > KILL > DO_ACTION > MOVE > WAIT
        Players can see actions of other players in the same room
        """
        chosen_actions.sort(key=lambda x: x.type, reverse=True)
        someone_reported = False
        for action in chosen_actions:
            self.state.playthrough.append(f"[{action.source}]: {action}")
            if action.source.state.life != PlayerState.DEAD:
                action.source.kill_cooldown = max(0, action.source.kill_cooldown - 1)
                if action.type == GameActionType.REPORT:
                    self.broadcast_history(
                        "report", f"{action.source} reported a dead body"
                    )
                    reported_players = self.state.get_dead_players_in_location(
                        action.source.location
                    )
                    self.broadcast_history(
                        "dead_players",
                        f"Dead players found: {', '.join(reported_players)}",
                    )
                    someone_reported = True  # in case of report; go to discussion
                if action.type == GameActionType.KILL and isinstance(
                    action.target, Player
                ):
                    action.target.state.action_result = (
                        f"You were eliminated by {action.source}"
                    )

                action.source.state.action_result = action.do_action()

                # update stories of seen actions and players in room
                for player in self.state.players:
                    if player.state != PlayerState.DEAD and player != action.source:
                        if (
                            action.location == player.location
                            or action.location == player.history.rounds[-1].location
                        ):
                            playthrough_text = f"Player {player} saw action {action.get_spectator_story()} when {player} were in {HUMAN_READABLE_LOCATIONS[action.location]}"
                            self.state.playthrough.append(playthrough_text)
                            if self.DEBUG:
                                print(playthrough_text)
                            player.state.seen_actions.append(
                                f"you saw {action.get_spectator_story()} when you were in {HUMAN_READABLE_LOCATIONS[action.location]}"
                            )

        # update players in room
        for player in self.state.players:
            players_in_room = [
                other_player
                for other_player in self.state.players
                if player.state.location == other_player.state.location
                and player != other_player
                and other_player.state == PlayerState.ALIVE
            ]

            playthrough_text = f"Player {player} is in {HUMAN_READABLE_LOCATIONS[player.location]} with {players_in_room}"
            self.state.playthrough.append(playthrough_text)
            if self.DEBUG:
                print(playthrough_text)
            if players_in_room:
                player.state.player_in_room = f"Players in room with you: {', '.join([str(player) for player in players_in_room])}"
            else:
                player.state.player_in_room = "You are alone in the room"

            # update player history
            player.log_state_new_round()
        return someone_reported

    def get_actions(self, player: Player) -> list[GameAction]:
        actions = []

        # actions for WAIT
        actions.append(GameAction(GameActionType.WAIT, player))

        # action for REPORT
        dead_players_in_room = self.state.get_dead_players_in_location(player.location)
        if dead_players_in_room:
            actions.append(
                GameAction(GameActionType.REPORT, player, dead_players_in_room)
            )

        # actions for MOVE
        for location in DOORS[player.location]:
            actions.append(GameAction(GameActionType.MOVE, player, location))

        # actions for tasks DO_ACTION
        for task in player.state.tasks:
            if task.location == player.location and not task.completed:
                actions.append(GameAction(GameActionType.DO_ACTION, player, task))

        # actions for impostors KILL
        if player.is_impostor and player.kill_cooldown == 0:
            targets = self.state.get_player_targets(player)
            for target in targets:
                actions.append(GameAction(GameActionType.KILL, player, target))

        return actions

    def discussion_loop(self) -> None:
        self.state.set_stage(GamePhase.DISCUSS)
        for player in self.state.players:
            player.state.prompt = (
                "Discussion phase has started. You can discuss and vote who to banish"
            )

        discussion_log: list[str] = []
        for round in range(game_consts.NUM_CHATS):
            for player in self.state.players:
                if player.state == PlayerState.ALIVE:
                    player.state.observations.append(
                        f"Discussion: [System]: You have {game_consts.NUM_CHATS - round} rounds left to discuss, then you will vote"
                    )
                    answer: str = player.prompt_discussion()
                    answer_str = f"Discussion: [{player}]: {answer}"
                    discussion_log.append(answer_str)
                    self.broadcast_message(answer_str)
            self.state.playthrough.append(f"Discussion log:")
            self.state.playthrough.append("\n".join(discussion_log))
            if self.DEBUG:
                print("Discussion log:")
                print("\n".join(discussion_log))

    def go_to_voting(self) -> None:
        dead_players = [
            player for player in self.state.players if player.state == PlayerState.DEAD
        ]
        votes = {}
        for player in self.state.players:
            possible_actions = self.get_vote_actions(player)
            possible_voting_actions_str = [action.text for action in possible_actions]
            player.state.observations.append(
                f"Dead players found: {', '.join([str(player) for player in dead_players])}"
            )
            player.state.observations.append(
                "Voting phase has started. You can vote who to banish"
            )

            if player.state == PlayerState.ALIVE:
                action = player.prompt_vote(possible_voting_actions_str)
                votes[player] = possible_actions[action].target
                player.state.observations.append(
                    f"You voted for {possible_actions[action].target}"
                )
                player.location = GameLocation.LOC_CAFETERIA
                playthrough_text = (
                    f"{player} voted for {possible_actions[action].target}"
                )
                self.state.playthrough.append(playthrough_text)
                if self.DEBUG:
                    print(playthrough_text)

        votes_counter = Counter(votes.values())
        two_most_common = votes_counter.most_common(2)
        if len(two_most_common) > 1 and two_most_common[0][1] == two_most_common[1][1]:
            self.broadcast_history("vote", "It's a tie! No one will be banished")
        else:
            assert isinstance(
                two_most_common[0][0], Player
            )  # Ensure that the expression is of type Player
            player_to_banish: Player = two_most_common[0][
                0
            ]  # Explicitly cast the expression to Player
            if player_to_banish == self.nobody:
                self.broadcast_history("vote", "Nobody was banished!")
            elif player_to_banish.is_impostor:
                self.broadcast_history(
                    "vote", f"{player_to_banish} was banished! They were an impostor"
                )
            else:
                self.broadcast_history(
                    "vote", f"{player_to_banish} was banished! They were a crewmate"
                )
            player_to_banish.state = PlayerState.DEAD
        for player, target in votes.items():
            self.broadcast_history(f"vote {player}", f"{player} voted for {target}")

        self.state.game_stage = GamePhase.ACTION_PHASE
        self.remove_dead_players()

    def get_vote_actions(self, player: Player) -> list[GameAction]:
        actions = []
        actions.append(GameAction(GameActionType.VOTE, player, self.nobody))
        for other_player in self.state.players:
            if other_player != player and other_player.state == PlayerState.ALIVE:
                actions.append(GameAction(GameActionType.VOTE, player, other_player))
        return actions

    def broadcast(self, key: str, message: str) -> None:
        for player in self.state.get_alive_players():
            player.state.observations.append(message)

    def broadcast_history(self, key: str, message: str) -> None:
        self.broadcast(key, message)

    def broadcast_message(self, message: str) -> None:
        self.broadcast("chat", message)

    def remove_dead_players(self) -> None:
        for player in self.state.players:
            if player.state == PlayerState.DEAD:
                player.state = PlayerState.DEAD_REPORTED

    def check_impostors_win(self) -> bool:
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        impostors_alive = [p for p in self.state.get_alive_players() if p.is_impostor]
        return len(impostors_alive) >= len(crewmates_alive)

    def check_crewmates_win(self) -> bool:
        return self.check_win_by_tasks() or self.check_crewmate_win_by_voting()

    def check_win_by_tasks(self) -> bool:
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        return all(
            task.completed for player in crewmates_alive for task in player.state.tasks
        )

    def check_crewmate_win_by_voting(self) -> bool:
        impostors_alive = [p for p in self.state.get_alive_players() if p.is_impostor]
        return len(impostors_alive) == 0

    def check_game_over(self) -> bool:
        return self.check_impostors_win() or self.check_crewmates_win()

    def check_game_over_action_crewmate(self) -> bool:
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        turns_passed = max(len(player.history) for player in crewmates_alive)
        completed_tasks = [
            task.completed for player in crewmates_alive for task in player.tasks
        ]

        if turns_passed >= 100:
            self.state.log_action(f"Turns passed: {turns_passed}")
            self.state.log_action(
                f"Crewmates lose! Too many turns passed! Completed tasks: {completed_tasks}"
            )
            self._save_playthrough()
            return True

        if all(completed_tasks):
            self.state.log_action(f"Turns passed: {turns_passed}")
            self._save_playthrough()
            return True

        return False

    def _save_playthrough(self) -> None:
        if self.save_playthrough:
            with open(self.save_playthrough, "w") as f:
                f.write("\n".join(self.state.playthrough))

    def end_game(self) -> None:
        if self.check_crewmate_win_by_voting():
            print("Crewmates win! All impostors were banished!")
            self.state.log_action("Crewmates win! All impostors were banished!")
        elif self.check_win_by_tasks():
            print("Crewmates win! All tasks were completed!")
            self.state.log_action("Crewmates win! All tasks were completed!")
        elif self.check_impostors_win():
            print("Impostors win!")
            self.state.log_action("Impostors win!")

        self._save_playthrough()

    def __repr__(self):
        return f"GameEngine | Players: {self.state.players} | Stage: {self.state.game_stage}"
