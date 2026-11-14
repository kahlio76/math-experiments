# Erdős Problem 197

SAT experiments related to [Erdős Problem 197](https://www.erdosproblems.com/197): two-colorings of integers where
each class can be ordered to avoid certain arithmetic progression patterns.

- `gen.c`: writes a DIMACS instance for a coloring of [S, N] with an order on each class
- `runcnf.py`: solves a DIMACS file with CaDiCaL
- `partsat.py`, `partsat2.py`, `blocksat.py`, `window.py`: direct encodings of the partition, its blocks, and windows
- `dyadic.py`: checks a specific dyadic partition

These explore small cases only.
