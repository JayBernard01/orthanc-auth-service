# First Steps -> after installing poetry
setup:
	poetry shell

install:
	poetry install --no-root

# In .vscode
# Make sure to use the interpreter in the poetry environement
# Opening the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).
# Typing and selecting Python: Select Interpreter.
# Choosing the interpreter from the Poetry environment.
py-env:
	poetry env info --path

run:
	poetry run python3 rest.py

# Use .vscode extensions instead for Ruff
lint:
	poetry run ruff --watch
	
# Testing
test:
	poetry run ruff check --fix
	poetry run pytest

