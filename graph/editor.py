import copy

from graph.validator import GraphValidator
from graph.algorithms import CurriculumAlgorithms


class GraphEditor:

    def __init__(self, graph):
        self.graph = graph

    def add_edge(self, source, target, edge_type):

        """
        Add a graph relationship with validation and rollback.

        If validation or algorithm recomputation fails,
        the graph is restored to its previous state.
        """

        # Check that nodes exist
        if source not in self.graph:
            raise ValueError(
                f"Source node '{source}' does not exist."
            )

        if target not in self.graph:
            raise ValueError(
                f"Target node '{target}' does not exist."
            )

        # Check edge type before modifying the graph
        if edge_type not in GraphValidator.ALLOWED_EDGE_TYPES:
            raise ValueError(
                f"Invalid edge type '{edge_type}'. "
                f"Allowed types: {GraphValidator.ALLOWED_EDGE_TYPES}"
            )

        # Prevent duplicate relationships
        if self.graph.has_edge(source, target):
            raise ValueError(
                f"Relationship {source} -> {target} already exists."
            )

        # Create snapshot before editing
        snapshot = copy.deepcopy(self.graph)

        try:

            # Apply edit
            self.graph.add_edge(
                source,
                target,
                type=edge_type
            )

            # 1. Validate graph integrity
            validator = GraphValidator(self.graph)
            validator.validate()

            # 2. Recompute graph algorithms
            algorithms = CurriculumAlgorithms(self.graph)

            algorithms.learning_order()
            algorithms.degree_centrality()
            algorithms.betweenness_centrality()
            algorithms.pagerank()

            print(
                f"Edit accepted: {source} -> {target} "
                f"({edge_type})"
            )

            return True

        except Exception as e:

            # Rollback graph
            self.graph.clear()

            self.graph.add_nodes_from(
                snapshot.nodes(data=True)
            )

            self.graph.add_edges_from(
                snapshot.edges(data=True)
            )

            raise ValueError(
                f"Edit rejected and rolled back: {e}"
            )