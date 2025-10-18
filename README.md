# XiangQi (Chinese Chess) Project

This project aims to implement a complete, rules-accurate XiangQi (Chinese Chess) engine with both CLI and GUI front-ends in Python.

## 1. Python Version
Tested with Python 3.13.5 (should also work on 3.11+). If you run into dependency wheels (e.g. pygame), prefer the latest stable Python 3.12/3.11 for production use.

## 2. Directory Overview
```
xiangqi/
  core/        # Board model, enums, pieces, move representation
  rules/       # Pseudo move generatopygame==2.5.2pygame==2.5.2rs and legality / check detection
  engine/      # Game state orchestration, future search helpers
  cli/         # Text (Typer) interface
  ui/          # Pygame UI and rendering helpers
  ai/          # Future evaluation + search
 tests/         # Pytest-based tests
requirements*.txt  # Dependency groups
mypy.ini           # Type checking configuration
ruff.toml          # Lint configuration (Ruff)
```

## 3. Creating a Virtual Environment (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```
If execution policy blocks activation:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Installing Dependencies
Pick the groups you need (order is safe):
```
pip install -r requirements.txt          # core (may be empty initially)
pip install -r requirements-ui.txt       # pygame for GUI
pip install -r requirements-cli.txt      # typer for CLI
pip install -r requirements-dev.txt      # pytest, mypy, ruff, coverage
```
Optional one-liner (PowerShell):
```
Get-ChildItem -Filter requirements*.txt | ForEach-Object { pip install -r $_.Name }
```

## 5. Running the CLI
From project root (venv active):
```
python -m xiangqi.cli.cli_main
```
Enter moves in algebraic-like form: `a0 a3` (file letter + rank digit). `undo` to revert last move, `exit` to quit.

## 6. Running the Pygame GUI
```
python -m xiangqi.ui.pygame_app
```
Drag a piece from origin square to destination square. (Highlights and asset images are placeholders—future enhancement.)

## 7. Linting & Type Checking
```
ruff check .
ruff format .    # (If you want auto-format; enable once rules chosen)
mypy .
```

## 8. Testing
Tests live under `tests/`.
```
pytest -q
```
Add coverage:
```
pytest --cov=xiangqi --cov-report=term-missing
```

## 9. Suggested Next Development Steps
1. Flesh out test coverage (rook/cannon screens, elephant river, advisor palace, flying general, self-check filtering, undo integrity).
2. Implement perft tool in `engine/perft.py` to validate move generator counts.
3. Add move highlight & last-move trace + legal move preview in GUI.
4. Replace placeholder circle rendering with actual piece images from `Pieces/` asset folders.
5. Implement checkmate / stalemate detection (game termination status method in `engine.game`).
6. Introduce evaluation + basic minimax or negamax (depth-limited) in `ai/`.
7. Transposition table & iterative deepening for stronger AI (optional).

## 10. Piece Asset Integration (Planned)
- Map internal board coordinates to pixel rectangles.
- Load appropriate Red/Black PNG from `Pieces/Chinese/Red` or `Pieces/Chinese/Black` (or English variant) based on selected theme.
- Add a lightweight asset cache in `ui/assets.py`.

## 11. Coding Conventions
- Keep core logic pure (no pygame imports in `core/` or `rules/`).
- Avoid premature optimization; prefer clarity for rule correctness.
- Use dataclasses where immutable semantics are helpful (Move, Piece).

## 12. Type & Lint Strictness
Initial strictness can be relaxed by editing `mypy.ini` or `ruff.toml`. Start strict; dial back only if velocity suffers.

## 13. Removing Poetry
`pyproject.toml` was removed in favor of plain `requirements*.txt`. If you later want to reintroduce Poetry, regenerate a `pyproject.toml` and run `poetry lock && poetry install`.

## 14. Troubleshooting
Issue: Pygame install fails on Python 3.13
Resolution: Try Python 3.12, then reinstall: `pip install -r requirements-ui.txt`.

Issue: Encoding paths with spaces or Unicode
Resolution: Always quote paths in scripts; keep virtualenv inside project root to avoid long OneDrive paths if possible.

Issue: mypy reports missing imports for pygame
Resolution: Add `types-pygame` (if available) to dev requirements or set `follow_imports = skip` for that module.

## 15. License
Add a LICENSE file (MIT recommended) before publishing.

---
Happy hacking! Build the rules first, then polish the UI.
