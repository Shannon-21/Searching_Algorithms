from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
        grid (Grid): Grid of points

        Returns:
        Solution: Solution found
        """

        # inicializa la busqueda desde la raiz
        nodo = Node("", grid.start, 0)

        explored = {}
        explored[nodo.state] = nodo

        frontier: PriorityQueueFrontier = PriorityQueueFrontier()
        frontier.add(nodo, 0)

        while True:
            # recorre y elije un nodo de la frontera
            if frontier.is_empty(): return NoSolution(explored)
            nodo = frontier.pop()

            if nodo.state == grid.end: return Solution(nodo, explored)
            neighbours = grid.get_neighbours(nodo.state)

            # expande el nodo seleccionado
            for position in neighbours:
                child = Node("", neighbours[position],
                             nodo.cost + grid.get_cost(neighbours[position]),
                             nodo, position)
                
                # añade el nodo si no ha sido expandido antes, o si su costo es menor al mismo nodo ya expandido
                if child.state not in explored or child.cost < explored[child.state].cost:
                    explored[child.state] = child
                    frontier.add(child, child.cost)
