import random
from collections import deque
import heapq
import pandas as pd

# puzzle


def neighbors(state, size):
    zero = state.index(0)
    row, col = divmod(zero, size)
    nbrs = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < size and 0 <= c < size:
            new_zero = r * size + c
            new_state = list(state)
            new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
            nbrs.append(tuple(new_state))
    return nbrs


# Heuristic: number of tiles
def h_out_of_place(state, goal):
    count = 0
    for i, tile in enumerate(state):
        if tile != 0 and tile != goal[i]:
            count += 1
    return count


# Heuristic: total of Manhattan distances
def h_manhattan(state, size):
    dist = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_row, goal_col = divmod(tile - 1, size)
        row, col = divmod(i, size)
        dist += abs(row - goal_row) + abs(col - goal_col)
    return dist


#  random walk
def random_walk(start, steps, size):
    state = start
    for _ in range(steps):
        state = random.choice(neighbors(state, size))
    return state


# Reconstruct
def reconstruct_path(came_from, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


# Search algorithms
MAX_EXPANSIONS = 1000000


def bfs(start, goal, size):
    frontier = deque([start])
    came_from = {start: None}
    nodes = 0
    while frontier:
        state = frontier.popleft()
        nodes += 1
        if state == goal:
            return reconstruct_path(came_from, state), nodes
        for nbr in neighbors(state, size):
            if nbr not in came_from:
                came_from[nbr] = state
                frontier.append(nbr)
        if nodes > MAX_EXPANSIONS:
            return None, nodes
    return None, nodes


def a_star(start, goal, size, heuristic):
    # heuristic
    frontier = []
    heapq.heappush(frontier, (heuristic(start), 0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes = 0
    while frontier:
        _, cost, state = heapq.heappop(frontier)
        nodes += 1
        if state == goal:
            return reconstruct_path(came_from, state), nodes
        for nbr in neighbors(state, size):
            new_cost = cost + 1
            if nbr not in cost_so_far or new_cost < cost_so_far[nbr]:
                cost_so_far[nbr] = new_cost
                hval = heuristic(nbr)
                priority = new_cost + hval
                heapq.heappush(frontier, (priority, new_cost, nbr))
                came_from[nbr] = state
        if nodes > MAX_EXPANSIONS:
            return None, nodes
    return None, nodes


# Experiment
results = []
sizes = [3, 4]
depths = [5, 10, 20, 40, 80]
goals = {3: tuple(list(range(1, 9)) + [0]), 4: tuple(list(range(1, 16)) + [0])}

for size in sizes:
    goal = goals[size]
    for depth in depths:
        for trial in range(3):
            start = random_walk(goal, depth, size)
            # BFS
            path_bfs, nodes_bfs = bfs(start, goal, size)
            length_bfs = len(path_bfs) - 1 if path_bfs else None
            results.append(
                {
                    "size": size,
                    "depth": depth,
                    "algorithm": "BFS",
                    "start_state": start,
                    "solution": path_bfs,
                    "solution_length": length_bfs,
                    "nodes_expanded": nodes_bfs,
                }
            )

            path_h1, nodes_h1 = a_star(
                start, goal, size, lambda s: h_out_of_place(s, goal)
            )
            length_h1 = len(path_h1) - 1 if path_h1 else None
            results.append(
                {
                    "size": size,
                    "depth": depth,
                    "algorithm": "A*_OutOfPlace",
                    "start_state": start,
                    "solution": path_h1,
                    "solution_length": length_h1,
                    "nodes_expanded": nodes_h1,
                }
            )

            path_h2, nodes_h2 = a_star(
                start, goal, size, lambda s: h_manhattan(s, size)
            )
            length_h2 = len(path_h2) - 1 if path_h2 else None
            results.append(
                {
                    "size": size,
                    "depth": depth,
                    "algorithm": "A*_Manhattan",
                    "start_state": start,
                    "solution": path_h2,
                    "solution_length": length_h2,
                    "nodes_expanded": nodes_h2,
                }
            )

# Save results
df = pd.DataFrame(results)
print(df)
