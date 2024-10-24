Here's a GUI development plan using Streamlit to visualize your Among Us game state, progressing from a basic JSON display to a richer, more interactive experience.


**Phase 2: Interactive Map (Medium Effort)**

* **Goal:** Create an interactive map visualizing the Among Us game map, displaying player locations, and highlighting selected players.  The map should update dynamically as players move.

* **Techniques:**

    * **Map Representation:** Use an image-based representation of the Among Us map. This provides a visually appealing and familiar context for players.

    * **Library Selection:**  `plotly` is the recommended library for this phase due to its capabilities for creating interactive web-based visualizations.  It allows for dynamic updates and easy handling of user interactions.

    * **Player Markers:** Represent each player with a distinct marker on the map, color-coded by role (Crewmate/Impostor) and status (Alive/Dead).  Consider using different marker shapes or sizes to further distinguish players.

    * **Dynamic Updates:** Leverage Streamlit's reactive capabilities and `plotly`'s update functionality to refresh the map whenever the game state changes.  This ensures the map always reflects the current player locations.

    * **Player Selection and Highlighting:** Implement click-to-select functionality. When a player marker is clicked, that player should be highlighted on the map (e.g., by changing the marker color, size, or adding a border).  Consider using `plotly`'s `click` event to detect user interactions.

    * **Data Binding:**  Establish a clear mapping between the game state data (player locations) and the map visualization.  This will ensure that updates to the game state automatically trigger corresponding updates on the map.

    * **Layout:**  Consider the map layout.  You might need to adjust marker positions to avoid overlaps, especially in crowded rooms.  Experiment with different marker sizes and positions to optimize readability.

    * **Tooltips:**  On hover over a player marker, display a tooltip showing the player's name, role, and status.  This provides additional information without cluttering the map.

    * **Room Highlighting (Optional):**  Consider highlighting the room where a significant event (e.g., a kill, a report) occurred.  This can be achieved by changing the color or opacity of the room area on the map.


**Phase 3: Timeline View with Streamlit Slider (High Effort)**

* **Goal:** Provide a chronological view of game events using a Streamlit slider to select rounds.  Clearly indicate the phase (Action, Discussion, Voting) for each round.

* **Techniques:**

    * **Streamlit Slider:** Use `st.slider` to allow users to select a specific round from the game.  The slider's range should be the total number of rounds in the game.

    * **Round Data Display:**  When a round is selected, display the relevant information for that round:
        * **Phase:** Clearly indicate whether the round was an Action, Discussion, or Voting phase.
        * **Player Actions:** Show the actions taken by each player during that round.
        * **Discussion Log (if applicable):** Display the discussion log for that round.
        * **Voting Results (if applicable):** Show the voting results for that round.

    * **Data Structure:** Ensure your game data is structured in a way that makes it easy to access the information for each round.  Consider using a list of dictionaries or a similar data structure.

    * **Clear Visual Indicators:** Use distinct visual cues (e.g., different colors, icons, or labels) to differentiate between Action, Discussion, and Voting phases.

    * **Error Handling:** Handle cases where the slider is moved beyond the valid range of rounds.


**Phase 4: Advanced Features (Advanced Effort)**

* **Goal:** Enhance the GUI with advanced features for analysis and replayability.  The prompts and actions should be displayed in a chat-like format.

* **Techniques:**
    * **Interactive Controls:** Implement controls to step through the game turn by turn, pause, rewind, or fast-forward.  This will allow users to replay the game and analyze decisions at their own pace.
    * **Data Export:** Allow users to export the game data (JSON or CSV) for further analysis.  Specifically, provide an option to export the discussion logs and LLM responses separately. This will facilitate detailed analysis of the language used by the agents and the effectiveness of their communication strategies.
    * **Chat-like Display:** Present the prompts and actions taken by the agents in a chat-like format. This will improve the readability and understanding of the game's progression.

This plan provides a structured approach to building your Streamlit GUI.  Start with Phase 1, then gradually add features from the subsequent phases based on your time and priorities. Remember to test frequently and iterate on your design.
