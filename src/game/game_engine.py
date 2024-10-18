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
from game.models.player import Player, HumanPlayer
from game.models.game_models import GameAction, GameActionType
from game.utils import get_random_tasks
from typing import List, Callable, Optional
import random
from game import consts as game_consts
from collections import OrderedDict, Counter


class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.nobody = HumanPlayer("Nobody")
        self.save_playthrough = ""
        self.DEBUG = False

    def load_players(self, players: List[Player], impostor_count: int = 1) -> None:
        if len(players) < 3:
            raise ValueError("Minimum number of players is 3.")

        if impostor_count >= len(players) or impostor_count <= 0:
            raise ValueError("Invalid number of impostors")

        for player in players:
            self.state.add_player(player)

        # Count existing impostors
        existing_impostors = sum(1 for player in self.state.players if player.role == PlayerRole.IMPOSTOR)

        # Assign impostors randomly, only if needed
        impostors_to_assign = impostor_count - existing_impostors
        while impostors_to_assign > 0:
            available_players = [p for p in self.state.players if p.role != PlayerRole.IMPOSTOR]
            if not available_players:
                break  # No more players to assign as impostors
            chosen_player = random.choice(available_players)
            chosen_player.set_role(PlayerRole.IMPOSTOR)
            impostors_to_assign -= 1

        # Check for imbalanced team sizes AFTER role assignment
        crewmates_count = len(self.state.players) - impostor_count
        if impostor_count >= crewmates_count:
            raise ValueError("Number of impostors cannot be greater than or equal to the number of crewmates.")


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
                self.go_to_discussion()
                self.go_to_voting()
            self.gui.update_gui()

        # END OF GAME
        if freeze_stage is None:
            print("Game Over!")
            self.end_game()

    def set_game_stage(self, freeze_stage: Optional[GamePhase]) -> Callable[[], bool]:
        """Set the game stage and return the appropriate game over check function."""
        if freeze_stage:
            self.game_stage = freeze_stage
            return self.check_game_over_action_crewmate
        return self.check_game_over

    def get_player_actions(self) -> list[GameAction]:
        """Get actions from all alive players."""
        choosen_actions: list[GameAction] = []
        for player in self.state.players:
            if player.player_state == PlayerState.ALIVE:
                possible_actions = self.get_actions(player)
                possible_actions_str = [
                    action.get_input_story() for action in possible_actions
                ]
                action_int = player.prompt_action(
                    "Choose an action", possible_actions_str
                )
                choosen_actions.append(possible_actions[action_int])
        return choosen_actions

    def update_game_state(self, actions: list[GameAction]) -> bool:
        """
        Update game state based on actions
        actions are sorted by action type in way that actions with higher priority are first
        ex: REPORT > KILL > DO_ACTION > MOVE > WAIT
        Players can see actions of other players in the same room
        """
        actions.sort(key=lambda x: x.action_type, reverse=True)

        for action in actions:
            self.state.playthrough.append(f"[{action.source}]: {action}")
            if self.DEBUG:
                print(f"[{action.source}]: {action}")  # DEBUG
            action.source.history.append(OrderedDict())  # create new history entry
            action.source.prev_location = None
            if action.source.player_state != PlayerState.DEAD:
                action.source.kill_cooldown = max(0, action.source.kill_cooldown - 1)
                if action.action_type == GameActionType.REPORT:
                    self.broadcast_history(
                        "report", f"{action.source} reported a dead body"
                    )
                    self.broadcast_history(
                        "dead_players",
                        f"Dead players found: {', '.join([str(player) for player in self.state.players if player.player_state == PlayerState.DEAD])}",
                    )
                    return True  # in case of report; go to discussion
                if action.action_type == GameActionType.MOVE:
                    action.source.prev_location = action.source.get_location()
                if action.action_type == GameActionType.KILL and isinstance(
                    action.target, Player
                ):
                    action.target.history[-1][
                        "killed"
                    ] = f"You were killed by {action.source}"

                action.source.history[-1][
                    "action_result"
                ] = action.do_action()  # do action and save result in history

        for action in actions:
            if action.source.player_state != PlayerState.DEAD:
                for (
                    player
                ) in (
                    self.state.players
                ):  # update stories of seen actions and players in room
                    if (
                        player.player_state != PlayerState.DEAD
                        and player != action.source
                    ):
                        if (
                            action.location == player.player_location
                            or action.location == player.prev_location
                        ):
                            self.state.playthrough.append(
                                f"Player {player} saw action {action.get_spectator_story()} when {player} were in {HUMAN_READABLE_LOCATIONS[action.location]}"
                            )
                            if self.DEBUG:
                                print(
                                    f"Player {player} saw action {action.get_spectator_story()} when {player} were in {HUMAN_READABLE_LOCATIONS[action.location]}"
                                )  # DEBUG
                            seen_actions: list[str] = player.history[-1].get(
                                "seen_action", []
                            )
                            seen_actions.append(
                                f"you saw {action.get_spectator_story()} when you were in {HUMAN_READABLE_LOCATIONS[action.location]}"
                            )
                            player.history[-1]["seen_action"] = seen_actions

        # update players in room
        for player in self.state.players:
            players_in_room = [
                other_player
                for other_player in self.state.players
                if player.get_location() == other_player.get_location()
                and player != other_player
                and other_player.player_state == PlayerState.ALIVE
            ]
            player.history[-1][
                "Current_location"
            ] = f"You are in {HUMAN_READABLE_LOCATIONS[player.get_location()]}"

            self.state.playthrough.append(
                f"Player {player} is in {HUMAN_READABLE_LOCATIONS[player.get_location()]} with {players_in_room}"
            )
            if self.DEBUG:
                print(
                    f"Player {player} is in {HUMAN_READABLE_LOCATIONS[player.get_location()]} with {players_in_room}"
                )
            if players_in_room:
                player.history[-1][
                    "player_in_room"
                ] = f"Players in room with you: {', '.join([str(player) for player in players_in_room])}"
            else:
                player.history[-1]["player_in_room"] = "You are alone in the room"
        return False

    def get_actions(self, player: Player) -> list[GameAction]:
        actions = []
        # actions for waiting
        actions.append(GameAction(GameActionType.WAIT, player))
        # action for reporting
        dead_players_in_room = [
            dead_player
            for dead_player in self.state.get_dead_players()
            if dead_player.player_location == player.player_location
        ]
        if dead_players_in_room:
            actions.append(
                GameAction(GameActionType.REPORT, player, dead_players_in_room)
            )
        # actions for moves
        for location in DOORS[player.player_location]:
            actions.append(GameAction(GameActionType.MOVE, player, location))
        # actions for tasks
        for task in player.player_tasks:
            if task.location == player.player_location and not task.completed:
                actions.append(GameAction(GameActionType.DO_ACTION, player, task))
        # actions for impostors
        if player.is_impostor and player.kill_cooldown == 0:
            targets = [
                other_player
                for other_player in self.state.players
                if other_player.player_state == PlayerState.ALIVE
                and other_player != player
                and other_player.player_location == player.player_location
            ]
            for target in targets:
                actions.append(GameAction(GameActionType.KILL, player, target))

        return actions

    def go_to_discussion(self) -> None:
        self.game_stage = GamePhase.DISCUSS
        for player in self.state.players:
            player.set_stage(GamePhase.DISCUSS)
            player.history.append(OrderedDict())
            player.chat_history.append([])
            player.history[-1][
                "discussion"
            ] = "Discussion phase has started. You can discuss and vote who to banish"

        discussion_log: list[str] = []
        for round in range(game_consts.NUM_CHATS):
            for player in self.state.players:
                if player.player_state == PlayerState.ALIVE:
                    player.history[-1][
                        "turns left"
                    ] = f"You have {game_consts.NUM_CHATS - round} rounds left to discuss, then you will vote"
                    answer: str = player.prompt_discussion()
                    answer_str = f"[{player}]: {answer}"
                    discussion_log.append(answer_str)
                    self.broadcast_message(answer_str)
                    player.discussion_prompt = ""  # clear prompt for next round
            self.state.playthrough.append(f"Discussion log:")
            self.state.playthrough.append("\n".join(discussion_log))
            if self.DEBUG:
                print("Discussion log:")
                print("\n".join(discussion_log))

    def go_to_voting(self) -> None:
        dead_players = [
            player
            for player in self.state.players
            if player.player_state == PlayerState.DEAD_REPORTED
        ]
        votes = {}
        for player in self.state.players:
            possible_actions = self.get_vote_actions(player)
            possible_voting_actions_str = [
                action.get_input_story() for action in possible_actions
            ]
            player.history[-1][
                "found_dead"
            ] = f"Dead players found: {', '.join([str(player) for player in dead_players])}"
            player.history[-1][
                "voting"
            ] = "Voting phase has started. You can vote who to banish\n"

            if player.player_state == PlayerState.ALIVE:
                action = player.prompt_vote(possible_voting_actions_str)
                votes[player] = possible_actions[action].target
                player.history[-1][
                    "vote"
                ] = f"You voted for {possible_actions[action].target}"
                player.player_location = GameLocation.LOC_CAFETERIA
                self.state.playthrough.append(
                    f"{player} voted for {possible_actions[action].target}"
                )
                if self.DEBUG:
                    print(f"{player} voted for {possible_actions[action].target}")

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
            player_to_banish.set_state(PlayerState.DEAD)
        for player, target in votes.items():
            self.broadcast_history(f"vote {player}", f"{player} voted for {target}")

        self.game_stage = GamePhase.ACTION_PHASE
        self.remove_dead_players()

    def get_vote_actions(self, player: Player) -> list[GameAction]:
        actions = []
        actions.append(GameAction(GameActionType.VOTE, player, self.nobody))
        for other_player in self.state.players:
            if (
                other_player != player
                and other_player.player_state == PlayerState.ALIVE
            ):
                actions.append(GameAction(GameActionType.VOTE, player, other_player))
        return actions

    def broadcast(self, key: str, message: str) -> None:
        for player in self.state.get_alive_players():
            if key == "chat":
                player.chat_history[-1].append(message)
            else:
                player.history[-1][key] = message

    def broadcast_history(self, key: str, message: str) -> None:
        self.broadcast(key, message)

    def broadcast_message(self, message: str) -> None:
        self.broadcast("chat", message)

    def remove_dead_players(self) -> None:
        for player in self.state.players:
            if player.player_state == PlayerState.DEAD:
                player.set_state(PlayerState.DEAD_REPORTED)

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
            task.completed for player in crewmates_alive for task in player.player_tasks
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
        turns_passed = max(player.turns_passed() for player in crewmates_alive)
        completed_tasks = [
            task.completed for player in crewmates_alive for task in player.player_tasks
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

        self.state = GameState()  # Reset the game state
        self._save_playthrough()

    def __repr__(self):
        return f"GameEngine | Players: {self.state.players} | Stage: {self.state.game_stage}"
