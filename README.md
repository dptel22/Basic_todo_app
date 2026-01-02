# Basic_todo_app
# Multi-Interface Todo Application (Python)

This project is a complete todo management system implemented with multiple interfaces: command-line, desktop GUI, and web app, all sharing the same core logic.

## Overview
The application uses a single file-based backend to manage todos and exposes it through different user interfaces, showcasing modular design and code reuse.

## Tech Stack
- Python
- File I/O
- FreeSimpleGUI
- CustomTkinter
- Streamlit

## Interfaces
- CLI: Text-based todo management
- GUI: Desktop applications using FreeSimpleGUI and CustomTkinter
- Web: Streamlit-based web interface

## Files
- `functions.py` – Core todo logic (read/write operations)
- `CLI.py` – Command-line interface
- `gui.py` – Desktop GUI using FreeSimpleGUI
- `tinkergui.py` – Modern desktop GUI using CustomTkinter
- `web.py` – Web interface using Streamlit
- `requirements.txt` – Project dependencies

## Usage
1. Install dependencies:
2. Run the desired interface:
python CLI.py
python gui.py
python tinkergui.py
streamlit run web.py


## Learning Outcome
This project demonstrates modular Python architecture, UI abstraction, and implementing the same business logic across multiple platforms.
