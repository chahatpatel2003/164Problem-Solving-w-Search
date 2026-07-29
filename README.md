# Sliding Puzzle Search Algorithms

A Python implementation comparing uninformed and informed search techniques for solving sliding-tile puzzles.

## Overview

This academic artificial intelligence project explores how different search strategies solve randomized sliding-puzzle states.

The implementation includes:

- Breadth-First Search (BFS)
- A* Search
- Misplaced-tile heuristic
- Manhattan-distance heuristic
- Randomized puzzle generation
- Path reconstruction
- Performance comparison using Pandas

## Repository Structure

```text
.
├── notebooks/
│   └── sliding_puzzle_search.ipynb
├── results/
│   └── search_algorithm_output.pdf
├── src/
│   └── sliding_puzzle_search.py
├── .gitignore
└── README.md
```

## Technologies

- Python
- Pandas
- Jupyter Notebook
- Data Structures
- Graph Search
- Heuristic Search

## Algorithms

### Breadth-First Search

BFS explores puzzle states level by level and finds the shortest solution when all moves have equal cost.

### A* Search

A* prioritizes states using the estimated total cost: `f(n) = g(n) + h(n)`.

The project evaluates two heuristics:

- Number of misplaced tiles
- Total Manhattan distance

## Run Locally

```bash
python3 -m pip install -r requirements.txt
python3 src/sliding_puzzle_search.py
```

The notebook can also be opened through Jupyter Notebook or Google Colab.

## Academic Context

Developed as part of artificial intelligence coursework at California State University, Fresno.
