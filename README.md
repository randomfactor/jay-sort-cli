# Jay Sort CLI

A command-line tool to help librarians sort a collection of LPs into alphabetical order.

## Description

This program takes a file representing the current physical layout of LPs on shelves. It then calculates the optimal set of moves to get all the LPs into alphabetical order while respecting the capacity of each shelf. It outputs a series of step-by-step instructions for the librarian to follow.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/randomfactor/jay-sort-cli.git
    cd jay-sort-cli
    ```

2.  **Create a virtual environment and install dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

## Usage

To run the program, you need an input file that describes the current arrangement of albums. The file should list album names, with `---` on a line by itself to indicate a shelf break.

For example (`sample-10.txt`):
```
Desire Paths
---
War Stories
Circling
The Far Field
```

Run the script with:
```bash
.venv/bin/python main.py <your_input_file.txt>
```

This will print the move instructions to the console.

## Running Tests

The project includes a test suite to verify the sorting logic. To run the tests:
```bash
.venv/bin/python -m unittest test_main.py
```
