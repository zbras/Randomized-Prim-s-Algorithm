# Randomized Prim's Algorithm

***Concept game implementing a randomized version of Prim's binary search tree algorithm for maze generation.***

Requires NumPy for `where()`, `zeros()`, and `delete()`, and Pandas for `to_csv()` (only used if the array is desired - run ***/logic/maze.py***).
***/logic/game_state.py*** houses the variables for block size and maze width / height.

Prim's algorithm operates by the following rules:

1. Start with a grid of unvisited cells.
2. Choose a cell at random and mark it as part of the maze (a path cell).
   - Add the cells to the North, South, East, and West (neighbors) to the candidate wall list.
3. While the wall list is not empty, do the following:
   - Pick a random wall from the list.
     - Check if only one of the cells that wall divides is visited.
       - If 3.1.1 is satisfied, make the wall and the unvisited cell a path.
         - Add the unvisited cell's neighbors to the wall list.
   - Remove the randomly chosen wall from the wall list.

Todo:
- [ ] Add title screen
- [ ] Add options screen and corresponding options
- [ ] Add scoring system
- [ ] Add save state