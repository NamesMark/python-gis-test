# Task
You are tasked with developing a street colouring algorithm using Python3. Your algorithm should color lines in the same color when perceived as a single street.

# Explanation

## Intuition
Out of the sample files we are interested in the .shp file.
The task immediately looks like an assignment to color a graph using dfs, but remains to be seen if there's a better solution.
For each multiline end point, if there exist another multiline, it is of the same color (street),
- If only one, then it's the same color
- If more than one, then one of them, specifically, with the smallest angle to the current one.

## Approach


## Complexity

# Solution example
## Input

## Output




