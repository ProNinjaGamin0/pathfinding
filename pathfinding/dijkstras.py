from .pathfinding_abc import Node, NoSolution, PathFinder

class Dijkstras(PathFinder):
    def search(self, start: Node, end: Node) -> list[Node]:
        """Implements Dijkstra's algorithm

        Args:
            start (Node): The ``Node`` to start at
            end (Node): The ``Node`` to end at

        Raises:
            NoSolution: Raised when no path exists between ``start`` and ``end``

        Returns:
            list[Node]: A list of all ``Nodes`` traversed
        """
        open_nodes:list[Node] = [start]
        closed_nodes:list[Node] = []
        while open_nodes:
            
            current_node = open_nodes[0]
            current_index = 0
            for index, node in enumerate(open_nodes):
                if node.distance(end) < current_node.distance(end):
                    current_node = node
                    current_index = index
            
            open_nodes.pop(current_index)
            closed_nodes.append(current_node)

            if current_node == end:
                return current_node.path()

            for adjacent_node in self.grid.adjacent(current_node):
                if adjacent_node.wall or adjacent_node in closed_nodes or adjacent_node in open_nodes:
                    continue
                adjacent_node.parent = current_node
                open_nodes.append(adjacent_node)

        raise NoSolution("No Path Exists")
        