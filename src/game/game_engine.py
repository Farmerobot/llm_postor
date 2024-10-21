import time
from game.game_state import GameState
from game.models.engine import (
    GamePhase,
    GameLocation,
    DOORS,
)
from game.players.base_player import Player, PlayerRole
from game.models.history import PlayerState
from game.players.human import HumanPlayer
from game.models.action import GameAction, GameActionType
from typing import Any, List, Callable, Optional
import random
from game import consts as game_consts
from collections import Counter
from pydantic import BaseModel, Field
from game.gui_handler import GUIHandler


class GameEngine(BaseModel):
    state: GameState = Field(default_factory=GameState)
    nobody: HumanPlayer = Field(default_factory=lambda: HumanPlayer(name="Nobody"))
    gui_handler: GUIHandler = Field(default_factory=GUIHandler) # Initialize GUIHandler

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
            chosen_player.set_role(PlayerRole.IMPOSTOR)
            impostors_to_assign -= 1

        # Check for imbalanced team sizes AFTER role assignment
        crewmates_count = len(self.state.players) - impostor_count
        if impostor_count >= crewmates_count:
            raise ValueError(
                "Number of impostors cannot be greater than or equal to the number of crewmates."
            )

    def init_game(self) -> None:
        self.state.set_stage(GamePhase.ACTION_PHASE)

    def enter_main_game_loop(self, freeze_stage: Optional[GamePhase] = None) -> None:
        """
        Main game loop that controls the flow of the game.

        :param freeze_stage: If set, the game will stay in this stage (used for testing).
        """
        check_game_over = self.set_game_stage(freeze_stage)

        print("Game started!")
        while not check_game_over():
            print(f"Game stage: {self.state.game_stage}")
            if self.state.DEBUG:
                time.sleep(0.5)

            chosen_actions = self.get_player_actions()
            someone_reported = self.update_game_state(chosen_actions)
            
            self.gui_handler.update_gui(self.state)

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
                if self.state.DEBUG:
                    print(f"Player {player} actions: {possible_actions_str}")
                action_int = player.prompt_action(possible_actions_str)
                choosen_actions.append(possible_actions[action_int])
                if self.state.DEBUG:
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
            self.state.playthrough.append(f"[{action.player}]: {action}")
            if action.player.state.life != PlayerState.DEAD:
                action.player.kill_cooldown = max(0, action.player.kill_cooldown - 1)
                if action.type == GameActionType.REPORT:
                    self.broadcast_history(
                        "report", f"{action.player} reported a dead body"
                    )
                    reported_players = self.state.get_dead_players_in_location(
                        action.player.state.location
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
                        f"You were eliminated by {action.player}"
                    )

                action.player.state.action_result = action.do_action()

                # update stories of seen actions and players in room
                for player in self.state.players:
                    if (
                        player.state.life != PlayerState.DEAD
                        and player != action.player
                    ):
                        if (
                            action.player.state.location == player.state.location
                            or action.player.state.location
                            == player.history.rounds[-1].location
                        ):
                            playthrough_text = f"Player {player} saw action {action.spectator} when {player} were in {action.player.state.location.value}"
                            self.state.playthrough.append(playthrough_text)
                            if self.state.DEBUG:
                                print(playthrough_text)
                            player.state.seen_actions.append(
                                f"you saw {action.spectator} when you were in {action.player.state.location.value}"
                            )

        for player in self.state.players:
            # update player history
            player.log_state_new_round()
            
        # update players in room
        for player in self.state.players:
            players_in_room = [
                other_player
                for other_player in self.state.players
                if player.state.location == other_player.state.location
                and player != other_player
                and other_player.state.life == PlayerState.ALIVE
            ]

            playthrough_text = f"Player {player} is in {player.state.location.value} with {players_in_room}"
            self.state.playthrough.append(playthrough_text)
            if self.state.DEBUG:
                print(playthrough_text)
            if players_in_room:
                player.state.player_in_room = f"Players in room with you: {', '.join([str(player) for player in players_in_room])}"
            else:
                player.state.player_in_room = "You are alone in the room"

        return someone_reported

    def get_actions(self, player: Player) -> list[GameAction]:
        actions = []

        # actions for WAIT
        actions.append(GameAction(type=GameActionType.WAIT, player=player))

        # action for REPORT
        dead_players_in_room = self.state.get_dead_players_in_location(
            player.state.location
        )
        if dead_players_in_room:
            actions.append(
                GameAction(
                    type=GameActionType.REPORT,
                    player=player,
                    target=dead_players_in_room,
                )
            )

        # actions for MOVE
        for location in DOORS[player.state.location]:
            actions.append(
                GameAction(type=GameActionType.MOVE, player=player, target=location)
            )

        # actions for tasks DO_ACTION
        for task in player.state.tasks:
            if task.location == player.state.location and not task.completed:
                actions.append(
                    GameAction(
                        type=GameActionType.DO_ACTION, player=player, target=task
                    )
                )

        # actions for impostors KILL
        if player.is_impostor and player.kill_cooldown == 0:
            targets = self.state.get_player_targets(player)
            for target in targets:
                actions.append(
                    GameAction(type=GameActionType.KILL, player=player, target=target)
                )

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
                if player.state.life == PlayerState.ALIVE:
                    player.state.observations.append(
                        f"Discussion: [System]: You have {game_consts.NUM_CHATS - round} rounds left to discuss, then you will vote"
                    )
                    answer: str = player.prompt_discussion()
                    answer_str = f"Discussion: [{player}]: {answer}"
                    discussion_log.append(answer_str)
                    self.broadcast_message(answer_str)
            self.state.playthrough.append(f"Discussion log:")
            self.state.playthrough.append("\n".join(discussion_log))
            if self.state.DEBUG:
                print("Discussion log:")
                print("\n".join(discussion_log))

    def go_to_voting(self) -> None:
        dead_players = [
            player
            for player in self.state.players
            if player.state.life == PlayerState.DEAD
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

            if player.state.life == PlayerState.ALIVE:
                action = player.prompt_vote(possible_voting_actions_str)
                votes[player] = possible_actions[action].target
                player.state.observations.append(
                    f"You voted for {possible_actions[action].target}"
                )
                player.state.location = GameLocation.LOC_CAFETERIA
                playthrough_text = (
                    f"{player} voted for {possible_actions[action].target}"
                )
                self.state.playthrough.append(playthrough_text)
                if self.state.DEBUG:
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
        actions.append(
            GameAction(type=GameActionType.VOTE, player=player, target=self.nobody)
        )
        for other_player in self.state.players:
            if other_player != player and other_player.state.life == PlayerState.ALIVE:
                actions.append(
                    GameAction(
                        type=GameActionType.VOTE, player=player, target=other_player
                    )
                )
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
            if player.state.life == PlayerState.DEAD:
                player.state.life = PlayerState.DEAD_REPORTED

    def check_impostors_win(self) -> bool:
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        impostors_alive = [p for p in self.state.get_alive_players() if p.is_impostor]
        if len(impostors_alive) >= len(crewmates_alive):
            self.state.log_action(
                f"Impostors win! Impostors: {impostors_alive}, Crewmates: {crewmates_alive}"
            )
            for impostor in impostors_alive:
                impostor.state.tasks[0].complete(location=GameLocation.LOC_UNKNOWN)
            return True
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
            task.completed for player in crewmates_alive for task in player.state.tasks
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
        if self.state.save_playthrough:
            with open(self.state.save_playthrough, "w") as f:
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

    def to_dict(self):
        return self.state.dict()
