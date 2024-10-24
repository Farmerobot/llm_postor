# LLMPostor

[![Tests](https://github.com/Farmerobot/mk-ai-agents/actions/workflows/test.yml/badge.svg)](https://github.com/Farmerobot/mk-ai-agents/actions/workflows/test.yml)

Source code for a project in Artificial Intelligence at the Faculty of Computing and Telecommunications at Poznan University of Technology.

## Project Description

This project aims to test and compare the persuasive abilities of large language models (LLMs) in a game-like environment. The system simulates the game "Among Us," where AI agents, powered by various LLMs, interact, make decisions, and attempt to persuade each other.  The goal is to understand how different LLMs approach persuasion, deception, and social interaction within a complex, dynamic environment.  The project analyzes both the success of persuasive attempts and the strategies employed by the agents.

## Current Features

TODO

## Project Architecture

The project is structured into several modules:

* **`agents`**: Contains implementations of different AI agents, each using a specific LLM.
* **`models`**: Defines data structures for tasks and game state.
* **`players`**: Defines the players.
* **`data`**: Contains saved game states ready to analyze. files are named in following format: `game_state_<phase>_<action_phase_count>_<discussion_phase_count>_<who_won>_<id>.json`.

## Table of Contents

- Installation
- Usage
- Configuration
- Running Tests
- Contributing
- License

## Installation

This project requires Python 3.11 or higher.

### 1. Install Poetry

If you don't have Poetry installed, you can install it by following these steps:

- For Unix/macOS:
```bash
  curl -sSL https://install.python-poetry.org | python3 -
```
- For Windows:

  Visit the official [Poetry installation page](https://python-poetry.org/docs/#installation) for Windows-specific instructions.

Once installed, verify Poetry's installation by running:
```bash
  poetry --version
```
### 2. Clone the Repository and Install Dependencies

- Clone the repository:

```bash
  git clone https://github.com/username/llm_poster.git
  cd llm_poster
```

- Install dependencies using Poetry:

```bash
  poetry install
```

### 3. Activate the Virtual Environment

Once the dependencies are installed, activate the virtual environment:

```bash
  poetry shell
```

## Usage

To run the simulation with the GUI:

```bash
  poetry run run-gui
```

## Configuration

The project requires API keys for LLMs such as OpenAI. Set the following environment variables in your shell:

```bash
  export OPENAI_API_KEY=your-api-key
```

Alternatively, you can set these in a `.env` file at the project root.

## Running Tests

To run all tests, use the following command:

```bash
  poetry run pytest
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

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
