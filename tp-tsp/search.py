"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Controla el numero de iteraciones antes de un reset
        n_iters = 0

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:
            # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una acción aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un óptimo local
            if diff[act] <= 0:
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                break

            # Sino, moverse a un nodo con el estado sucesor
            else:
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1
                n_iters += 1
                
                # Esta configuracion funciona bien para att48, puede variar en los demas problemas
                if n_iters > 45:
                    print("--------------- Hill Climbing Reset ---------------")
                    actual = Node(problem.init, problem.obj_val(problem.init))
                    problem.random_reset()
                    n_iters = 0
                    

class Tabu(LocalSearch):
    """Algoritmo de búsqueda Tabu."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con búsqueda Tabu.

        Arguments:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        current = Node(problem.init, problem.obj_val(problem.init))
        best = current

        # Confugraciones iniciales, funcionan bien para att48, puede variar en los demas problemas
        tabu_list = []
        max_iterations = 100
        max_iterations_without_improvement = 10
        max_tabu_iterations = 20
        iterations_without_improvement = 0

        # Criterio de parada: Maximo numero de iteraciones y maximo numero numero de iteraciones sin mejora
        while self.niters < max_iterations and iterations_without_improvement < max_iterations_without_improvement:
            # Genera todos los vecinos al nodo actual
            successors = []
            actions = problem.actions(current.state)
            for action in actions:
                successor = problem.result(current.state, action)
                successors.append(successor)

            # Elije el mejor nodo que no es tabu
            best_successor = None
            for successor in successors:
                if successor not in tabu_list:
                    successor_value = problem.obj_val(successor)
                    if best_successor is None or successor_value > problem.obj_val(best_successor):
                        best_successor = successor

            # Actualiza la lista tabu, remueve los estados que han permanecido por n iteraciones
            tabu_list.append(best_successor)
            tabu_list = [element for element in tabu_list if self.niters - element[1] <= max_tabu_iterations]

            # Actualiza el mejor estado y el actual si es necesario
            current = Node(best_successor, problem.obj_val(best_successor))
            if current.value > best.value:
                best = current
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

            self.niters += 1

        # Asignacion de la solucion
        self.tour = best.state
        self.value = problem.obj_val(best.state)
        end = time()
        self.time = end - start 