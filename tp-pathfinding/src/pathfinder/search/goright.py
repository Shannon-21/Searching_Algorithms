from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GoRight:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Go Right

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """

        node = Node("", state=grid.start, cost=0)

        explored = {} 

        frontier = QueueFrontier()
        frontier.add(node)

        while True:
            if frontier.is_empty(): return NoSolution(explored)
            node = frontier.remove()
            explored[node.state] = True

            if node.state == grid.end: return Solution(node, explored)
            neighbours = grid.get_neighbours(node.state)

            if 'right' in neighbours:
                new_state = neighbours['right']
                new_node = Node("", new_state, node.cost + grid.get_cost(new_state))
                new_node.parent = node
                new_node.action = 'right'

                frontier.add(new_node)
