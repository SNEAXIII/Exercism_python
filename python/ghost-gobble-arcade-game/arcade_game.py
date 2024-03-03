eat_ghost = lambda active_pellet, touching_ghost: active_pellet and touching_ghost
score = lambda touching_pellet, touching_dot: touching_pellet or touching_dot
lose = lambda active_pellet, touching_ghost: not active_pellet and touching_ghost
win = lambda eaten_all_dots, active_pellet, touching_ghost: eaten_all_dots and not lose(active_pellet, touching_ghost)