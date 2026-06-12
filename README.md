# DevTrack CLI 

> A Python-based command-line tool for managing users, projects, and tasks.

## Features

-  Create and manage **users**, **projects**, and **tasks** from the terminal
- Persistent storage via JSON — data survives restarts
- Project progress tracking (e.g. `50% — 2/4 tasks done`)
- Formatted, color-coded tables powered by [`rich`](https://github.com/Textualize/rich)
-  Filter tasks by status: `pending`, `completed`, or `all`
-  Unit tests with `pytest`

---

## Project Structure

```
devtrack/
├── main.py              # Entry point & argparse CLI
├── cli/
│   └── commands.py      # One function per CLI subcommand
├── models/
│   ├── user.py          # User model (owns projects)
│   ├── project.py       # Project model (owns tasks)
│   └── task.py          # Task model
├── utils/
│   ├── storage.py       # JSON load/save utilities
│   └── display.py       # Rich-powered display helpers
├── tests/
│   └── test_devtrack.py # Pytest test suite
├── data/
│   └── devtrack_data.json  # Persistent data file
├── Pipfile
└── requirements.txt
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/devtrack-cli.git
cd devtrack-cli
```

### 2. Install dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using Pipenv:**
```bash
pip install pipenv
pipenv install
pipenv shell
```

---

## Usage

All commands are run from the `devtrack/` directory:

```bash
python main.py <command> [options]
```

### Commands

| Command | Description |
|---|---|
| `add-user` | Create a new user |
| `list-users` | List all users |
| `add-project` | Add a project to a user |
| `list-projects` | List all projects for a user |
| `add-task` | Add a task to a project |
| `list-tasks` | List all tasks for a project |
| `complete-task` | Mark a task as complete |
| `filter-tasks` | Filter tasks by status |

### Examples

```bash
# Add users
python main.py add-user --name "Alex" --email "alex@dev.com"
python main.py add-user --name "Jordan"

# List users
python main.py list-users

# Add projects
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build a CLI" --deadline "2025-12-31"
python main.py add-project --user "Alex" --title "API Redesign"

# List projects
python main.py list-projects --user "Alex"

# Add tasks
python main.py add-task --project "CLI Tool" --title "Implement argparse"
python main.py add-task --project "CLI Tool" --title "Add file persistence" --description "Use JSON"
python main.py add-task --project "CLI Tool" --title "Write tests"

# List tasks
python main.py list-tasks --project "CLI Tool"

# Complete a task
python main.py complete-task --project "CLI Tool" --title "Implement argparse"

# Filter tasks
python main.py filter-tasks --status pending
python main.py filter-tasks --status completed
python main.py filter-tasks --status all
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Data Model

```
User (1)
 └── Project (many)
       └── Task (many)
```

All data is stored in `data/devtrack_data.json` and auto-loaded on every command.

---

## Dependencies

| Package | Purpose |
|---|---|
| `rich` | Terminal formatting — tables, colors, panels |
| `pytest` | Unit testing |

---

## Git Workflow

This project uses feature branches with meaningful commits:
- `feat/` — new features
- `fix/` — bug fixes
- `test/` — test additions
- `docs/` — documentation updates
