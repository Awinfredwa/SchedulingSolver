# This is a progress recording
## March 1st Update:
**Some important files:**
- Code of our main model setup including some testing samples: Solver.py
- Code to load data (provided by Garrett) and calling the model: test.py
- A simpler model (ignoring that courses can have different sections), which has already been tested to work with Garrett's data: simpleSolver.py

**TODO**: Fixing the problem in Solver.py that students are assigned to not only classes in preferenced set but also other classes while the preference set assignment looks good.

## March 28th Update:
**Solver.py:** is now able to produce reasonable solution to sample data and is also compatible with test data (run in test.py).

**How to Run:** To run with sample data, type `python3 Solver.py`. To run with test data, type `python3 test.py`.