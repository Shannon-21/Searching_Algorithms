from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
        grid (Grid): Grid of points

        Returns:
        Solution: Solution found
        """

        # inicializa la busqueda desde la raiz
        nodo = Node("", grid.start, 0)

        expanded = {}

        frontier = StackFrontier()
        frontier.add(nodo)

        while True:
            # recorre y ejile un nodo de la frontera
            if frontier.is_empty(): return NoSolution(expanded)
            nodo = frontier.remove()

            if nodo.state == grid.end: return Solution(nodo, expanded)

            # verifica que el nodo ya no haya sido exandido antes
            if nodo.state not in expanded:
                expanded[nodo.state] = True
                neighbours = grid.get_neighbours(nodo.state)

                # expande el nodo seleccionado
                for position in neighbours:
                    child = Node("", neighbours[position],
                                nodo.cost + grid.get_cost(neighbours[position]),
                                nodo, position)
                    
                    if child.state not in expanded:
                        frontier.add(child)
