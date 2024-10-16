# Zastosowanie dużych modeli językowych do tworzenia inteligentnych agentów w grach komputerowych
Kod źródłowy do pracy magisterskiej na kierunku Informatyka (specjalność: Sztuczna Inteligencja) na Wydziale Informatyki i Telekomunikacji Politechniki Poznańskiej.

## Instrukcja uruchomienia
Potrzebna wersja Pythona: 3.11

Praca wykorzystuję menadzer pakietów `poetry`, który można zainstalować korzystając z instrukcji na stronie [https://python-poetry.org/docs/](https://python-poetry.org/docs/)

Aby zainstalować wszystkie zależności przy pomocy narzędzia `poetry`, należy wykonać poniższe polecenie:
```bash
poetry install
```
Z racji użycia dużych modeli językowych konieczne jest podaine klucza API do OpenAI. Klucz można uzyskać na stronie [https://beta.openai.com/signup/](https://beta.openai.com/signup/). Po uzyskaniu klucza, należy go przypisać do zmiennej środowiskowej `OPENAI_API_KEY`.

Aby uruchomić wersje demonstracyjną, należy wykonać poniższe polecenie:
```bash
cd src
poetry run python demo.py
```

## Struktura
Here's a breakdown of the files and folders in your repository:

**Root Level:**

* **.gitignore:** This file tells Git which files and folders to ignore when tracking changes. It's used to prevent unnecessary files from being committed to the repository.
* **.idea:** This folder contains configuration files for the IntelliJ IDEA IDE. It's usually ignored in Git.
* **mypy.ini:** This file contains configuration settings for the Mypy static type checker.
* **poetry.lock:** This file locks down the versions of dependencies used in your project, ensuring consistent environments.
* **pyproject.toml:** This file defines your project's metadata and build settings, including dependencies and build tools.
* **src:** This folder contains the source code for your project.
  * **demo.py:** This file likely contains a demonstration or example script for your project.
  * **discussion_points_Warek_2024-10-09_09-54-45.txt:** This file appears to be a text file containing discussion points, possibly related to a specific meeting or event.
  * **discussion_points_Warek_2024-10-09_09-56-16.txt:** Another text file with discussion points.
  * **discussion_points_Warek_2024-10-09_09-58-51.txt:** Yet another text file with discussion points.
  * **game:** This folder contains code related to a game.
    * **__init__.py:** This file makes the "game" folder a Python package.
    * **__pycache__:** This folder contains compiled Python bytecode files, which are used to speed up execution.
    * **agents:** This folder contains code for different game agents.
      * **AdventureAgent.py:** This file contains code for an "AdventureAgent" class, which likely represents an agent that plays the game in an adventurous way.
      * **DiscussionAgent.py:** This file contains code for a "DiscussionAgent" class, which likely represents an agent that participates in discussions.
      * **VotingAgent.py:** This file contains code for a "VotingAgent" class, which likely represents an agent that votes during the game.
      * **__pycache__:** This folder contains compiled Python bytecode files.
    * **game_engine.py:** This file likely contains the main logic for running the game.
    * **game_results:** This folder contains results from game simulations or tests.
      * **Game1.txt:** This file likely contains results from a specific game simulation.
      * **Game2.txt:** Another file with game results.
      * **action_phase:** This folder contains results related to the action phase of the game.
      * **whole_game:** This folder contains results related to the entire game.
    * **models:** This folder contains code for game models and data structures.
      * **__init__.py:** This file makes the "models" folder a Python package.
      * **__pycache__:** This folder contains compiled Python bytecode files.
      * **game_models.py:** This file likely contains definitions for game models and data structures.
      * **player.py:** This file likely contains code for the "Player" class, which represents a player in the game.
      * **tasks.py:** This file likely contains code for the "Task" class, which represents a task that players can complete.
    * **utils.py:** This file likely contains utility functions for the game.
  * **test_ai_action_phase_crewmate.py:** This file likely contains tests for the AI's actions during the crewmate phase of the game.
  * **test_ai_whole_game.py:** This file likely contains tests for the AI's behavior throughout the entire game.
  * **utils.py:** This file likely contains utility functions for the game.

