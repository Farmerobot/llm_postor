**Phase 1: Round Tracking and State Serialization**

1. **Add Round Counter:**
   - Introduce a `round_number` attribute to the `GameEngine` class.
   - Increment `round_number` at the beginning of each game loop iteration.

2. **Track Current Player:**
   - Add a `current_player_index` attribute to `GameEngine` to keep track of the player whose turn it is.
   - Initialize `current_player_index` to 0 at the start of the game.

3. **State Serialization:**
   - Implement a method `save_state(filename)` in `GameEngine` to serialize the current game state (including `round_number` and `current_player_index`) to a JSON file.
   - Create a method `load_state(filename)` to load a previously saved game state from a JSON file.

**Phase 2: Continue Game Functionality**

1. **Modify `enter_main_game_loop`:**
   - Add a parameter `continue_from_state` to `enter_main_game_loop`.
   - If `continue_from_state` is provided, call `load_state` to load the game state from the specified file.
   - If `continue_from_state` is not provided, start a new game as usual.

2. **Update Game Loop:**
   - Modify the game loop to use the loaded `round_number` and `current_player_index` if a state was loaded.
   - Ensure that the game loop continues from the correct round and player's turn.
   - Use `current_player_index` to determine which player should act next.
   - After each player's turn, increment `current_player_index` and wrap around to 0 if it reaches the end of the player list.

**Phase 3: Testing and Integration**

1. **Unit Tests:**
   - Write unit tests to verify the functionality of `save_state`, `load_state`, and `enter_main_game_loop` with the `continue_from_state` parameter.
   - Test scenarios where a game is saved, loaded, and continued from a specific round and player's turn.

2. **Integration with GUI:**
   - Update the GUI to allow users to save and load game states.
   - Provide a mechanism for users to select a saved state and continue playing from that point.
   - Display the current round number and the player whose turn it is in the GUI.

**Example Code Snippets:**

```python
# src/game/game_engine.py

class GameEngine(BaseModel):
    # ... other attributes ...
    round_number: int = 0
    current_player_index: int = 0

    def save_state(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump(self.dict(), f)

    def load_state(self, filename: str) -> None:
        with open(filename, "r") as f:
            data = json.load(f)
            self.__dict__.update(data)

    def enter_main_game_loop(self, continue_from_state: Optional[str] = None) -> None:
        if continue_from_state:
            self.load_state(continue_from_state)
        # ... rest of the game loop ...
        self.round_number += 1
        current_player = self.state.players[self.current_player_index]
        # ... get actions from current_player ...
        self.current_player_index = (self.current_player_index + 1) % len(self.state.players)
        # ... rest of the game loop ...
```

**Additional Considerations:**

- **State Consistency:** Ensure that all relevant game state information is saved and loaded correctly, including the `current_player_index`.
- **GUI Integration:** Design a user-friendly interface for saving, loading, and continuing games. Consider providing options to view the current round number and the player whose turn it is in the GUI.
- **Error Handling:** Implement robust error handling for file operations and state loading. Handle cases where the saved state is invalid or corrupted.
- **Performance:** Optimize the serialization and deserialization processes to minimize performance impact. Consider using efficient data structures and serialization libraries.
