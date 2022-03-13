from .pathfinding_abc import Node, NoSolution, PathFinder

class BreadthFirst(PathFinder):
    def search(self, start: Node, end: Node) -> list[Node]:
        queue = [start]
        explored = [start]
        while queue:
            current_node = queue.pop(0)
            if current_node == end:
                return current_node.path()
            
            for adjacent_node in self.grid.adjacent(current_node):
                if adjacent_node in explored or adjacent_node.wall:
                    continue
                adjacent_node.parent = current_node
                queue.append(adjacent_node)
                explored.append(adjacent_node)

        raise NoSolution("No Path Exists")