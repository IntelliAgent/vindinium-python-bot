from Queue import PriorityQueue


class PathFinding():
    def __init__(self, game):
        self.game = game

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_path(self, current_pos, goal_pos):
        frontier = PriorityQueue()
        frontier.put(current_pos, 0)
        came_from = {}
        cost_so_far = {}
        came_from[current_pos] = None
        cost_so_far[current_pos] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal_pos:
                break

            for next in self.game.board.neighbors(current):
                new_cost = cost_so_far[current] + self.game.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + 1
                    frontier.put(next, priority)
                    came_from[next] = current

        return self.reconstruct_path(came_from, current_pos, goal_pos), cost_so_far[goal_pos]

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
