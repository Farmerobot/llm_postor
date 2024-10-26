import random
import json
import streamlit as st
from typing import Any, List
from collections import Counter
from pydantic import BaseModel, Field

from llm_postor.game import consts as game_consts
from llm_postor.game.game_state import GameState
from llm_postor.game.models.engine import (
    GamePhase,
    GameLocation,
    DOORS,
)
from llm_postor.game.players.base_player import Player, PlayerRole
from llm_postor.game.models.history import PlayerState
from llm_postor.game.players.human import HumanPlayer
from llm_postor.game.models.action import GameAction, GameActionType
from llm_postor.game.players.ai import AIPlayer
from llm_postor.game.players.fake_ai import FakeAIPlayer
from llm_postor.game.models.tasks import ShortTask, LongTask, Task
from llm_postor.game.agents.base_agent import Agent

class GameEngine(BaseModel):
    """Manages the game logic, including player actions, game state transitions, and win conditions."""
    state: GameState = Field(default_factory=GameState)
    nobody: HumanPlayer = Field(default_factory=lambda: HumanPlayer(name="Nobody"))

    def load_players(self, players: List[Player], impostor_count: int = 1) -> None:
        """Loads players into the game and assigns roles (crewmate or impostor)."""
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

    def init_game(self, game_state: GameState) -> None:
        """Initializes the game with a given game state."""
        self.state = game_state

    def init_game(self) -> None:
        """Initializes the game. Tries to set state from file, otherwise starts a new game."""
        if not self.load_state():
            self.state.set_stage(GamePhase.ACTION_PHASE)

    def perform_step(self) -> bool:
        """Executes a single step in the game, handling player turns and game state transitions.
        only when player successfully completes the action, the next player will be called to act.
        otherwise, the same player will be called to act again on next function call.
        
        :return: True if the game is over or in MAIN_MENU stage, False otherwise
        """
        if self.state.game_stage == GamePhase.ACTION_PHASE:
            self.state.log_action(f"Action: round: {self.state.round_number}. Player to act: {self.state.player_to_act_next}")
            self.perform_action_step()
        elif self.state.game_stage == GamePhase.DISCUSS:
            start = self.state.round_of_discussion_start
            now = self.state.round_number
            max = game_consts.NUM_CHATS
            self.state.log_action(f"Discussion ({now-start+1}/{max}): round: {now}. Player to act: {self.state.player_to_act_next}")
            self.perform_discussion_step()
        else:
            print("Game is in MAIN_MENU stage - read_only mode")
            return True
        if self.check_game_over():
            self.end_game()
            return True
        self.state.player_to_act_next += 1
            
        # Only when round is over (all players have acted), the players' states are moved to history and the next round starts.
        # this is because players can see actions from entire round, not just their own turn.
        if self.state.player_to_act_next == len(self.state.players):
            self.state.player_to_act_next = 0
            self.state.round_number += 1
            for player in self.state.players:
                player.log_state_new_round()
            if (
                self.state.round_of_discussion_start + game_consts.NUM_CHATS
                <= self.state.round_number
                and self.state.game_stage == GamePhase.DISCUSS
            ):
                self.go_to_voting()
                
        # Skip dead players. This even works if dead players are at the end of round or at the beginning
        # We check if next player is dead, and if so, we update the player_to_act_next to the next player
        while (
            self.state.players[self.state.player_to_act_next].state.life
            != PlayerState.ALIVE
        ):
            self.state.player_to_act_next = (self.state.player_to_act_next + 1) % len(
                self.state.players
            )
            self.state.log_action(f"Player to act next set to: {self.state.player_to_act_next}")
            # if we happen to reach the end of the list, we need to start from the beginning and update the round number
            # This is the same code as above, but we need to repeat it here, because we might have skipped dead players at the end
            if self.state.player_to_act_next == 0:
                self.state.round_number += 1
                for player in self.state.players:
                    # update player history
                    player.log_state_new_round()
                if (
                    self.state.round_of_discussion_start + game_consts.NUM_CHATS
                    <= self.state.round_number
                    and self.state.game_stage == GamePhase.DISCUSS
                ):
                    self.go_to_voting()
        self.save_state()
        return False

    def perform_action_step(self) -> None:
        """Handles the action phase of the game, where players take actions like moving, completing tasks, or killing."""
        chosen_action = self.get_player_action()
        self.update_game_state(chosen_action)

    def get_player_action(self) -> GameAction:
        """Gets the action chosen by the current player. LLMs are called here."""
        choosen_action: GameAction = None
        # Use round_number and current_player_index to determine the player's turn
        current_player = self.state.players[self.state.player_to_act_next]
        possible_actions = self.get_actions(current_player)
        possible_actions_str = [action.text for action in possible_actions]
        action_int = current_player.prompt_action(possible_actions_str)
        choosen_action = possible_actions[action_int]
        return choosen_action

    def update_game_state(self, action: GameAction) -> None:
        """Updates the game state based on the action taken by a player."""
        # REPORT
        if action.type == GameActionType.REPORT:
            self.broadcast_observation("report", f"{action.player} reported a dead body")
            reported_players = self.state.get_dead_players_in_location(
                action.player.state.location
            )
            assert reported_players
            self.broadcast_observation(
                "dead_players",
                f"Dead players found: {reported_players}",
            )
            self.state.set_stage(GamePhase.DISCUSS)

        prev_location = action.player.state.location

        # KILL, TASK, MOVE, WAIT - location changed
        action.player.state.action_result = action.do_action()

        # update stories of seen actions and players in room
        # when moving to a room, player can see actions of other players in both rooms
        players_in_room = self.state.get_players_in_location(prev_location)
        if action.player.state.location != prev_location:
            players_in_room += self.state.get_players_in_location(
                action.player.state.location
            )
        if action.player in players_in_room:
            players_in_room.remove(action.player)

        for player in players_in_room:
            if player != action.player:
                player.state.seen_actions.append(
                    f"you saw {action.spectator} when you were in {action.player.state.location.value}"
                )

        self.state.log_action(f"{action.spectator}")
        if players_in_room:
            self.state.log_action(f"{players_in_room} saw this action")
        else:
            self.state.log_action(f"No one saw this action")

        # update players in room
        for player in self.state.players:
            players_in_room = [
                other_player
                for other_player in self.state.players
                if player.state.location == other_player.state.location
                and player != other_player
                and other_player.state.life == PlayerState.ALIVE
            ]
            if players_in_room:
                player.state.player_in_room = f"Players in room with you: {players_in_room}"
            else:
                player.state.player_in_room = "You are alone in the room"

    def get_actions(self, player: Player) -> list[GameAction]:
        """Gets a list of possible actions for a given player."""
        actions = []

        # actions for WAIT
        actions.append(GameAction(type=GameActionType.WAIT, player=player))

        # action for REPORT
        dead_players_in_room = self.state.get_dead_players_in_location(
            player.state.location
        )
        for dead in dead_players_in_room:
            actions.append(
                GameAction(
                    type=GameActionType.REPORT,
                    player=player,
                    target=dead,
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

    def perform_discussion_step(self) -> None:
        """Handles the discussion phase of the game, where players can chat and discuss their suspicions. LLMs are called here."""
        player = self.state.players[self.state.player_to_act_next]
        player.state.observations.append(
            f"Discussion: [System]: You have {self.state.round_of_discussion_start+game_consts.NUM_CHATS - self.state.round_number} rounds left to discuss, then you will vote"
        )
        answer: str = player.prompt_discussion()
        answer_str = f"Discussion: [{player}]: {answer}"
        self.broadcast_message(answer_str)

    def go_to_voting(self) -> None:
        """Initiates the voting phase of the game, where players vote to banish a suspect. 
        LLMs are called here. There is no step. Voting is itself an entire step"""
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
                votes[player.name] = possible_actions[action].target.name
                player.state.observations.append(
                    f"You voted for {possible_actions[action].target}"
                )
                player.state.location = GameLocation.LOC_CAFETERIA
                playthrough_text = (
                    f"{player} voted for {possible_actions[action].target}"
                )
                self.state.log_action(playthrough_text)

        votes_counter = Counter(votes.values())
        two_most_common = votes_counter.most_common(2)
        if len(two_most_common) > 1 and two_most_common[0][1] == two_most_common[1][1]:
            self.broadcast_observation("vote", "It's a tie! No one will be banished")
        else:
            player_to_banish = [x for x in self.state.players if x.name == two_most_common[0][0]][0]
            assert isinstance(
                player_to_banish, Player
            )  # Ensure that the expression is of type Player
            if player_to_banish == self.nobody:
                self.broadcast_observation("vote", "Nobody was banished!")
            elif player_to_banish.is_impostor:
                self.broadcast_observation(
                    "vote", f"{player_to_banish} was banished! They were an impostor"
                )
            else:
                self.broadcast_observation(
                    "vote", f"{player_to_banish} was banished! They were a crewmate"
                )
            player_to_banish.state.life = PlayerState.DEAD
        for player, target in votes.items():
            self.broadcast_observation(f"vote {player}", f"{player} voted for {target}")

        self.state.set_stage(GamePhase.ACTION_PHASE)
        self.mark_dead_players_as_reported()

    def get_vote_actions(self, player: Player) -> list[GameAction]:
        """Gets a list of possible voting actions for a given player."""
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

    def broadcast_observation(self, key: str, message: str) -> None:
        """Broadcasts an observation to all alive players. Players state observations are updated."""
        self.state.log_action(f"{key}: {message}")
        for player in self.state.get_alive_players():
            player.state.observations.append(f"{key}: {message}")

    def broadcast_message(self, message: str) -> None:
        """Broadcasts a chat message to all alive players."""
        self.broadcast_observation("chat", message)

    def mark_dead_players_as_reported(self) -> None:
        """Marks all dead players as reported to avoid double reporting."""
        for player in self.state.players:
            if player.state.life == PlayerState.DEAD:
                player.state.life = PlayerState.DEAD_REPORTED

    def check_impostors_win(self) -> bool:
        """Checks if the impostors have won the game."""
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
        """Checks if the crewmates have won the game."""
        return self.check_win_by_tasks() or self.check_crewmate_win_by_voting() or self.check_game_over_action_crewmate()

    def check_win_by_tasks(self) -> bool:
        """Checks if the crewmates have won by completing all tasks."""
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        return all(
            task.completed for player in crewmates_alive for task in player.state.tasks
        )

    def check_crewmate_win_by_voting(self) -> bool:
        """Checks if the crewmates have won by banishing all impostors."""
        impostors_alive = [p for p in self.state.get_alive_players() if p.is_impostor]
        return len(impostors_alive) == 0

    def check_game_over(self) -> bool:
        """Checks if the game is over."""
        return self.check_impostors_win() or self.check_crewmates_win()

    def check_game_over_action_crewmate(self) -> bool:
        """Checks if the game is over based on crewmate actions (turns passed or tasks completed)."""
        crewmates_alive = [
            p for p in self.state.get_alive_players() if not p.is_impostor
        ]
        turns_passed = max(len(player.history.rounds) for player in crewmates_alive)
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
        """Saves the game playthrough to a file if specified."""
        if self.state.save_playthrough:
            with open(self.state.save_playthrough, "w") as f:
                f.write("\n".join(self.state.playthrough))

    def end_game(self) -> None:
        """Ends the game and saves the final state."""
        if self.check_crewmate_win_by_voting():
            self.state.log_action("Crewmates win! All impostors were banished!")
        elif self.check_win_by_tasks():
            self.state.log_action("Crewmates win! All tasks were completed!")
        elif self.check_impostors_win():
            self.state.log_action("Impostors win!")

        self.save_state()
        self._save_playthrough()

    def save_state(self) -> None:
        """Saves the current game state to a file."""
        with open(game_consts.STATE_FILE, "w") as f:
            for player in self.state.players:
                if isinstance(player, AIPlayer):
                    player.adventure_agent = None
                    player.discussion_agent = None
                    player.voting_agent = None
            json.dump(self.state.model_dump(), f)
            for player in self.state.players:
                if isinstance(player, AIPlayer):
                    player.init_agents()
            # yaml.dump(self.state.model_dump(), f)

    def load_state(self) -> bool:
        """Loads a previously saved game state from a file.
        :return: True if the state was successfully loaded, False otherwise
        """
        try:
            with open(game_consts.STATE_FILE, "r") as f:
                data = json.load(f)
                # Deserialize players based on their type
                players = [
                    self._create_player_from_dict(player_data)
                    for player_data in data["players"]
                ]
                data["players"] = players
                self.state = GameState.model_validate(
                    {**data}
                )  # Update GameState with deserialized players
        except FileNotFoundError:
            print("No saved state found. Starting new game.")
            return False
        except Exception as e:
            return False
        return True

    def _create_player_from_dict(self, player_data: dict) -> Player:
        """Creates a Player object from a dictionary representation."""
        # Deserialize tasks for the player's current state
        player_data["state"]["tasks"] = [
            self._create_task_from_dict(task_data)
            for task_data in player_data["state"]["tasks"]
        ]

        # Deserialize tasks for each round in the player's history
        for round_data in player_data["history"]["rounds"]:
            round_data["tasks"] = [
                self._create_task_from_dict(task_data)
                for task_data in round_data["tasks"]
            ]
        llm_model_name = player_data.get("llm_model_name", "none")
        if llm_model_name is None:
            return HumanPlayer(**player_data)
        elif llm_model_name == "fake":
            return FakeAIPlayer(**player_data)
        else:
            return AIPlayer(**player_data)

    def _create_task_from_dict(self, task_data: dict) -> Task:
        """Creates a Task object from a dictionary representation."""
        if "turns_left" in task_data:
            return LongTask(**task_data)
        else:
            return ShortTask(**task_data)

    def __repr__(self):
        """Returns a string representation of the GameEngine object."""
        return self.to_dict()

    def to_dict(self):
        """Returns a dictionary representation of the GameEngine object."""
        return self.state.to_dict()
