from .pathfinding_abc import PathFinder, Node, Grid, NoSolution

class AStarNode(Node):
    def __init__(self, x, y, wall=False, parent=None) -> None:
        self.f = 0
        self.g = 0
        self.h = 0
        super().__init__(x, y, wall, parent)
    
    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)
    
    @classmethod
    def from_node(cls, node:Node, parent=None):
        """Creates an ``AStarNode`` from a ``Node``

        Args:
            node (Node): The ``Node`` to create from
            parent (AStarNode, optional): The parent ``AStarNode`` of this ``Node``. Defaults to None.

        Returns:
            AStarNode: The ``AStarNode`` version of the ``Node``
        """
        return cls(node.x, node.y, node.wall, parent)

    def to_node(self) -> Node:
        """Converts AStarNode into a Node

        Returns:
            Node: The Node version of the AStarNode
        """
        return Node(self.x, self.y, self.wall)


class AStar(PathFinder):
    def __init__(self, grid:Grid) -> None:
        super().__init__(grid)

    def search(self, start: Node, end: Node) -> list[Node]:
        """Finds a path between ``start`` and ``end`` if one exists using the A* pathfinding algorithim

        Args:
            start (Node): ``Node`` to start from
            end (Node): ``Node`` to find path to

        Raises:
            NoSolution: Raised if no path exists between ``start`` and ``end``

        Returns:
            list[Node]: A list of ``Nodes`` traversed to get from ``start`` to ``end``
        """
        open_nodes = [AStarNode.from_node(start)]
        closed_nodes:list[AStarNode] = []
        end = AStarNode.from_node(end)
        while open_nodes:
            current_node = open_nodes[0]
            current_index = 0


            for index, item in enumerate(open_nodes):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_nodes.pop(current_index)
            closed_nodes.append(current_node)
            
            # Check to see if the goal is reached
            if current_node == end:
                return current_node.path()

            children:list[AStarNode] = []
            for adjacent_node in self.grid.adjacent(current_node):
                adjacent_node = AStarNode.from_node(adjacent_node, current_node)
                if adjacent_node.wall:
                    continue
                children.append(adjacent_node)
            
            for child in children:
                if child in closed_nodes:
                    continue

                child.g = current_node.g + 1
                child.h = child.distance(end)
                child.f = child.g + child.h

                for open_node in open_nodes:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_nodes.append(child)
        # If we went through every node in open_nodes and we didnt get to the end node
        # That means that no path between the two nodes exist
        raise NoSolution("No Path exists")
