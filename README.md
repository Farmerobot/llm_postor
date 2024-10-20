# Analysis of Persuasive Capabilities of Large Language Models in Computer Games

Source code for a project in Artificial Intelligence at the Faculty of Computing and Telecommunications at Poznan University of Technology.

## Project Description

This project aims to test and compare the persuasive abilities of large language models (LLMs) in a game-like environment. The system simulates the game "Among Us," where AI agents, powered by various LLMs, interact, make decisions, and attempt to persuade each other.  The goal is to understand how different LLMs approach persuasion, deception, and social interaction within a complex, dynamic environment.  The project analyzes both the success of persuasive attempts and the strategies employed by the agents.

## Current Features

1. **Web GUI**: A user-friendly interface built using [insert framework used, e.g., Flask, Streamlit] that allows:
   - Observation of game progress in real-time.
   - Analysis of specific agent actions at various points in the game, including transcripts of conversations and decision-making processes.
   - Insight into the thought and decision-making process of LLMs through logging of their internal states (if available from the LLM).

2. **Interactive Map**: A visual representation of the game environment, showing locations and movements of AI agents, using [insert library used, e.g., Pygame, a JavaScript library].

3. **Post-Game Analysis**: After the game concludes, the system provides an in-depth analysis of the persuasive abilities demonstrated by AI agents, including metrics such as:
    * Success rate of persuasive attempts.
    * Frequency of different persuasive techniques used.
    * Correlation between LLM model and persuasive success.

4. **"Among Us" Simulation**: The project uses the popular game "Among Us" as a framework to test AI agents' abilities in interaction, deception, and persuasion.  The core mechanics of tasks, meetings, voting, and impostors are replicated.

5. **Multiple AI Agents**: The system supports multiple AI agents, each of which can be powered by a different LLM (e.g., GPT-3, GPT-4, other open-source models), enabling comparative analysis of their persuasive capabilities.

## Project Architecture

The project is structured into several modules:

* **`game_engine`**: Manages the game logic, including task assignment, player interactions, and game state transitions.
* **`agents`**: Contains implementations of different AI agents, each using a specific LLM.
* **`models`**: Defines data structures for players, tasks, and game state.
* **`gui`**: Handles the user interface and visualization.
* **`utils`**: Contains helper functions.

## Technologies Used

* **Python 3.11**: Programming language.
* **[List Libraries/Frameworks Used, e.g., Pydantic, Flask, Pygame, etc.]**:  Specific libraries and frameworks used for data modeling, web development, game visualization, etc.
* **OpenAI API**: For accessing large language models.


## Running Instructions

Required Python version: 3.11

The project uses the `poetry` package manager, which can be installed following the instructions at [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

To install all dependencies using `poetry`, execute the following command:
```bash
poetry install
```

Due to the use of large language models, it is necessary to provide an OpenAI API key. The key can be obtained at [https://beta.openai.com/signup/](https://beta.openai.com/signup/). After obtaining the key, assign it to the `OPENAI_API_KEY` environment variable.

To run the demonstration version, execute the following command:
```bash
cd src
poetry run python demo.py
```

## Future Enhancements (Roadmap)

We are planning to add the following features to enhance the project:

- **Configuration Panel**: A web-based configuration panel for setting game parameters (number of players, impostors, task difficulty), selecting LLM models, and customizing game scenarios.
- **Real-time Statistics**: A dashboard displaying live game statistics, such as task completion rates, voting patterns, and agent success rates.
- **NLP Metrics**: Integration of NLP metrics (e.g., sentiment analysis, readability scores) to analyze the quality and effectiveness of the language used by the AI agents.
- **Scenario Editor**: A tool for creating and modifying game scenarios, allowing researchers to test the AI agents in different contexts and situations.
- **Comparative Analysis Tools**: Advanced tools for comparing the performance of different LLM models, including statistical analysis and visualization of results.
- **Export and Sharing**: Functionality for exporting game data and analysis results in various formats (e.g., CSV, JSON) for further analysis and sharing.
- **Human Player Interface**:  Allowing human players to participate in the game alongside AI agents, providing a more realistic and challenging environment for testing.
- **API Documentation**: Comprehensive API documentation for integrating custom LLM models or analytical tools.
- **Automated Testing**:  Implementation of automated tests to ensure the robustness and reliability of the game engine and AI agents.


These planned features aim to make the project more comprehensive and versatile for researchers and enthusiasts in AI and NLP fields.

This project offers a unique and interactive way to study the persuasive abilities of LLMs in a controlled, game-like environment, providing valuable insights for researchers in the field of artificial intelligence and natural language processing.
