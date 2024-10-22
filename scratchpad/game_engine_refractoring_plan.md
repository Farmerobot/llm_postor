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
   - Remove the `continue_from_state` parameter as it's always assumed the game will load from a state.
   - Directly call `load_state` at the beginning of the function to load the game state from the predefined file.

2. **Update Game Loop:**
   - Use the loaded `round_number` and `current_player_index` to control the game loop.
   - Instead of starting from `round_number = 0`, use the loaded `round_number` as the starting point.
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


**Additional Considerations:**

- **State Consistency:** Ensure that all relevant game state information is saved and loaded correctly, including the `current_player_index`.
- **GUI Integration:** Design a user-friendly interface for saving, loading, and continuing games. Consider providing options to view the current round number and the player whose turn it is in the GUI.
- **Error Handling:** Implement robust error handling for file operations and state loading. Handle cases where the saved state is invalid or corrupted.
- **Performance:** Optimize the serialization and deserialization processes to minimize performance impact. Consider using efficient data structures and serialization libraries.
