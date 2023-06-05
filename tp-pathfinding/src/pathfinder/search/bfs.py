from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
        grid (Grid): Grid of points

        Returns:
        Solution: Solution found
        """

        # inicializa la busqueda desde la raiz
        node = Node("", grid.start, 0)

        explored = {}
        explored[node.state] = True

        if node.state == grid.end: return Solution(node, explored)

        frontier = QueueFrontier()
        frontier.add(node)

        while True:
            # recorre y elije un nodo de la frontera
            if frontier.is_empty(): return NoSolution(explored)
            nodo = frontier.remove()
            explored[nodo.state] = True
            neighbours = grid.get_neighbours(nodo.state)

            # expande el nodo seleccionado
            for position in neighbours:
                child = Node("", neighbours[position],
                             nodo.cost + grid.get_cost(neighbours[position]),
                             nodo, position)
                
                if child.state == grid.end: return Solution(child, explored)

                # añade el hijo a la frontera
                if child.state not in explored:
                    explored[child.state] = True
                    frontier.add(child)
