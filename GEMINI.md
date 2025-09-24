# Gemini Project: AI Werewolf

## 1. Project Overview

This is a Python-based command-line Werewolf game where all players are AI agents powered by Large Language Models (LLMs). The project serves as an experimental platform for multi-agent systems, focusing on simulating social deduction and information asymmetry.

The core architecture consists of a `GameMaster` that orchestrates the game flow, a `GameState` to hold the "ground truth," and a collection of `Agent` classes representing the different roles (Werewolf, Seer, Villager, etc.). Each agent has its own instance of an LLM client (`zhipuai`) and makes decisions based on a combination of public history and private knowledge.

The primary LLM provider is configured to be Zhipu AI (智谱AI), as indicated by the `zhipuai` dependency and the `BaseAgent` implementation.

## 2. Key Files

*   `main.py`: The main entry point to start the game.
*   `game_master.py`: The central game engine. It controls the game phases (night, day, voting), manages player actions, and distributes information.
*   `game_state.py`: A data container for the current state of the game, including player lists, roles, and game history.
*   `config.py`: Handles loading the `API_KEY` from a `.env` file.
*   `agents/base_agent.py`: The abstract base class for all AI agents. It includes the core logic for interacting with the LLM, managing private knowledge, and defining standard actions like `discuss` and `vote`.
*   `agents/roles/`: This directory contains the specific implementations for each character role, inheriting from `BaseAgent`.

## 3. Building and Running

### 3.1. Installation

First, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 3.2. Configuration

The game requires an API key from Zhipu AI to function.

1.  Create a file named `.env` in the project root directory (`D:\Space\1_Crucible\Werewolf`).
2.  Add your API key to the file in the following format:

    ```
    API_KEY="your_zhipu_api_key_here"
    ```

### 3.3. Running the Game

Execute the `main.py` script to start the game. The game will run in the terminal, with the user acting as a host/observer who presses "Enter" to advance the game stages.

```bash
python main.py
```

## 4. Development Conventions

*   **Agent-Based Architecture**: The logic for each player is encapsulated within its own `Agent` class. Agents are responsible for their own decision-making (`think` method).
*   **Information Control**: The `GameMaster` is the single source of truth and is responsible for information control. It provides each agent with only the information it is supposed to know, simulating the information asymmetry of a real Werewolf game.
*   **Adding New Roles**: To add a new role, create a new Python file in the `agents/roles/` directory. The file should contain a class that inherits from `BaseAgent` and implements the necessary methods, particularly `night_action`. The new role class must then be imported and added to the `role_classes` dictionary in `game_master.py`.
*   **LLM Interaction**: All LLM prompts and interactions are centralized in the `BaseAgent`. The `get_prompt` method constructs the context for the LLM, including role, name, and private knowledge.
