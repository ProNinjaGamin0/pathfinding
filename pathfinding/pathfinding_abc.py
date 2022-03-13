from abc import ABC, abstractmethod
from typing import Optional

class NoSolution(Exception):
    pass

class Node:
    def __init__(self, x, y, wall=False, parent=None) -> None:
        self.x:int = x
        self.y:int = y
        self.coords = (x, y)
        self.wall:bool = wall
        self.parent: Optional[Node] = parent

    def __eq__(self, __o: object) -> bool:
        """Checks if 2 Nodes are equal

        Args:
            __o (Node): The Node to compare to

        Raises:
            TypeError: Raised if object is not a Node

        Returns:
            bool: Whether the 2 Nodes are equal
        """
        if not isinstance(__o, Node):
            raise TypeError("Must compare between 2 Nodes")
        return self.coords == __o.coords and self.wall == __o.wall
    
    def __str__(self) -> str:
        return str(self.coords)

    def __repr__(self) -> str:
        return str(self)

    def distance(self, node):
        """Finds the distance between 2 ``Nodes`` without taking the square root

        Args:
            node (Node): ``Node`` to check distance from

        Raises:
            ValueError: Raised if ``node`` isnt a ``Node``

        Returns:
            int: Distance between ``Nodes``
        """
        if not isinstance(node, Node):
            raise ValueError("Distance must be between 2 Nodes")
        return ((self.x - node.x)**2 + (self.y - node.y)**2) # Pythagorean Theorem but no square root

    def path(self):
        """Returns a path from the root parent to this ``Node``

        Returns:
            list[Node]: A list of Nodes starting with the root parent ``Node``
        """
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]

    

class Grid:
    def __init__(self, grid:list[list[Node]]=None) -> None:
        self.grid = grid if grid is not None else [[]]

    def __contains__(self, __o) -> bool:
        if not isinstance(__o, Node):
            raise ValueError("Grid only contains Nodes")
        return __o.y < len(self.grid) and __o.y >= 0 and __o.x < len(self.grid[0]) and __o.x >= 0

    def node_at(self, x, y):
        return self.grid[y][x]

    def adjacent(self, node:Node) -> list[Node]:
        """Returns a list of Nodes surrounding ``node`` if the Nodes are in the ``Grid``

        Args:
            node (Node): The parent ``Node`` to find adjacents to

        Returns:
            list[Node]: A list of all adjacent ``Nodes``
        """
        adjacent_pos:list[tuple[int, int]] = [(-1, 0), (0, -1), (1, 0), (0, 1)]            
        adjacent_nodes:list[Node] = []
        for (x, y) in adjacent_pos:
            new_node = Node(x + node.x, y + node.y)
            if new_node not in self:
                continue
            adjacent_nodes.append(self.node_at(new_node.x, new_node.y))
        return adjacent_nodes

class PathFinder(ABC):

    def __init__(self, grid:Grid) -> None:
        self.grid:Grid = grid
        super().__init__()

    @abstractmethod
    def search(self, start:Node, end:Node) -> list[Node]:
        pass