# Analysis of Persuasive Capabilities of Large Language Models in Computer Games

Source code for a project in Artificial Intelligence at the Faculty of Computing and Telecommunications at Poznan University of Technology.

## Project Description

This project aims to test and compare the persuasive abilities of large language models (LLMs) in a game-like environment. The system simulates the game "Among Us," where AI agents, powered by various LLMs, interact, make decisions, and attempt to persuade each other.

## Current Features

1. **Web GUI**: A user-friendly interface that allows:
   - Observation of game progress
   - Analysis of specific agent actions at various points
   - Insight into the thought and decision-making process of LLMs

2. **Interactive Map**: A visual representation of the game environment, showing locations and movements of AI agents.

3. **Post-Game Analysis**: After the game concludes, the system provides an in-depth analysis of the persuasive abilities demonstrated by AI agents.

4. **"Among Us" Simulation**: The project uses the popular game "Among Us" as a framework to test AI agents' abilities in interaction, deception, and persuasion.

5. **Multiple AI Agents**: The system supports multiple AI agents, each of which can be powered by a different LLM, enabling comparative analysis.

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

- **Configuration Panel**: For setting game parameters and selecting LLM models.
- **Real-time Statistics**: Dashboard for live game statistics.
- **NLP Metrics**: Display of language quality and effectiveness metrics.
- **Scenario Editor**: Tool for creating and modifying game scenarios.
- **Comparative Analysis Tools**: For comparing performance of different LLM models.
- **Export and Sharing**: Functionality for exporting game data and analysis results.
- **Human Player Interface**: Option for human participation alongside AI agents.
- **API Documentation**: For integrating custom LLM models or analytical tools.

These planned features aim to make the project more comprehensive and versatile for researchers and enthusiasts in AI and NLP fields.

This project offers a unique and interactive way to study the persuasive abilities of LLMs in a controlled, game-like environment, providing valuable insights for researchers in the field of artificial intelligence and natural language processing.
